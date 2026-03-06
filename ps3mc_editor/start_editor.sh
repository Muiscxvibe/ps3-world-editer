#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$APP_DIR/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "[PS3MC] Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

"$PYTHON_BIN" -m pip install --quiet --upgrade pip
"$PYTHON_BIN" -m pip install --quiet PySide6 nbtlib

if [[ "${1:-}" == "--check" ]]; then
  "$PYTHON_BIN" -c "import PySide6, nbtlib; print('Dependencies OK')"
  exit 0
fi

if [[ -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
  echo "[PS3MC] No graphical display detected (DISPLAY/WAYLAND_DISPLAY not set)."
  echo "[PS3MC] Run this from your Linux desktop session."
  exit 1
fi

exec "$PYTHON_BIN" "$APP_DIR/main.py"
