# Cloudflare Deployment Script for AI Search Engine (PowerShell)
# Run this script to deploy both frontend and backend to Cloudflare

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("full", "backend", "frontend", "database", "migrate")]
    [string]$DeploymentType = "full"
)

# Function to check if a command exists
function Test-CommandExists {
    param($Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Function to write colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

Write-ColorOutput "🚀 Starting Cloudflare deployment for AI Search Engine..." "Green"

# Check if wrangler is installed
if (-not (Test-CommandExists "wrangler")) {
    Write-ColorOutput "❌ Wrangler CLI not found. Installing..." "Red"
    npm install -g wrangler
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput "Failed to install Wrangler CLI" "Red"
        exit 1
    }
}

# Check authentication
Write-ColorOutput "🔐 Checking Cloudflare authentication..." "Yellow"
$authCheck = wrangler whoami 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-ColorOutput "Please login to Cloudflare..." "Yellow"
    wrangler login
}

# Function to create D1 database
function New-D1Database {
    Write-ColorOutput "📊 Setting up Cloudflare D1 database..." "Yellow"
    
    try {
        $dbResult = wrangler d1 create ai-search-db --output json | ConvertFrom-Json
        $databaseId = $dbResult.id
        
        if ($databaseId) {
            Write-ColorOutput "✅ Database created with ID: $databaseId" "Green"
            
            # Update wrangler.toml
            if (Test-Path "wrangler.toml") {
                (Get-Content "wrangler.toml") -replace "your-d1-database-id", $databaseId | Set-Content "wrangler.toml"
                Write-ColorOutput "✅ Updated wrangler.toml with database ID" "Green"
            }
            
            # Apply schema
            Write-ColorOutput "📋 Applying database schema..." "Yellow"
            wrangler d1 execute ai-search-db --file=cloudflare-d1-schema.sql
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput "✅ Database schema applied" "Green"
            }
        }
    }
    catch {
        Write-ColorOutput "❌ Failed to create D1 database" "Red"
        $databaseId = Read-Host "Enter your D1 database ID manually"
    }
    
    return $databaseId
}

# Function to create KV namespace
function New-KVNamespace {
    Write-ColorOutput "🗂️ Creating KV namespace for caching..." "Yellow"
    
    try {
        $kvResult = wrangler kv:namespace create "AI_SEARCH_CACHE" --output json | ConvertFrom-Json
        $kvId = $kvResult.id
        
        if ($kvId) {
            Write-ColorOutput "✅ KV namespace created with ID: $kvId" "Green"
            
            # Update wrangler.toml
            if (Test-Path "wrangler.toml") {
                (Get-Content "wrangler.toml") -replace "your-kv-namespace-id", $kvId | Set-Content "wrangler.toml"
            }
        }
    }
    catch {
        Write-ColorOutput "❌ Failed to create KV namespace" "Red"
        $kvId = Read-Host "Enter your KV namespace ID manually"
    }
    
    return $kvId
}

# Function to set secrets
function Set-WorkerSecrets {
    Write-ColorOutput "🔑 Setting up environment secrets..." "Yellow"
    
    $openaiKey = Read-Host "Enter OpenAI API Key (or press Enter to skip)" -AsSecureString
    if ($openaiKey.Length -gt 0) {
        $openaiKeyPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($openaiKey))
        $openaiKeyPlain | wrangler secret put OPENAI_API_KEY
        Write-ColorOutput "✅ OpenAI API key set" "Green"
    }
    
    $databaseUrl = Read-Host "Enter Database URL (external, or press Enter to skip)"
    if ($databaseUrl -and $databaseUrl.Trim() -ne "") {
        echo $databaseUrl | wrangler secret put DATABASE_URL
        Write-ColorOutput "✅ Database URL set" "Green"
    }
    
    $secretKey = Read-Host "Enter Secret Key (or press Enter to skip)" -AsSecureString
    if ($secretKey.Length -gt 0) {
        $secretKeyPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secretKey))
        $secretKeyPlain | wrangler secret put SECRET_KEY
        Write-ColorOutput "✅ Secret key set" "Green"
    }
}

