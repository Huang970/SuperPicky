@echo off
chcp 65001 >nul
cd /d "%~dp0"
setlocal EnableExtensions EnableDelayedExpansion

echo ==============================================
echo  Build Start
echo ==============================================

REM Auto activate venv
call ".venv\Scripts\activate.bat"

set "PYTHON_EXE=python"
set "APP_NAME=SuperPicky"
set "SPEC_FILE=SuperPicky_win64.spec"
set "ROOT_DIR=%~dp0"
set "ROOT_DIR=%ROOT_DIR:~0,-1%"

echo [Step 0] Clean old files
rd /s /q "%ROOT_DIR%\build_dist" 2>nul
rd /s/q "%ROOT_DIR%\dist" 2>nul

echo [Step 1] Check environment
if not exist "%SPEC_FILE%" (
    echo ERROR: spec not found
    pause
    exit /b 1
)

echo [Step 2] Start build
"%PYTHON_EXE%" -m PyInstaller "%SPEC_FILE%" --clean --noconfirm

if exist "%ROOT_DIR%\dist\SuperPicky\SuperPicky.exe" (
    echo ==============================================
    echo  Build Success !
    echo ==============================================
) else (
    echo Build Failed
    pause
)

endlocal
pause
exit /b 0