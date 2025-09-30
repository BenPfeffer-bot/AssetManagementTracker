#!/bin/bash
# Startup script for Portfolio Tracker Dashboard

echo "🚀 Starting Portfolio Tracker Dashboard..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Run Streamlit app
streamlit run app.py --server.port 8501 --server.address localhost

# Note: The dashboard will open automatically in your browser
# Access it at: http://localhost:8501
