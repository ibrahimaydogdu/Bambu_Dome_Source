@echo off
REM Genel kosu: 30 tohum x 3 model x 16 algoritma = 1440 is. Sonuclar C:\BambuDome_campaign\full
REM Ayni komut yarim kalan kampanyayi kaldigi yerden surdurur.
cd /d "%~dp0"
python run_full_campaign.py dry-run --profile full
python run_full_campaign.py preflight --profile full
if errorlevel 1 (
  echo.
  echo ON KONTROL BASARISIZ - kampanya baslatilmadi.
  pause
  exit /b 1
)
choice /M "Genel kampanya baslatilsin mi"
if errorlevel 2 exit /b 0
python run_full_campaign.py start --profile full --skip-preflight --background
echo.
echo Genel kosu arka planda baslatildi. Ilerleme icin STATUS.bat full, durdurmak icin PAUSE.bat full
pause
