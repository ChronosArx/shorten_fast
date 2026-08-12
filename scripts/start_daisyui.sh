#!/bin/sh
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$(dirname "$SCRIPT_DIR")" && pwd)"

"$PROJECT_DIR"/static/daisyui/tailwindcss -i "$PROJECT_DIR"/static/daisyui/input.css -o "$PROJECT_DIR"/static/daisyui/output.css --watch