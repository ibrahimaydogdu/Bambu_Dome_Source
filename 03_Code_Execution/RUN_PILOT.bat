@echo off
REM Pilot kosu: 1 tohum x 3 model x 16 algoritma = 48 is (~3-4 dk). Sonuclar C:\BambuDome_campaign\pilot
cd /d "%~dp0"
python run_full_campaign.py dry-run --profile pilot
python run_full_campaign.py preflight --profile pilot
if errorlevel 1 (
  echo.
  echo ON KONTROL BASARISIZ - kampanya baslatilmadi.
  pause
  exit /b 1
)
python run_full_campaign.py start --profile pilot --skip-preflight --background
echo.
echo Pilot arka planda baslatildi. Ilerleme icin STATUS.bat pilot, durdurmak icin PAUSE.bat pilot
pause
