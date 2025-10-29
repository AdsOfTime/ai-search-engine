# Check if we're in a git repository
if (!(Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit - AI Search Engine"
}

# Add any changes
Write-Host "Adding changes to Git..." -ForegroundColor Green
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    git commit -m "Add Cloudflare deployment configuration and build optimizations"
    Write-Host "Changes committed successfully!" -ForegroundColor Green
    
    # Check if origin exists
    $remotes = git remote
    if ($remotes -notcontains "origin") {
        Write-Host "Please add your GitHub repository as origin:" -ForegroundColor Yellow
        Write-Host "git remote add origin https://github.com/yourusername/your-repo-name.git" -ForegroundColor Cyan
        Write-Host "git branch -M main" -ForegroundColor Cyan
        Write-Host "git push -u origin main" -ForegroundColor Cyan
    } else {
        Write-Host "Pushing to GitHub..." -ForegroundColor Green
        git push origin main
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Successfully pushed to GitHub!" -ForegroundColor Green
        }
    }
} else {
    Write-Host "No changes to commit." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Green
Write-Host "1. Go to https://dash.cloudflare.com/pages" -ForegroundColor White
Write-Host "2. Click 'Create a project'" -ForegroundColor White
Write-Host "3. Connect your GitHub repository" -ForegroundColor White
Write-Host "4. Use these build settings:" -ForegroundColor White
Write-Host "   - Build command: npm run build" -ForegroundColor Cyan
Write-Host "   - Build output directory: build" -ForegroundColor Cyan
Write-Host "   - Root directory: frontend" -ForegroundColor Cyan
Write-Host "   - Node.js version: 18" -ForegroundColor Cyan
Write-Host ""
Write-Host "Environment Variables to set in Cloudflare Pages:" -ForegroundColor Yellow
Write-Host "   REACT_APP_API_URL=https://ai-search-backend.dnash29.workers.dev/api" -ForegroundColor Cyan
Write-Host "   REACT_APP_ENVIRONMENT=production" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your backend is already live at:" -ForegroundColor Green
Write-Host "https://ai-search-backend.dnash29.workers.dev/api" -ForegroundColor Cyan