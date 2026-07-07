# DeepSeek-V4-Flash on V100 (Volta / sm_70)

**PLI Labs research release.** DeepSeek-V4-Flash (284B / ~13B-active MoE, MLA
attention) serving correctly on eight 2017-era NVIDIA V100-SXM2-32GB GPUs —
to our knowledge the first published Volta datapoint for this model — plus the
root-cause analysis of a silent-output-corruption bug that anyone running
DeepSeek-family MLA models on quantized K-caches under CC 7.0 should read.

## Headline numbers

8× V100-SXM2-32GB (one node, two NVLink quad boards, power-capped 245 W/GPU),
llama.cpp layer split, FlashAttention on, f16 KV-cache, `llama-bench -r 3`:

| model | pp512 t/s | pp8192 t/s | tg t/s |
|---|---:|---:|---:|
| **DeepSeek-V4-Flash UD-Q4_K_XL** | **228.3 ± 0.3** | **209.2 ± 1.1** | **12.2 ± 0.1** |
| **DeepSeek-V4-Flash, tuned batching** (`-b 2048 -ub 1024`) | — | 205.4 ± 2.1 | **12.9 ± 0.1** |
| MiniMax-M3 UD-Q2_K_XL (same rig, comparison) | 280.1 ± 10.8 | 269.7 ± 7.5 | 31.2 ± 0.4 |
| MiniMax-M3, tuned batching | — | ~299 | ~33.6 |

Batch-size sweep verdict: `-b 2048 -ub 1024` is the best serving config for
both models (+5–6% generation over the initial `-b 1024 -ub 512`).

Output verified coherent at temperature 0, through a legal-drafting quality
screen and verbatim needle retrieval from multi-thousand-token prompts
(transcripts in [`evidence/quality-screens/`](evidence/quality-screens/)).

## The bug you need to know about — UPDATED: it affects EVERY backend, not just Volta

With a **quantized K-cache** (`--cache-type-k q8_0`), DeepSeek-V4-Flash loads
cleanly, serves a green `/health`, and emits **confident gibberish** — no
error, nothing in the logs. Our first root cause blamed a Volta (sm_70)
kernel; continued investigation **disproved that**: the identical garbage
reproduces on **CPU-only** inference, and the suspect GPU kernels all pass
isolated numeric tests. Upstream issue:
[ggml-org/llama.cpp#25382](https://github.com/ggml-org/llama.cpp/issues/25382).

The real mechanism is graph-level: a quantized K-cache enables llama.cpp's
Hadamard "incoherence rotation," and the mere presence of that rotation
**diverts DeepSeek-V4 off its designed sparse attention paths** into a
fallback that applies the rotation with the wrong matmul primitive and never
un-rotates the MLA V-view output. Full trail, including our own wrong first
attribution kept for the record: [`docs/research-notes.md`](docs/research-notes.md)
and [`evidence/`](evidence/).

**Operational fix (any build):** run `--cache-type-k f16` — negligible cost,
MLA's cache is tiny by design. **Code fix (verified):** the
[`ds4-volta-fix`](https://github.com/Mermiges/llama.cpp/tree/ds4-volta-fix)
branch (patches in [`patches/`](patches/)) disables the rotation for this
architecture; the full 4-cell K/V matrix is coherent after it — quantized-K
becomes usable again ([`evidence/ds4fix-live-matrix-20260707.md`](evidence/ds4fix-live-matrix-20260707.md)).
A deeper fix making the sparse paths rotation-aware is in progress.

## Quickstart

```sh
git clone -b ds4-volta-fix https://github.com/Mermiges/llama.cpp
cmake -S llama.cpp -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=70 -DCMAKE_BUILD_TYPE=Release
cmake --build build --target llama-server llama-bench -j

build/bin/llama-server \
  -m DeepSeek-V4-Flash-UD-Q4_K_XL-00001-of-00005.gguf \
  -ngl 999 -sm layer -fa 1 -b 2048 -ub 1024 -c 8192 \
  --cache-type-k f16 --cache-type-v f16
```

Model: [unsloth/DeepSeek-V4-Flash-GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF)
`UD-Q4_K_XL` (144 GiB, 5 shards) — verify shard sha256s against the HF LFS
manifest before serving; both failure investigations here started by ruling
the weights out that way.

Hard rules on this hardware: **layer split only** (`-sm layer`), **f16
K-cache** (correctness), fp16 compute (no bf16/FP8 on Volta), and **8 GPUs is
the sweet spot**. CUDA's peer-mapping limit aborts >8 GPUs on the default
build (`peer mapping resources exhausted`); a `GGML_CUDA_NO_VMM=ON` build
crosses the limit, but the measured scaling ladder says don't bother for
these models: 10 GPUs ≈ par with 8 (DS4 tg 11.5 vs 12.2), and 14 GPUs
**halves** throughput (DS4 113 pp8K / 7.8 tg) once the split spans four
PCIe-hopped NVLink islands. More cards buy KV headroom for very long
contexts, not speed.

## Repo map

| path | contents |
|---|---|
| [`docs/research-notes.md`](docs/research-notes.md) | Full research record: provenance, isolation matrices, guard design, negative results, throughput, reproduction |
| [`evidence/isolation-exec-log.md`](evidence/isolation-exec-log.md) | Raw execution log of the root-cause lane (every probe, honest first-hypothesis failure included) |
| [`evidence/bench/`](evidence/bench/) | Raw `llama-bench` outputs with build SHAs |
| [`evidence/quality-screens/`](evidence/quality-screens/) | Quality-screen transcripts (legal-drafting probes + needle retrieval) |
| [`patches/`](patches/) | The fail-loud guard as `git am`-able patch against llama.cpp `v100-unified` |
| [`tools/quality_screen.py`](tools/quality_screen.py) | Stdlib-only quality screen used for the PASS/FAIL gates (empty completions fail loudly) |

## Why PLI Labs does this

Proprietary Legal Intelligence builds legal AI that a law practice can run
entirely on-premises. Eight used V100s provide 256 GB of pooled VRAM for less
than a year of per-seat SaaS; if current frontier-class open MoE models run
*correctly* there, private legal AI becomes accessible to small firms with
strict confidentiality requirements. Correctness is the operative word — this
release exists because the scariest failure we found was a model that looked
healthy while being wrong.

Nothing in this repository is legal advice. Questions and replication reports
are welcome via issues.

*PLI Labs — Proprietary Legal Intelligence, LLC. Apache-2.0 licensed.*
