# Run script for a2a-mini-1-basic-communication
# Supports both uv and traditional Python

Write-Host "🚀 Running A2A Code Review System..." -ForegroundColor Green
Write-Host ""

# Check if uv is available
$uvAvailable = Get-Command uv -ErrorAction SilentlyContinue

if ($uvAvailable) {
    Write-Host "✨ Using uv (fast mode)" -ForegroundColor Cyan
    uv run python main.py
} else {
    Write-Host "⚙️  Using traditional Python" -ForegroundColor Yellow
    $env:PYTHONPATH = $PSScriptRoot
    python main.py
}


