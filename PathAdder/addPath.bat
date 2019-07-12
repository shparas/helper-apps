@echo off

:: addPath

if [%1]==[-help] goto :HELP
if [%1]==[-h] goto :HELP
if [%1]==[--help] goto :HELP
if [%1]==[/?] goto :HELP
goto :START

:START
:: start "" /i "%ProgramFiles(x86)%\myFile.exe" %*
:: @"C:\MongoDB\Server\4.0\bin\mongo.exe" %*
(echo @"%~2" %%*) > C:/PathApps/%1.bat 
goto :EOF

:HELP
echo ----------------------------------
echo addPath - A Path Adder Program
echo Adds something to the current Path
echo ----------------------------------
echo .
echo Usage :
echo.
echo addPath --help : This help message
echo addPath -h : This help message
echo.
echo addPath name "FilePath" : Adds FilePath as name
echo.
echo Examples:
echo addPath python3 "C:/Python3/python.exe"
echo addPath pip3 C:/Python3/pip/pip.exe
echo addPath python2 "C:/Program Files/Python/python.exe"
echo.
goto :EOF

::@echo off
:::: Notepad++ execution
::if [%1]==[-h] goto :HELP
::if [%1]==[--help] goto :HELP
::goto :START
:::START
::start "" /i "%ProgramFiles(x86)%\notepad++\notepad++.exe" %*
::goto :EOF

:::HELP
::echo Notepad++ Command Argument Help
::echo -------------------------------
::echo Usage :
::echo.
::echo notepad++ [--help] [-multiInst] [-noPlugins] [-lLanguage] [-nLineNumber] [-cColumnNumber] [-xPos] [-yPos] [-nosession] [-notabbar] [-ro] [-systemtray] [-loadingTime] [fullFilePathName]
::echo.
::echo     --help : This help message
::echo     -multiInst : Launch another Notepad++ instance
::echo     -noPlugins : Launch Notepad++ without loading any plugin
::echo.
::goto :EOF
:::EOF

:EOF
