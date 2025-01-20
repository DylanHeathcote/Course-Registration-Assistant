@echo off
REM Get the current directory (project root)
set PROJECT_ROOT=%~dp0

REM Remove trailing backslash
set PROJECT_ROOT=%PROJECT_ROOT:~0,-1%

REM Add to PYTHONPATH
set PYTHONPATH=%PROJECT_ROOT%;%PYTHONPATH%

REM Confirm PYTHONPATH
echo PYTHONPATH set to: %PYTHONPATH%
