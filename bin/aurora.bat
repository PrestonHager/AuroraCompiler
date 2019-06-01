@echo off
set args=%*
call set args=%%args:*%1=%%
set argCount=0
for %%a in (%*) do (
  set /A argCount+=1
)

if %argCount% LSS 1 (python %~dp0compiler.py -h) else (python %~dp0compiler.py %1 %args%)
