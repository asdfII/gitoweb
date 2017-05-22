git add -A
$date = Get-Date -f "yyyyMMddHHmmss"
git commit -m "Ticket $env:username@$env:computername $date`n$(git diff --cached --name-only)"
git push origin dev
