# FitFusion Studio Setup Script
# Run this to complete the setup

Write-Host "🏋️ FitFusion Studio - Setup Script" -ForegroundColor Cyan
Write-Host "====================================`n" -ForegroundColor Cyan

# Step 1: Check Python
Write-Host "1️⃣  Checking Python installation..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found! Please install Python 3.8 or later." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Python found`n" -ForegroundColor Green

# Step 2: Install dependencies
Write-Host "2️⃣  Installing dependencies..." -ForegroundColor Yellow
pip install -q google-generativeai gradio python-dotenv reportlab
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencies installed`n" -ForegroundColor Green

# Step 3: Check for .env file
Write-Host "3️⃣  Checking for .env file..." -ForegroundColor Yellow
if (-Not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "📝 Please edit .env and add your GOOGLE_API_KEY" -ForegroundColor Cyan
    Write-Host "   Get your key from: https://makersuite.google.com/app/apikey`n" -ForegroundColor Cyan
} else {
    Write-Host "✅ .env file found`n" -ForegroundColor Green
}

# Step 4: Generate PDF
Write-Host "4️⃣  Generating business PDF..." -ForegroundColor Yellow
python generate_pdf.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to generate PDF!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ PDF generated`n" -ForegroundColor Green

# Step 5: Final check
Write-Host "5️⃣  Verifying setup..." -ForegroundColor Yellow
$requiredFiles = @(
    "requirements.txt",
    ".env",
    "me\business_summary.txt",
    "me\about_business.pdf",
    "business_agent.ipynb",
    "app.py",
    "generate_pdf.py",
    "README.md"
)

$allPresent = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (missing)" -ForegroundColor Red
        $allPresent = $false
    }
}

Write-Host ""
if ($allPresent) {
    Write-Host "🎉 Setup complete! You're ready to go!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Add your GOOGLE_API_KEY to the .env file"
    Write-Host "  2. Run: python app.py"
    Write-Host "  3. Or open: business_agent.ipynb in Jupyter"
    Write-Host ""
} else {
    Write-Host "⚠️  Some files are missing. Please check the setup." -ForegroundColor Yellow
}
