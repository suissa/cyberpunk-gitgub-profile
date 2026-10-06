#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"
PROFILE="${1:-$ROOT/examples/marie-curie/profile.json}"
OUTPUT="${2:-$ROOT/generated-profile}"
shift 2 2>/dev/null || true
exec "$PYTHON" "$ROOT/scripts/profile_generator.py" "$PROFILE" --output "$OUTPUT" --validate "$@"
