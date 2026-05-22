@echo off
cd /d "%~dp0"
setlocal EnableExtensions EnableDelayedExpansion

set "SCRIPT_ROOT=%~dp0"
set "SCRIPT_ROOT=%SCRIPT_ROOT:~0,-1%"

echo ==============================================
echo Build Start
echo Path: %SCRIPT_ROOT%
echo User: %USERNAME%
echo ==============================================

if "%USERNAME%"=="Mac" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=%~dp0.venv_pack\Scripts\python.exe"
)

echo Python: %PYTHON_EXE%
echo.

if not exist "%PYTHON_EXE%" (
    echo ERROR: Python not found
    pause
    exit /b 1
)

set "APP_NAME=SuperPicky"
set "SPEC_FILE=SuperPicky_win64.spec"
set "ROOT_DIR=%~dp0"
set "ROOT_DIR=%ROOT_DIR:~0,-1%"
cd /d "!SCRIPT_ROOT!"

set "VERSION_ARG="
set "ZIP_COPY_DIR="
set "OUT_DIST_DIR=dist"
set "BUILD_ZIP=0"

call :parse_args %*
if errorlevel 1 exit /b 1
goto :start

:parse_args
:parse_args_loop
if "%~1"=="" exit /b 0
if /i "%~1"=="--help" (exit /b 0)
if /i "%~1"=="-h" (exit /b 0)
if "%VERSION_ARG%"=="" (
    set "VERSION_ARG=%~1"
) else if "%ZIP_COPY_DIR%"=="" (
    set "ZIP_COPY_DIR=%~1"
)
shift
goto :parse_args_loop

:start
echo.
echo [Step 0] Clean old files
set "INNO_DIR=%ROOT_DIR%\inno"

rd /s /q "%ROOT_DIR%\build_dist" 2>nul
rd /s /q "%ROOT_DIR%\build_dist_cpu" 2>nul
rd /s /q "%ROOT_DIR%\build_dist_cuda" 2>nul
rd /s /q "%ROOT_DIR%\dist" 2>nul
rd /s /q "%ROOT_DIR%\dist_cpu" 2>nul
rd /s /q "%ROOT_DIR%\dist_cuda" 2>nul
rd /s /q "%ROOT_DIR%\output" 2>nul

echo.
echo [Step 1] Check environment
if not exist "%SPEC_FILE%" (
    echo ERROR: spec missing
    exit /b 1
)

call :check_python "%PYTHON_EXE%"
if errorlevel 1 exit /b 1

echo.
echo [Step 2] Resolve version
set "VERSION=4.0.5_sp3"
if not "%VERSION_ARG%"=="" (
    set "VERSION=%VERSION_ARG%"
)

echo.
echo [Step 3] Update build info
set "COMMIT_HASH=unknown"
for /f "tokens=*" %%i in ('git rev-parse --short HEAD 2^>nul') do set "COMMIT_HASH=%%i"

set "BUILD_INFO_FILE=!SCRIPT_ROOT!\core\build_info.py"
set "BUILD_INFO_BACKUP=core\build_info.py.backup"
if exist "%BUILD_INFO_FILE%" copy /y "%BUILD_INFO_FILE%" "%BUILD_INFO_BACKUP%" >nul

powershell -NoProfile -Command "(Get-Content -Path '%BUILD_INFO_FILE%' -Raw -Encoding UTF8) -replace 'COMMIT_HASH\s*=\s*.*', 'COMMIT_HASH = \"%COMMIT_HASH%\"' | Set-Content -Path '%BUILD_INFO_FILE%' -Encoding UTF8"

echo.
echo [Step 4] Build
call :build_single
call :restore_build_info >nul

echo.
echo ==============================================
echo Build finished
echo ==============================================
echo EXE: %ROOT_DIR%\dist\SuperPicky\SuperPicky.exe
echo ZIP: skipped
echo.

endlocal
pause
exit /b 0

:check_python
"%~1" -c "import sys; import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python or PyInstaller invalid
    exit /b 1
)
exit /b 0

:build_single
set "WORK_DIR=%ROOT_DIR%\build_dist"
set "DIST_DIR=%ROOT_DIR%\dist"
"%PYTHON_EXE%" -m PyInstaller "%SPEC_FILE%" --clean --noconfirm --workpath "%WORK_DIR%" --distpath "%DIST_DIR%"
if not exist "%DIST_DIR%\%APP_NAME%\SuperPicky.exe" (
    echo ERROR: Build failed
    exit /b 1
)
exit /b 0

:restore_build_info
if exist "%BUILD_INFO_BACKUP%" move /y "%BUILD_INFO_BACKUP%" "%BUILD_INFO_FILE%" >nul
exit /b 0