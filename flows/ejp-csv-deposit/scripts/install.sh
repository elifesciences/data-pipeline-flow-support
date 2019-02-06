#!/bin/bash
set -e # everything must succeed.
echo "[-] install.sh"

. mkvenv.sh

source venv/bin/activate

pip install -r requirements.lock --no-cache-dir

echo "[✓] install.sh"
