@echo off
REM BambuDome - Gozetimsiz optimizasyon kampanyasi
REM Cift tiklayin veya parametre verin:  RUN_CAMPAIGN.bat --runs 2 --gen 5
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
python -m pip install --quiet comtypes numpy pandas scipy matplotlib
python run_campaign.py %*
echo.
echo Kampanya sona erdi. Sonuclar: results\   Gunluk: logs\campaign.log
pause
