function Start-EntryPoint {
    param (
        [string]$pythonCommand
    )

    Write-Output "Starting EntryPoint site server on port 8080: http://localhost:8080/posts.html"
    
    # Start the frontend server
    $frontendJob = Start-Job -ScriptBlock {
        param ($pythonCommand)
        & $pythonCommand -m http.server 8080 -d frontend
    } -ArgumentList $pythonCommand

    # Install Flask and start the backend server
    & $pythonCommand -m pip install flask
    $backendJob = Start-Job -ScriptBlock {
        param ($pythonCommand)
        & $pythonCommand backend/api.py
    } -ArgumentList $pythonCommand

    # Open the browser
    Start-Process "http://localhost:8080/posts.html"

    # Wait for Ctrl+C
    try {
        Write-Output "Press Ctrl+C to stop the servers..."
        Wait-Job -Any
    } finally {
        Write-Output "Stopping the servers..."
        Stop-Job $frontendJob
        Stop-Job $backendJob
        Remove-Job $frontendJob
        Remove-Job $backendJob
    }
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    Start-EntryPoint -pythonCommand "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    Start-EntryPoint -pythonCommand "python3"
} else {
    Write-Output "Neither python nor python3 is installed."
}
