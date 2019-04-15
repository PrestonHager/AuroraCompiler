@echo off
set cmdargs=-s
for %%G in (%*) do (
  if %%G == -r set cmdargs=%cmdargs% --run
  if %%G == --run set cmdargs=%cmdargs% --run
)
python %~p0/compiler.py %1 %cmdargs%
