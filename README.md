# Coverity JSON to SARIF

Convert Coverity `cov-format-errors` JSON results to SARIF 2.1.0.

Requires Python 3.7 or newer.

## Install

```powershell
python -m pip install .
```

## Use

```powershell
coverity-to-sarif input.json output.sarif
```

Or run it as a module:

```powershell
python -m coverity_sarif input.json output.sarif
```

## Build

```powershell
python setup.py sdist bdist_wheel
```

Licensed under GPL-3.0-only; see [LICENSE](LICENSE).