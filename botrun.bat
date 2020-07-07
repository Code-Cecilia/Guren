@echo off
python botstart.py
for /L %%n in (1,2,3,4,5) do echo %%n
echo rebooting the bot
pause
goto begin
