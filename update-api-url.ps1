# Script to update API URL for production deployment

param(
    [Parameter(Mandatory=$true)]
    [string]$BackendUrl
)

Write-Host "Updating API URLs to: $BackendUrl" -ForegroundColor Green

# Update Home.jsx
$homeFile = "frontend\src\pages\Home.jsx"
(Get-Content $homeFile) -replace "const API_URL = 'http://127.0.0.1:8000'", "const API_URL = '$BackendUrl'" | Set-Content $homeFile
Write-Host "✓ Updated $homeFile" -ForegroundColor Green

# Update ProductDetail.jsx  
$detailFile = "frontend\src\pages\ProductDetail.jsx"
(Get-Content $detailFile) -replace "const API_URL = 'http://127.0.0.1:8000'", "const API_URL = '$BackendUrl'" | Set-Content $detailFile
Write-Host "✓ Updated $detailFile" -ForegroundColor Green

# Update ChatInterface.jsx
$chatFile = "frontend\src\components\ChatInterface.jsx"
(Get-Content $chatFile) -replace "const API_URL = 'http://127.0.0.1:8000'", "const API_URL = '$BackendUrl'" | Set-Content $chatFile
Write-Host "✓ Updated $chatFile" -ForegroundColor Green

Write-Host "`nDone! Now run:" -ForegroundColor Yellow
Write-Host "  git add ." -ForegroundColor Cyan
Write-Host "  git commit -m 'Update API URL for production'" -ForegroundColor Cyan
Write-Host "  git push" -ForegroundColor Cyan
