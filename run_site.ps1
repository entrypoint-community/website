if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Output "Starting EntryPoint site server on port 8080: http://localhost:8080/frontend/posts.html"
    python -m http.server 8080
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    Write-Output "Starting EntryPoint site server on port 8080: http://localhost:8080/frontend/posts.html"
    python3 -m http.server 8080
} else {
    Write-Output "Neither python nor python3 is installed."
}
