#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/draw_scenes.py
python3 scripts/generate_materials.py
python3 scripts/generate_audio.py
