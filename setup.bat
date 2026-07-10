@echo off
chcp 65001 >nul
echo ================================================
echo   London Project — Complete Setup
echo ================================================

if not exist .env (
    copy .env.example .env
    echo [1] Created .env from .env.example
)

echo [2] Installing Python packages...
pip install -r requirements.txt --quiet

echo [3] Running Django setup ^(migrate + demo + images^)...
python manage.py full_setup

echo.
echo   Quick start:  python manage.py runserver
echo ================================================
pause
