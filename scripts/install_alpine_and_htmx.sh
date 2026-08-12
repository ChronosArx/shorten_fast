#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$(dirname "$SCRIPT_DIR")" && pwd)"

mkdir -p "$PROJECT_DIR"/static
mkdir -p "$PROJECT_DIR"/static/js
mkdir -p "$PROJECT_DIR"/static/daisyui

curl https://cdn.jsdelivr.net/npm/htmx.org@2.0.10/dist/htmx.min.js -o "$PROJECT_DIR"/static/js/htmx.min.js
curl https://cdn.jsdelivr.net/npm/alpinejs@3.16.1/dist/cdn.min.js -o "$PROJECT_DIR"/static/js/alpine.min.js

cd "$PROJECT_DIR"/static/daisyui && curl -sL daisyui.com/fast | bash

