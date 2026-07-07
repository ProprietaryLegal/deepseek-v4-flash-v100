ggml_cuda_init: found 10 CUDA devices (Total VRAM: 324941 MiB):
  Device 0: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: no, VRAM: 32494 MiB
  Device 1: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: no, VRAM: 32494 MiB
  Device 2: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: no, VRAM: 32494 MiB
  Device 3: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: no, VRAM: 32494 MiB
  Device 4: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: no, VRAM: 32494 MiB
  Device 5: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: no, VRAM: 32494 MiB
  Device 6: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: no, VRAM: 32494 MiB
  Device 7: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: no, VRAM: 32494 MiB
  Device 8: Tesla V100-SXM2-32GB-LS, compute capability 7.0, VMM: no, VRAM: 32494 MiB
  Device 9: Tesla V100-SXM2-32GB-LS, compute capability 7.0, VMM: no, VRAM: 32494 MiB
| model                          |       size |     params | backend    | ngl |  fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --: | --------------: | -------------------: |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |   1 |           pp512 |        204.61 ± 0.29 |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |   1 |          pp8192 |        190.12 ± 0.85 |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |   1 |           tg128 |         11.46 ± 0.10 |

build: 8e7f3c017 (9898)
DS4_10_RC=0
