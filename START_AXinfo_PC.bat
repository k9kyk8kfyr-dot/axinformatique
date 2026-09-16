@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul 2>&1
where py >nul 2>&1
if %errorlevel%==0 goto USE_PY
where python >nul 2>&1
if %errorlevel%==0 goto USE_PYTHON

echo.
echo [ERROR] Python 3 was not found.
echo Install Python 3 from python.org, then run this file again.
echo.
pause
exit /b 1

:USE_PY
py -3 AXinfo_PC_Bridge.py
goto END

:USE_PYTHON
python AXinfo_PC_Bridge.py

:END
echo.
pause
