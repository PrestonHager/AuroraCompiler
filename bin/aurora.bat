@echo off
set args=%*
call set args=%%args:*%1=%%
set argCount=0
for %%a in (%*) do (
  set /A argCount+=1
)

if %argCount% LSS 1 (echo "Usage: aurora [filename] [optional flags]") else (python3 %~dp0compiler.py %1 %args%)
