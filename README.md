# Schoolyard Scuffle Cards

This project generates printable card PDFs for Schoolyard Scuffle, a board game I'm making. It uses data from a CSV file and a Jinja2 HTML template.

## Requirements
- Python 3.7+
- [WeasyPrint](https://weasyprint.org/) (for HTML to PDF)
- [Jinja2](https://palletsprojects.com/p/jinja/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [pdf2image](https://pypi.org/project/pdf2image/)
- [reportlab](https://pypi.org/project/reportlab/)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup
1. Clone/download this repo.
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies as above.

## CSV Format
Your main card data is in `sample_cards.csv`. Required columns:
- `name` (card name, must be unique)
- `buy_power`, `played_power`, `hand_power`, `gumball_wad`, `cost` (card text fields)
- `buy_power_icons`, `played_icons`, `hand_icons`, `gumball_icons` (icon specs, e.g. `action.svg:1|card.svg:1`)
- `clique`, `clique_icon` (for clique display)
- `quantity` (number of copies to print on sheets)

**Note:**
- Apostrophes and special characters in names are automatically normalized for PDF filenames.
- If a card's `quantity` is blank, it defaults to 1.

## Usage

### 1. Bulk Generate Card PDFs
Generates one PDF per card in `cards_output/`:
```bash
bulk
```
Or manually:
```bash
python generate_cards_bulk.py sample_cards.csv
```

### 2. Create Printout Sheets
Combines all card PDFs (with quantities) into a single multi-page PDF for printing:
```bash
printouts
```
Or manually:
```bash
python make_card_sheets.py
```
- Output: `card_sheets.pdf` (multi-page, 9 cards per page)

### 3. Add/Update Card Data
- Edit `sample_cards.csv` in a spreadsheet or text editor.
- Add new cards, update text, icons, or quantities.
- Run `bulk` and `printouts` again to update PDFs.

### 4. Custom Icons
- Place SVG icon files in the `icons/` directory.
- Reference them in the CSV (e.g. `action.svg:1|card.svg:1`).

## Shortcuts
- `bulk` — generate all card PDFs from CSV
- `printouts` — create printout sheets (multi-page PDF)

## File Structure
```
Cards/
  generate_cards_bulk.py      # Bulk card PDF generator
  make_card_sheets.py         # Printout sheet generator
  card_template.html          # Jinja2 HTML template for cards
  sample_cards.csv            # Main card data
  cards_output/               # Generated card PDFs
  icons/                      # SVG icon files
  venv/                       # (optional) Python virtual environment
```

## Copyright & Usage

All card designs, names, text, and artwork in this repository belong to Aaron Chasan. MINE MINE MINE.
These materials are provided for personal reference and inspiration only.  
**You may not reproduce, redistribute, or use these cards or designs for commercial purposes without explicit permission.**

If you wish to use or adapt any part of this project, please contact aaron.s.chasan@gmail.com
