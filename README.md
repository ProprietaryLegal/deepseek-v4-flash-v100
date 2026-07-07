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

## The bug you need to know about

With a **quantized K-cache** (`--cache-type-k q8_0`), DeepSeek-V4-Flash on
Volta loads cleanly, serves a green `/health`, and emits **confident
gibberish** — no CUDA error, nothing in the logs. A controlled one-variable
matrix (two sha256-verified quants, CPU control, architecture control,
single-GPU K/V-type sweep) pinned it: corruption occurs **iff the K-cache is
quantized**, independent of FlashAttention mode and V-cache type. DeepSeek's
MLA stores an unusually wide K row (head dim 576 = 512 latent + 64 RoPE); the
q8_0 K path for that shape is numerically wrong on sm_70.

**Fix:** run `--cache-type-k f16`. The MLA K-cache is small; the cost is
negligible. The [`patches/`](patches/) directory ships a fail-loud guard
(also on the [`ds4-volta-fix`](https://github.com/Mermiges/llama.cpp/tree/ds4-volta-fix)
branch) that refuses the broken configuration at startup instead of serving
garbage. Full analysis, including two failed kernel-level fixes published as
negative results: [`docs/research-notes.md`](docs/research-notes.md).

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
