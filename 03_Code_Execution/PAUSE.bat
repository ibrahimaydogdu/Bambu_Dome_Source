@echo off
REM Kullanim: PAUSE.bat pilot   veya   PAUSE.bat full   (varsayilan: full)
REM Devam etmek icin ilgili RUN_*.bat dosyasini yeniden calistirin.
cd /d "%~dp0"
set PROFILE=%1
if "%PROFILE%"=="" set PROFILE=full
python run_full_campaign.py pause --profile %PROFILE%
pause
