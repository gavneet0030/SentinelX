Write-Host "Running SentinelX test suite..." -ForegroundColor Cyan

.\.venv\Scripts\Activate.ps1

python -m pytest -v
