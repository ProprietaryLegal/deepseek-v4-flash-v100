ggml_cuda_init: found 8 CUDA devices (Total VRAM: 259953 MiB):
  Device 0: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 1: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 2: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 3: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 4: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 5: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 6: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 7: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
| model                          |       size |     params | backend    | ngl | type_k | type_v |  fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -----: | -----: | --: | --------------: | -------------------: |
| minimax-m3 ?B Q2_K - Medium    | 133.14 GiB |   425.95 B | CUDA       | 999 |   q8_0 |   q8_0 |   1 |           pp512 |       282.25 ± 16.99 |
| minimax-m3 ?B Q2_K - Medium    | 133.14 GiB |   425.95 B | CUDA       | 999 |   q8_0 |   q8_0 |   1 |          pp8192 |        239.69 ± 7.68 |
| minimax-m3 ?B Q2_K - Medium    | 133.14 GiB |   425.95 B | CUDA       | 999 |   q8_0 |   q8_0 |   1 |           tg128 |         29.53 ± 0.06 |

build: 87e767e5c (9644)
BENCH_M3_Q8KV_RC=0
