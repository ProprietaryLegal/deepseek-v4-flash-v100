ggml_cuda_init: found 14 CUDA devices (Total VRAM: 454917 MiB):
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
  Device 10: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: no, VRAM: 32494 MiB
  Device 11: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: no, VRAM: 32494 MiB
  Device 12: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: no, VRAM: 32494 MiB
  Device 13: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: no, VRAM: 32494 MiB
| model                          |       size |     params | backend    | ngl |  fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --: | --------------: | -------------------: |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |   1 |           pp512 |        119.48 ± 1.09 |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |   1 |          pp8192 |        113.36 ± 3.61 |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |   1 |           tg128 |          7.83 ± 0.13 |

build: 8e7f3c017 (9898)
DS4_14_RC=0
