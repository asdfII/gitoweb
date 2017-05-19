@echo off
git add -A
set gitdiff=git diff --cached --name-only
%gitdiff% >>win_gitdiff.tmp
set /p readdiff=<win_gitdiff.tmp
del /q /f win_gitdiff.tmp
git commit -m "Ticket %username%@%computername% %date:~0,4%%date:~5,2%%date:~8,2%0%time:~1,1%%time:~3,2%%time:~6,2% %readdiff%"
git push origin dev
