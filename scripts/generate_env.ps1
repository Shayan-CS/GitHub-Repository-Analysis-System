Param()
if (Test-Path -Path .env) {
    Write-Host ".env already exists - leaving it alone"
    exit 0
}

if (-not (Test-Path -Path .env.example)) {
    Write-Host ".env.example not found - create one first"
    exit 1
}

Copy-Item -Path .env.example -Destination .env
Write-Host "Created .env from .env.example. Edit .env to add secrets before running docker compose."
