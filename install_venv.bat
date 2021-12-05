@echo OFF
title Install Virtual Enviroment

setlocal
set "psCommand="(new-object -COM 'Shell.Application')^
.BrowseForFolder(0,'Please choose python path.',0,0).self.path""
for /f "usebackq delims=" %%I in (`powershell %psCommand%`) do set "py_path=%%I/python.exe"

setlocal enabledelayedexpansion
echo Creating virtual enviroment base by !py_path!
%py_path% -m venv ./env
endlocal

echo Activate virtual enviroment 
call .\env\Scripts\activate.bat

echo Installing modules from requirements.txt 
pip install -r requirements.txt

pause