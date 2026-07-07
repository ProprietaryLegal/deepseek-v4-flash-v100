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
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |   1 |           pp512 |        228.28 ± 0.31 |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |   1 |          pp8192 |        209.24 ± 1.14 |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |   1 |           tg128 |         12.22 ± 0.12 |

build: 87e767e5c (9644)
BENCH_DS4_RC=0
