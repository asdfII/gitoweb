@echo off
git add -A
set gitdiff=git diff --cached --name-only
git commit -m "Ticket %username%@%computername% %date:~0,4%%date:~5,2%%date:~8,2%0%time:~1,1%%time:~3,2%%time:~6,2% %gitdiff%"
git push origin dev
