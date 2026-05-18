param(
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 5173,
    [switch]$SkipInstall,
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"

$RootDir = $PSScriptRoot
$BackendDir = Join-Path $RootDir "backend"
$FrontendDir = Join-Path $RootDir "frontend"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Test-PortInUse {
    param([int]$Port)
    return [bool](Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue)
}

function Assert-PortAvailable {
    param([int]$Port, [string]$Name)
    if (Test-PortInUse $Port) {
        throw "$Name port $Port is already in use. Stop the existing process or pass another port."
    }
}

function Assert-Command {
    param([string]$CommandName)
    if (-not (Get-Command $CommandName -ErrorAction SilentlyContinue)) {
        throw "$CommandName is not available in PATH."
    }
}

function Ensure-BackendDependencies {
    if ($SkipInstall) {
        return
    }

    Push-Location $BackendDir
    try {
        python -c "import fastapi, uvicorn" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Step "Installing backend dependencies"
            python -m pip install -r requirements.txt
        }
    }
    finally {
        Pop-Location
    }
}

function Ensure-FrontendDependencies {
    if ($SkipInstall) {
        return
    }

    $NodeModulesDir = Join-Path $FrontendDir "node_modules"
    if (-not (Test-Path $NodeModulesDir)) {
        Write-Step "Installing frontend dependencies"
        Push-Location $FrontendDir
        try {
            npm.cmd install
        }
        finally {
            Pop-Location
        }
    }
}

Assert-Command "python"
Assert-Command "npm.cmd"
Assert-PortAvailable $BackendPort "Backend"
Assert-PortAvailable $FrontendPort "Frontend"

Ensure-BackendDependencies
Ensure-FrontendDependencies

if ($CheckOnly) {
    Write-Step "Preflight OK"
    Write-Host "Backend:  http://127.0.0.1:$BackendPort"
    Write-Host "Frontend: http://127.0.0.1:$FrontendPort"
    exit 0
}

Write-Step "Starting Athena dev stack"

$BackendJob = Start-Job -Name "athena-backend" -ScriptBlock {
    param($BackendDir, $BackendPort, $FrontendPort)
    Set-Location $BackendDir
    $env:BACKEND_CORS_ORIGINS = "http://localhost:$FrontendPort,http://127.0.0.1:$FrontendPort"
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port $BackendPort
} -ArgumentList $BackendDir, $BackendPort, $FrontendPort

$FrontendJob = Start-Job -Name "athena-frontend" -ScriptBlock {
    param($FrontendDir, $FrontendPort, $BackendPort)
    Set-Location $FrontendDir
    $env:VITE_API_BASE_URL = "http://127.0.0.1:$BackendPort"
    npm.cmd run dev -- --host 127.0.0.1 --port $FrontendPort
} -ArgumentList $FrontendDir, $FrontendPort, $BackendPort

try {
    Write-Host "Backend:  http://127.0.0.1:$BackendPort"
    Write-Host "API docs: http://127.0.0.1:$BackendPort/docs"
    Write-Host "Frontend: http://127.0.0.1:$FrontendPort"
    Write-Host ""
    Write-Host "Press Ctrl+C to stop both servers." -ForegroundColor Yellow

    while ($true) {
        foreach ($Job in @($BackendJob, $FrontendJob)) {
            Receive-Job -Job $Job | ForEach-Object {
                Write-Host "[$($Job.Name)] $_"
            }

            if ($Job.State -in @("Failed", "Stopped", "Completed")) {
                Receive-Job -Job $Job
                throw "$($Job.Name) stopped with state $($Job.State)."
            }
        }

        Start-Sleep -Seconds 1
    }
}
finally {
    Write-Step "Stopping Athena dev stack"
    Stop-Job -Job $BackendJob, $FrontendJob -ErrorAction SilentlyContinue
    Remove-Job -Job $BackendJob, $FrontendJob -Force -ErrorAction SilentlyContinue
}
