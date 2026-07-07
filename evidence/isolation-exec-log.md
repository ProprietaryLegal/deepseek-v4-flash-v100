# DS4FIX exec log — DeepSeek-V4-Flash on Volta (sm_70)

**Lane:** DS4FIX Fable deputy (v100-research)
**Date:** 2026-07-07 (V100 node, post-reboot, driver healthy)
**Plan:** `documents/plans/2026-07-07_ds4-volta-fix-plan.md`
**Granted GPUs:** 6 and 12 (probes). No NCCL, no reboots, no 8-card launches.

> **Bottom line:** DeepSeek-V4-Flash garbles on V100 **only when the K-cache is quantized
> (`--cache-type-k q8_0`)**. With an **f16 K-cache** it is coherent, with FlashAttention
> ENABLED, on Volta. The fix is operational — `--cache-type-k f16` — and needs **no code
> change**. My initial "FlashAttention kernel" hypothesis was WRONG and was reverted; see §5.

---

## 1. Discriminators consumed
- **CPU-only** (`-ngl 0`, build-unified, canonical UD-Q4_K_XL, CPU server :8324): `"…is"` →
  `" Paris."` — coherent. Weights/graph/tokenizer fine; bug is GPU-side.
- **MiniMax-M3** 8-card, same build/flags (orchestrator): coherent at 7.2K prefill. Normal
  attention geometry + q8_0 KV are fine on Volta ⇒ the fault is something DS4 uniquely exercises.

## 2. Method
Single V100, all 43 layers' attention on GPU, experts on CPU (`-ngl 999 -ot 'exps=CPU'`), so
every attention op runs on Volta while the MoE bulk stays on the coherent CPU path. Prompt
`"The capital of France is"`, greedy. "GARBAGE" = confident non-language
(`newcom … 大有 … regiment tact`) that fails the server's content parse.

## 3. Evidence matrix (the decisive part)
My first two probes changed **two** variables at once (`-fa` AND KV type), which produced a
wrong inference. Holding variables fixed and toggling one at a time isolates it:

| Run | Build | `-fa` | K cache | V cache | GPU | Output |
|---|---|---|---|---|---|---|
| Probe A | unpatched | 1 | q8_0 | q8_0 | 6 | **GARBAGE** |
| Probe B | unpatched | 0 | f16 | f16 | 6 | coherent |
| Verify  | patched   | auto | f16 | f16 | 6 | coherent |
| Control | unpatched | auto | f16 | f16 | 12 | coherent |
| test 6  | patched   | 1 | q8_0 | q8_0 | 12 | **GARBAGE** |
| G1      | unpatched | 1 | f16 | f16 | 12 | coherent |
| G2      | patched   | 1 | f16 | f16 | 6 | coherent |

Then a clean KV-quant matrix (build-unified, `-fa 1`, GPU 12), which **pins K vs V**:

| K cache | V cache | Output |
|---|---|---|
| q8_0 | q8_0 | **GARBAGE** |
| q8_0 | f16  | **GARBAGE** |
| f16  | q8_0 | coherent |
| f16  | f16  | coherent |
Raw: `/tmp/ds4fix-kvmatrix.out`.

**Reading:** garbage ⇔ K-cache is quantized, independent of `-fa` (0/1/auto), independent of the
patch (patched==unpatched everywhere), and independent of V-cache quant. FlashAttention on Volta
computes DS4's MLA 576/512 geometry **correctly** with an f16 K-cache.

## 4. Root cause
The **q8_0 K-cache dequantization path on Volta (sm_70) is numerically wrong for DeepSeek's MLA
latent K (head_dim 576)**. It corrupts the attention scores → confident gibberish, with no CUDA
trap (a silent-corruption seam). V-cache q8_0 is fine; normal-geometry q8_0 K (M3) is fine — it
is specifically the large-head MLA K dequant on Volta. This is the K-side analogue of the region
the cchuter `d4e21f0d3` commit patches (the `dequantize_V_q8_0<half>` templates); the sm_70
hardware-FP16 arm of the quantized-K dequant lacks the FP32-accumulate/software-FP16 fallback
needed for this shape.

## 5. Fix
**Operational, proven, zero code: run DS4 with `--cache-type-k f16`.** V-cache may stay q8_0 or
f16 (both coherent); simplest is f16/f16. FlashAttention stays ENABLED (`-fa 1` or `-fa auto`) —
it is fast and correct with f16 K. DS4's MLA K-cache is tiny (latent), so f16 costs almost nothing.

### Wrong turn — the confounded-A/B lesson (kept deliberately)
**Methodological lesson worth preserving.** My first "root cause" was wrong because probe A and
probe B differed in **two** variables at once — `-fa` (1→0) *and* KV type (q8_0→f16). Both flips
pointed the same way (garbage→coherent), so I attributed the effect to the more salient variable
(FlashAttention) and missed the real one (KV-cache quant). A two-variable A/B can only tell you
"one of these matters," never which. The fix was to re-run holding each variable fixed and toggling
exactly one (§3), which immediately exonerated `-fa` and convicted the q8_0 K-cache. **Rule for
this campaign: never name a root cause from an A/B that moved more than one knob — isolate to a
single variable first.**

Consequence: I first patched `ggml_cuda_get_best_fattn_kernel` to disable FA for Volta 576/512.
Runs G1 vs G2 (patched == unpatched at every config) prove that patch is a **no-op**, and test 6
(patched, q8_0 K, still garbles) proves it does not touch the real fault; it would also needlessly
disable a working FA path. **Reverted** (`git checkout -- ggml/src/ggml-cuda/fattn.cu`; worktree
diff now empty). No code committed to `ds4-volta-fix`.

## 6. Build (retained for reference)
`build-ds4fix` (separate dir; build-unified untouched): Release, `CUDA_ARCHITECTURES=70`,
`FA_ALL_QUANTS=OFF`, `FORCE_MMQ=OFF`, `NATIVE=ON`; `[100%] Built target llama-server`, exit 0.

## 7. 8-card verification — PASS (confirmed at scale by orchestrator)
Stock build-unified, DS4 UD-Q4_K_XL, boards A+B, `-sm layer -fa 1`, **f16 KV**:
- Raw completion coherent (`"Paris… The capital of Germany is Berlin."`).
- Full quality screen **6/6** (5 legal prompts + needle@~3.7K tokens retrieved verbatim).
- **tg ~12.0 tok/s** at 8 cards with FlashAttention ON.
Confirms the corrected root cause and the f16-K fix at the real serving scale.

## 8. Handoff
- **Roadmap for codex MSA sm_70 kernel lane** (two items):
  1. Fix the Volta quantized-K dequant numerics for the MLA 576 head (FP32 accumulate /
     software-FP16 fallback, mirroring `d4e21f0d3`'s V-side approach) so q8_0 K works — recovers
     the small extra KV saving. Failing kernels: the q8_0 K-dequant reached from `fattn-tile`/
     `fattn-mma-f16` for the 576/512 case.
  2. **Fail-loud guard** (MANDATORY per CLAUDE.md, since this is a silent-corruption seam): on
     Volta, when the model is DeepSeek-MLA (n_embd_head_k==576 / deepseek arch) and
     `--cache-type-k` is quantized, emit a clear error ("quantized K-cache is numerically broken
     on sm_70 for DeepSeek MLA; use --cache-type-k f16") rather than serving garbage. Best placed
     in `llama-context` KV validation (device-CC + arch aware), not in FA dispatch.
