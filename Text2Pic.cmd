@echo off
setlocal enableextensions

set text_file=%~1
D:\Python27\python.exe Text2Pic.py %text_file%

rem if "%text_file%" == "" (
rem   echo "Input your text file path."
rem ) else (
rem   echo D:\Python27\python.exe Text2Pic.py %text_file%
rem   D:\Python27\python.exe Text2Pic.py %text_file%
rem )

echo --------------------The End--------------------
pause