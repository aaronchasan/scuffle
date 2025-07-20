#!/bin/bash
echo "🖨️  Creating card sheet printouts..."
source venv/bin/activate
python make_card_sheets.py
echo ""
echo "🎉 Printouts created! Check for card_sheet_*.pdf files." 