# Function to deploy worker
function Deploy-Worker {
    Write-ColorOutput "🛠️ Building and deploying Cloudflare Worker..." "Yellow"
    
    Push-Location "cloudflare-workers"
    
    try {
        # Install dependencies
        if (-not (Test-Path "node_modules")) {
            npm install
        }
        
        # Deploy worker
        wrangler publish
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Worker deployed successfully" "Green"
        } else {
            Write-ColorOutput "❌ Worker deployment failed" "Red"
            return $false
        }
    }
    finally {
        Pop-Location
    }
    
    return $true
}

# Function to deploy frontend
function Deploy-Frontend {
    Write-ColorOutput "🌐 Preparing frontend for Cloudflare Pages..." "Yellow"
    
    Push-Location "frontend"
    
    try {
        # Install dependencies
        if (-not (Test-Path "node_modules")) {
            npm install
        }
        
        # Build frontend
        npm run build
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Frontend built successfully" "Green"
            
            Write-ColorOutput "📤 Frontend is ready for Cloudflare Pages deployment" "Yellow"
            Write-ColorOutput "Manual steps for Cloudflare Pages:" "Cyan"
            Write-ColorOutput "1. Go to https://dash.cloudflare.com/pages" "White"
            Write-ColorOutput "2. Click 'Create a project'" "White"
            Write-ColorOutput "3. Connect your GitHub repository" "White"
            Write-ColorOutput "4. Set build command: npm run build" "White"
            Write-ColorOutput "5. Set build output directory: build" "White"
            Write-ColorOutput "6. Set root directory: frontend" "White"
            
            Read-Host "Press Enter after setting up Cloudflare Pages connection"
        } else {
            Write-ColorOutput "❌ Frontend build failed" "Red"
            return $false
        }
    }
    finally {
        Pop-Location
    }
    
    return $true
}

# Function to migrate data
function Start-DataMigration {
    Write-ColorOutput "📦 Migrating existing data to Cloudflare D1..." "Yellow"
    
    # Look for CSV files
    $csvFiles = Get-ChildItem -Path "backend" -Filter "scraped_products_*.csv"
    
    if ($csvFiles.Count -gt 0) {
        $latestFile = $csvFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        Write-ColorOutput "Found scraped data: $($latestFile.Name)" "Green"
        
        # Create simple data migration using Python
        Write-ColorOutput "Creating data migration script..." "Yellow"
        
        $pythonScript = @"
import csv
import uuid
import os

csv_file = '$($latestFile.FullName)'
if os.path.exists(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        sql_statements = []
        
        for row in reader:
            product_id = str(uuid.uuid4())
            name = (row.get('name', '') or '').replace("'", "''")[:100]
            brand = (row.get('brand', '') or '').replace("'", "''")[:50]
            category = (row.get('category', 'general') or 'general').replace("'", "''")[:50]
            
            try:
                price = float(row.get('price', 0) or 0)
            except:
                price = 0
                
            try:
                rating = float(row.get('rating', 0) or 0)
            except:
                rating = 0
            
            description = (row.get('description', '') or '').replace("'", "''")[:200]
            
            sql = f"INSERT INTO products (id, name, brand, category, price, rating, description, in_stock) VALUES ('{product_id}', '{name}', '{brand}', '{category}', {price}, {rating}, '{description}', 1);"
            sql_statements.append(sql)
    
    with open('data_migration.sql', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_statements))
    
    print('Data migration SQL generated successfully')
else:
    print('CSV file not found')
"@
        
        $pythonScript | Out-File -FilePath "migrate_data.py" -Encoding UTF8
        
        # Run the Python migration script
        python migrate_data.py
        
        if (Test-Path "data_migration.sql") {
            wrangler d1 execute ai-search-db --file=data_migration.sql
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput "✅ Data migrated successfully" "Green"
                if (Test-Path "data_migration.sql") { Remove-Item "data_migration.sql" -Force }
                if (Test-Path "migrate_data.py") { Remove-Item "migrate_data.py" -Force }
            }
        }
    } else {
        Write-ColorOutput "No existing CSV data found to migrate" "Yellow"
    }
}

