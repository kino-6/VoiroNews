@echo off
REM Check if a keyword argument is provided
if "%~1"=="" (
    echo [NG] Please provide a search keyword.
    echo Usage: run.bat [keyword]
    exit /b 1
)

REM Join all arguments into a single quoted string
setlocal enabledelayedexpansion
set "args="
:loop
if "%~1"=="" goto done
set "args=!args! %~1"
shift
goto loop
:done

REM Trim leading space
set "args=%args:~1%"

REM Wrap the joined arguments in quotes
cd src
uv run main.py "%args%"
cd ..
