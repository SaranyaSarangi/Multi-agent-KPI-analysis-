#!/bin/bash

# KPI Agent System - Repository Setup Script
# This script creates the complete folder structure

echo "🚀 Setting up KPI Multi-Agent System repository..."

# Create main directory structure
echo "📁 Creating directories..."
mkdir -p src
mkdir -p examples
mkdir -p tests
mkdir -p docs

# Create __init__.py files
echo "📝 Creating __init__.py files..."
touch src/__init__.py
touch tests/__init__.py

# Create placeholder files
echo "📄 Creating placeholder files..."
touch src/utils.py
touch tests/conftest.py
touch examples/advanced_analysis.py
touch examples/sample_data.csv

# Add sample CSV data
cat > examples/sample_data.csv << 'EOF'
Date,Sales,Revenue,Customer_Count,Conversion_Rate
2025-01-01,100,5000,50,2.0
2025-01-02,105,5250,52,2.1
2025-01-03,98,4900,49,2.0
2025-01-04,300,15000,150,2.0
2025-01-05,102,5100,51,2.0
2025-01-06,99,4950,50,1.9
2025-01-07,103,5150,52,2.0
2025-01-08,101,5050,50,2.0
2025-01-09,97,4850,49,2.0
2025-01-10,500,25000,250,2.0
EOF

# Create LICENSE file
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

echo ""
echo "✅ Repository structure created!"
echo ""
echo "📋 Current structure:"
tree -L 2 -I '__pycache__|*.pyc|venv|env' 2>/dev/null || find . -type f -o -type d | grep -v '__pycache__\|\.pyc\|venv\|env' | sort

echo ""
echo "🔧 Next steps:"
echo "1. Copy the Python files from the artifacts into their respective locations"
echo "2. Create and configure .env file: cp .env.example .env"
echo "3. Add your GOOGLE_API_KEY to .env"
echo "4. Create virtual environment: python -m venv venv"
echo "5. Activate it: source venv/bin/activate"
echo "6. Install dependencies: pip install -r requirements.txt"
echo "7. Test: python examples/basic_usage.py"
echo ""
echo "📚 Files to copy:"
echo "   - .env.example (already shown in artifacts)"
echo "   - .gitignore (already shown in artifacts)"
echo "   - requirements.txt (already shown in artifacts)"
echo "   - setup.py (from artifacts)"
echo "   - README.md (from artifacts)"
echo "   - All src/*.py files (from artifacts)"
echo "   - examples/basic_usage.py (from artifacts)"
echo "   - tests/test_detection_engine.py (from artifacts)"
echo ""
echo "🎉 Setup complete!"