# Function to test deployment
function Test-Deployment {
    Write-ColorOutput "🧪 Testing deployment..." "Yellow"
    
    try {
        # Test health endpoint - you'll need to update with your actual worker URL
        Write-ColorOutput "Note: Update this with your actual worker URL for testing" "Yellow"
        # $response = Invoke-RestMethod -Uri "https://your-worker.workers.dev/api/health" -Method Get
        # Write-ColorOutput "✅ API is responding: $($response | ConvertTo-Json)" "Green"
    }
    catch {
        Write-ColorOutput "❌ API test failed: $($_.Exception.Message)" "Red"
    }
}

# Main deployment logic
function Start-Deployment {
    param([string]$Type)
    
    Write-ColorOutput "🔧 AI Search Engine - Cloudflare Deployment" "Green"
    Write-ColorOutput "======================================" "Green"
    
    if (-not (Test-Path "wrangler.toml")) {
        Write-ColorOutput "❌ wrangler.toml not found in current directory" "Red"
        return
    }
    
    switch ($Type.ToLower()) {
        "full" {
            New-D1Database
            New-KVNamespace
            Set-WorkerSecrets
            Start-DataMigration
            Deploy-Worker
            Deploy-Frontend
            Test-Deployment
        }
        "backend" {
            New-D1Database
            New-KVNamespace
            Set-WorkerSecrets
            Start-DataMigration
            Deploy-Worker
            Test-Deployment
        }
        "frontend" {
            Deploy-Frontend
        }
        "database" {
            New-D1Database
            New-KVNamespace
        }
        "migrate" {
            Start-DataMigration
        }
        default {
            Write-ColorOutput "Invalid deployment type. Use: full, backend, frontend, database, migrate" "Red"
            return
        }
    }
    
    Write-ColorOutput "" "White"
    Write-ColorOutput "🎉 Deployment completed!" "Green"
    Write-ColorOutput "" "White"
    Write-ColorOutput "📋 Next steps:" "Yellow"
    Write-ColorOutput "1. Update your frontend API URLs to point to the worker" "White"
    Write-ColorOutput "2. Set up custom domain in Cloudflare" "White"
    Write-ColorOutput "3. Configure DNS records" "White"
    Write-ColorOutput "4. Test all functionality" "White"
    Write-ColorOutput "" "White"
    Write-ColorOutput "🔗 Useful links:" "Green"
    Write-ColorOutput "• Cloudflare Dashboard: https://dash.cloudflare.com" "White"
    Write-ColorOutput "• Workers & Pages: https://dash.cloudflare.com/pages" "White"
    Write-ColorOutput "• D1 Database: https://dash.cloudflare.com/d1" "White"
}

# Interactive menu if no parameter provided
if (-not $DeploymentType) {
    Write-ColorOutput "Select deployment option:" "Cyan"
    Write-ColorOutput "1) Full deployment (database + worker + frontend)" "White"
    Write-ColorOutput "2) Backend only (database + worker)" "White"
    Write-ColorOutput "3) Frontend only" "White"
    Write-ColorOutput "4) Database setup only" "White"
    Write-ColorOutput "5) Migrate data only" "White"
    
    $choice = Read-Host "Choose option (1-5)"
    
    $typeMap = @{
        "1" = "full"
        "2" = "backend"
        "3" = "frontend"
        "4" = "database"
        "5" = "migrate"
    }
    
    $DeploymentType = $typeMap[$choice]
}

# Run deployment
Start-Deployment -Type $DeploymentType