@echo off
set cmdargs=
for %%G in (%*) do (
  if %%G == -r set cmdargs=%cmdargs% --run
  if %%G == --run set cmdargs=%cmdargs% --run
)
set argCount=0
for %%x in (%*) do Set /A argCount+=1

if %argCount% LSS 1 (echo "Usage: aurora [filename] [optional flags]") else (python %~dp0compiler.py %1 %cmdargs%)
