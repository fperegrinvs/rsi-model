# Python quality baseline

This record captures the repository immediately before the PEP 621 and
locked-`uv` migration on 2026-07-28. It is evidence for the migration ratchet,
not an accepted error baseline or a source of permanent suppressions.

Tool versions:

- Python 3.13.0
- uv 0.9.18
- Ruff 0.16.0
- Pyright 1.1.411
- Coverage.py 7.15.2

Results:

| Gate | Initial result |
|---|---:|
| `ruff check src scripts tests --statistics` | 204 errors |
| `pyright` before project-aware dependency resolution | 209 errors, 13 warnings |
| pytest with `--strict-config --strict-markers -W error` | 183 passed, 0 warnings |
| branch coverage over `src/rsimodel` | 85% |
| sdist/wheel build | unavailable: no build metadata existed |
| isolated wheel import and CLI check | unavailable: no wheel existed |

The Pyright count includes unresolved third-party imports because the
repository had neither project metadata nor a type-checker environment
configuration. The post-sync count must be measured again; dependency
resolution is not evidence that the remaining diagnostics were fixed.

Coverage was measured with:

```sh
uv run --no-project --with pytest-cov --with pytest-timeout \
  python -m pytest tests -q --strict-config --strict-markers -W error \
  --cov=src/rsimodel --cov-branch --cov-report=term-missing
```

The initial branch-coverage results for load-bearing modules were:

| Module | Coverage |
|---|---:|
| `model.py` | 95% |
| `lco.py` | 96% |
| `integrated.py` | 94% |
| `integrated_analysis.py` | 90% |
| `provenance.py` | 72% |
| `release.py` | 78% |
| `manifests.py` | 74% |

The aggregate floor begins at 85%. Future changes should raise both the
aggregate floor and the weaker load-bearing module floors through tests of
behavior and invariants, not by omitting difficult modules.
