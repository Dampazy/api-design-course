#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Backend: pytest ==="
cd "$ROOT_DIR/backend"
source venv/bin/activate
pytest tests/ -v

echo
echo "=== Frontend: Playwright smoke tests ==="
cd "$ROOT_DIR/frontend"

BACKEND_PID=""
FRONTEND_PID=""
cleanup() {
  [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null || true
  [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null || true
}
trap cleanup EXIT

if ! curl -s -o /dev/null http://127.0.0.1:8000/api/health; then
  (cd "$ROOT_DIR/backend" && source venv/bin/activate && uvicorn app.main:app --port 8000 &)
  BACKEND_PID=$!
  sleep 2
fi

if ! curl -s -o /dev/null http://localhost:5173/; then
  npm run dev &
  FRONTEND_PID=$!
  sleep 3
fi

npx playwright test

echo
echo "All tests passed."
