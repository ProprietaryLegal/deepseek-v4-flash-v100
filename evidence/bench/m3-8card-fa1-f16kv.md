ggml_cuda_init: found 8 CUDA devices (Total VRAM: 259953 MiB):
  Device 0: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 1: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 2: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 3: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 4: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 5: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 6: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 7: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
| model                          |       size |     params | backend    | ngl |  fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --: | --------------: | -------------------: |
| minimax-m3 ?B Q2_K - Medium    | 133.14 GiB |   425.95 B | CUDA       | 999 |   1 |           pp512 |       280.07 ± 10.83 |
| minimax-m3 ?B Q2_K - Medium    | 133.14 GiB |   425.95 B | CUDA       | 999 |   1 |          pp8192 |        269.66 ± 7.54 |
| minimax-m3 ?B Q2_K - Medium    | 133.14 GiB |   425.95 B | CUDA       | 999 |   1 |           tg128 |         31.23 ± 0.41 |

build: 87e767e5c (9644)
BENCH_M3_RC=0
