@echo off
setlocal
cd /d "%~dp0"
py -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo Wait till Pillow is downloaded
    py -m pip install --user Pillow
    if errorlevel 1 (
        echo.
        echo Install Python 3 is required
        pause
        exit /b 1
    )
)
py "%~dp0FastConvert.py"
if errorlevel 1 (
    echo.
    echo the tool couldn't start correctly
    pause
)
