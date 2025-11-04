#!/bin/bash

echo "📕 Installing PDF Generation Support..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Try normal installation first
echo "Attempting standard installation..."
pip install reportlab

# Check if successful
python -c "import reportlab" 2>/dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ reportlab installed successfully!"
    echo ""
    echo "You can now generate PDF reports from the dashboard."
    echo "Navigate to: 📧 Weekly Report → Generate Report → 📕 PDF Export"
else
    echo ""
    echo "⚠️  Standard installation failed. Trying alternative method..."
    echo ""
    
    # Try with trusted hosts
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org reportlab
    
    # Check again
    python -c "import reportlab" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ reportlab installed successfully with alternative method!"
    else
        echo ""
        echo "❌ Installation failed. Please try manual installation:"
        echo ""
        echo "1. Check your internet connection"
        echo "2. Update pip: pip install --upgrade pip"
        echo "3. Try: pip install --trusted-host pypi.org reportlab"
        echo ""
        echo "Or use the Plain Text format instead of PDF."
    fi
fi

echo ""
echo "For more help, see: docs/PDF_REPORT_SETUP.md"

