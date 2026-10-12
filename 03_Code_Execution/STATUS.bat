@echo off
REM Kullanim: STATUS.bat pilot   veya   STATUS.bat full   (varsayilan: full)
cd /d "%~dp0"
set PROFILE=%1
if "%PROFILE%"=="" set PROFILE=full
python run_full_campaign.py status --profile %PROFILE%
python run_full_campaign.py verify --profile %PROFILE%
pause
