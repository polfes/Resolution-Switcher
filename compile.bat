@echo off
title Compile Resolution Switcher
echo ========================================
echo   Compiling Resolution Switcher
echo ========================================
echo.

:: Find any .ico file
set ICON_FILE=
for %%f in (*.ico) do (
    set ICON_FILE=%%f
    goto :found
)

:found
if defined ICON_FILE (
    echo [OK] Icon found: %ICON_FILE%
    set ICON_PARAM=--icon="%ICON_FILE%"
) else (
    echo [WARNING] No .ico file found!
    set ICON_PARAM=
)

:: Install pyinstaller if needed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    echo.
)

:: Clean previous builds
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "*.spec" del /q *.spec

:: Compile
echo Compiling...
pyinstaller --onefile --name "ResolutionSwitcher" %ICON_PARAM% --uac-admin resolution_switcher.py

if errorlevel 1 (
    echo.
    echo [ERROR] Compilation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] Compilation completed!
echo ========================================
echo Executable created: dist\ResolutionSwitcher.exe
echo.
pause