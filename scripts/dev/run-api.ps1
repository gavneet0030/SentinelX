Write-Host "Starting SentinelX API..." -ForegroundColor Cyan

if (-not (Test-Path ".venv")) {
    Write-Host "Virtual environment not found." -ForegroundColor Red
    exit 1
}

.\.venv\Scripts\Activate.ps1

python -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
