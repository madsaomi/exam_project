#!/bin/bash
set -e

echo "================================================"
echo "  London Project — Complete Setup"
echo "================================================"

# 1. Environment
if [ ! -f .env ]; then
    cp .env.example .env
    echo "[1] Created .env from .env.example"
fi

# 2. Python dependencies
echo "[2] Installing Python packages..."
pip install -r requirements.txt --quiet

# 3. Run Django full setup
echo "[3] Running Django setup (migrate + demo + images)..."
python manage.py full_setup

echo ""
echo "  Quick start:  python manage.py runserver"
echo "================================================"
