# Launch backend (FastAPI) and frontend (Vite) in separate windows.
# Usage:  ./start.ps1
$root = $PSScriptRoot

if (-not (Test-Path "$root/.venv")) {
  Write-Host "Creating virtualenv (Python 3.11)..."
  py -3.11 -m venv "$root/.venv"
  & "$root/.venv/Scripts/python.exe" -m pip install -r "$root/requirements.txt"
  & "$root/.venv/Scripts/python.exe" -m ml.train_models
}

if (-not (Test-Path "$root/frontend/node_modules")) {
  Write-Host "Installing frontend dependencies..."
  Push-Location "$root/frontend"; npm install; Pop-Location
}

Write-Host "Starting backend on http://localhost:8000 ..."
Start-Process powershell -ArgumentList "-NoExit", "-Command",
  "cd `"$root`"; .\.venv\Scripts\Activate.ps1; uvicorn backend.main:app --reload --port 8000"

Write-Host "Starting frontend on http://localhost:5173 ..."
Start-Process powershell -ArgumentList "-NoExit", "-Command",
  "cd `"$root/frontend`"; npm run dev"

Write-Host "Backend:  http://localhost:8000/docs"
Write-Host "Frontend: http://localhost:5173"
