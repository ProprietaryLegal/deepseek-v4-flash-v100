# DS4 rotation-fix live 4-cell matrix — 2026-07-07T05:24:34Z
Build: build-ds4fix @ c57d18583 · GPU 12 · -ngl 999 -ot exps=CPU -fa 1 -c 4096 · temp 0

| K | V | output (first tokens) | tg t/s |
|---|---|---|---:|
| q8_0 | q8_0 | ` Paris.",     "label": "1" } ` | 8.35 |
| f16 | f16 | ` Paris. The capital of France is Paris. The capital of` | 7.62 |
| q8_0 | f16 | ` Paris.",     "label": "1" } ` | 7.67 |
| f16 | q8_0 | ` Paris. The capital of France is Paris. The capital of` | 7.53 |

MATRIX_COMPLETE_V2 2026-07-07T05:24:34Z
