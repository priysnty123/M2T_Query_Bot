#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Install all your dependencies
pip install -r requirements.txt

# 2. Run your new download script
python download_model.py