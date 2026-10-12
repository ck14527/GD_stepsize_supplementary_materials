#!/usr/bin/env bash
# Compatibility entry point: this bundle contains no manuscript LaTeX source.
# Run the lightweight package checks; Lean compilation is documented separately.
set -euo pipefail
cd "$(dirname "$0")/.."
if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo 'Python 3.10 or newer is required.' >&2
  exit 1
fi
"$PYTHON" scripts/verify_project.py --numerical "$@"
