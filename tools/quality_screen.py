#!/usr/bin/env python3
"""Quality screen for V100 serving smokes (runbook step 3).

5 legal prompts (drafting tone + doctrine) + needle-in-haystack at a chosen
context depth, against a llama.cpp /v1/chat/completions endpoint.

Usage:
    python3 tools/quality_screen.py --port 8322 --label ds4-udq4 [--needle-tokens 14000]

Writes a transcript to findings/raw/quality-screen-<label>-<port>.md and prints
a PASS/FAIL summary line per probe. Exit code 0 only if all probes returned
HTTP 200 and the needle was retrieved verbatim.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent  # transcripts land in <repo>/findings/raw/ (created on demand)

LEGAL_PROMPTS: list[tuple[str, str]] = [
    ("custody-standard",
     "In one paragraph, state the standard a South Carolina family court applies to a "
     "request to modify child custody, naming the controlling considerations."),
    ("alimony-factors",
     "List five statutory factors a South Carolina court weighs when awarding alimony, "
     "one line each."),
    ("drafting-tone",
     "Draft a single formal paragraph for a motion asking the court to compel discovery "
     "responses that are 45 days overdue, in a firm but professional litigator's voice."),
    ("hearsay",
     "Explain in two sentences why a text message offered to prove the truth of its "
     "contents is hearsay, and name one exception that might admit it."),
    ("arithmetic-count",
     "Count from 1 to 20, comma-separated, then state the sum of 17 and 25."),
]

NEEDLE_FACT = "The access code for the Magnolia file is MAGNOLIA-4471."
NEEDLE_QUESTION = "What is the access code for the Magnolia file? Answer with the code only."
FILLER = (
    "The parties appeared before the court on numerous occasions to address routine "
    "scheduling matters, none of which bear on the present motion. Counsel exchanged "
    "correspondence regarding discovery logistics, deposition availability, and the "
    "sequencing of expert disclosures throughout the pendency of the action. "
)


def chat(port: int, content: str, max_tokens: int = 1500, temperature: float = 0.2,
         timeout: int = 900) -> tuple[str, dict]:
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/v1/chat/completions",
        data=json.dumps({
            "messages": [{"role": "user", "content": content}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read())
    return body["choices"][0]["message"]["content"], body.get("usage", {})


def build_needle_prompt(target_tokens: int) -> str:
    # ~60 words/~80 tokens per filler block; place needle at ~40% depth.
    blocks = max(10, target_tokens // 80)
    needle_at = int(blocks * 0.4)
    parts = []
    for i in range(blocks):
        if i == needle_at:
            parts.append(NEEDLE_FACT)
        parts.append(FILLER)
    parts.append("\n\nBased only on the text above: " + NEEDLE_QUESTION)
    return "".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--needle-tokens", type=int, default=6000,
                    help="approx prompt tokens for the needle test (fit inside server -c)")
    args = ap.parse_args()

    out = REPO / "findings" / "raw" / f"quality-screen-{args.label}-{args.port}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# Quality screen — {args.label} (port {args.port})",
             f"*{time.strftime('%Y-%m-%d %H:%M:%S %Z')}*", ""]
    failures = 0

    for name, prompt in LEGAL_PROMPTS:
        t0 = time.time()
        try:
            text, usage = chat(args.port, prompt)
            # fail loud on empty visible content (e.g. reasoning consumed the whole
            # token budget) — an empty completion is a failure, never an OK
            if str(text).strip():
                status = "OK"
            else:
                status = "EMPTY"
                failures += 1
        except Exception as exc:  # noqa: BLE001 — record and count every failure mode
            text, usage, status = f"ERROR: {exc}", {}, "FAIL"
            failures += 1
        dt = time.time() - t0
        print(f"[{status}] {name} ({dt:.1f}s)")
        lines += [f"## {name} [{status}] ({dt:.1f}s)", "**Prompt:** " + prompt, "",
                  "```", str(text), "```", f"usage: {usage}", ""]

    prompt = build_needle_prompt(args.needle_tokens)
    t0 = time.time()
    try:
        # generous budget: reasoning models spend tokens thinking before the answer
        text, usage = chat(args.port, prompt, max_tokens=1500)
        got = "MAGNOLIA-4471" in str(text)
        status = "OK" if got else "MISS"
        if not got:
            failures += 1
    except Exception as exc:  # noqa: BLE001
        text, usage, status = f"ERROR: {exc}", {}, "FAIL"
        failures += 1
    dt = time.time() - t0
    print(f"[{status}] needle@~{args.needle_tokens}tok ({dt:.1f}s)")
    lines += [f"## needle@~{args.needle_tokens}tok [{status}] ({dt:.1f}s)", "",
              "```", str(text), "```", f"usage: {usage}", ""]

    out.write_text("\n".join(lines))
    print(f"transcript: {out}")
    print(f"RESULT: {'PASS' if failures == 0 else f'FAIL ({failures} probes)'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
