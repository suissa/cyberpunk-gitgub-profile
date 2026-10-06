#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"
PROFILE="${1:-$ROOT/examples/marie-curie/profile.json}"
if (($# > 0)); then shift; fi
OUTPUT="${1:-$ROOT/generated-profile}"
if (($# > 0)); then shift; fi
exec "$PYTHON" "$ROOT/scripts/profile_generator.py" "$PROFILE" --output "$OUTPUT" --validate "$@"
