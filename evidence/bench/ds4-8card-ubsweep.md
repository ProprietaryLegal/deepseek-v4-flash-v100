ggml_cuda_init: found 8 CUDA devices (Total VRAM: 259953 MiB):
  Device 0: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 1: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 2: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 3: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 4: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 5: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 6: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
  Device 7: Tesla V100-SXM2-32GB, compute capability 7.0, VMM: yes, VRAM: 32494 MiB
| model                          |       size |     params | backend    | ngl | n_ubatch |  fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | --: | --------------: | -------------------: |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |      256 |   1 |          pp8192 |        183.07 ± 1.39 |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |      256 |   1 |            tg64 |         12.26 ± 0.19 |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |      512 |   1 |          pp8192 |        200.88 ± 3.69 |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |      512 |   1 |            tg64 |         12.29 ± 0.16 |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |     1024 |   1 |          pp8192 |        205.40 ± 2.14 |
| deepseek4 ?B MXFP4 MoE         | 144.44 GiB |   284.33 B | CUDA       | 999 |     1024 |   1 |            tg64 |         12.89 ± 0.07 |

build: 8e7f3c017 (9898)
DS4_UB_RC=0
