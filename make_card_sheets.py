import os
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader

CARD_WIDTH = 2.5 * 72   # 2.5 inches in points
CARD_HEIGHT = 3.5 * 72  # 3.5 inches in points
PAGE_WIDTH, PAGE_HEIGHT = letter  # 8.5 x 11 inches in points
CARDS_PER_ROW = 3
CARDS_PER_COL = 3
X_MARGIN = (PAGE_WIDTH - (CARDS_PER_ROW * CARD_WIDTH)) / 2
Y_MARGIN = (PAGE_HEIGHT - (CARDS_PER_COL * CARD_HEIGHT)) / 2

# Directory with card PDFs
dir_with_cards = 'cards_output'
csv_file = 'sample_cards.csv'  # CSV file with card data including quantity
output_file = 'card_sheet.pdf'

# Helper to draw a single card onto the canvas
from reportlab.pdfbase import pdfdoc
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader

def draw_card(c, card_path, x, y):
    # Read the first page of the card PDF
    reader = PdfReader(card_path)
    page = reader.pages[0]
    # Render the card PDF page as an image (hack: use a temp PNG)
    import tempfile
    from pdf2image import convert_from_path
    images = convert_from_path(card_path, first_page=1, last_page=1, dpi=600)
    img = images[0]
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        img.save(tmp.name, 'PNG')
        c.drawImage(tmp.name, x, y, width=CARD_WIDTH, height=CARD_HEIGHT)
    os.unlink(tmp.name)

def get_card_list_with_quantities():
    """Read CSV and return list of (card_filename, quantity) tuples"""
    card_list = []
    
    # Get all available PDF files
    available_pdfs = {f.lower().replace('.pdf', ''): f for f in os.listdir(dir_with_cards) if f.lower().endswith('.pdf')}
    
    # Read CSV file
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        print(f"DEBUG: CSV headers: {reader.fieldnames}")
        for row in reader:
            card_name = row['name'].strip()
            # Get quantity (default to 1 if not specified)
            quantity = int(row.get('quantity', 1)) if row.get('quantity') else 1
            
            # Debug output for first few cards
            if len(card_list) < 3:
                print(f"DEBUG: Card '{card_name}' has quantity {quantity}")
                print(f"DEBUG: All row keys: {list(row.keys())}")
            
            # Find matching PDF file - try multiple variations
            pdf_filename = None
            
            # Normalize the card name for matching (remove apostrophes and question marks, replace spaces with underscores)
            normalized_name = card_name.replace("'", "").replace("'", "").replace("'", "").replace("'", "").replace(chr(8217), "").replace("?", "").replace(" ", "_").lower()
            
            # Debug output for apostrophe cards (including curly apostrophes and right single quotation mark)
            if "'" in card_name or "'" in card_name or "'" in card_name or "'" in card_name or chr(8217) in card_name:
                print(f"DEBUG: Processing card '{card_name}'")
                print(f"DEBUG: Normalized name: '{normalized_name}'")
                print(f"DEBUG: Available PDFs with similar names: {[k for k in available_pdfs.keys() if normalized_name in k or card_name.lower() in k]}")
            
            # Try exact match first
            if card_name.lower() in available_pdfs:
                pdf_filename = available_pdfs[card_name.lower()]
            # Try normalized name (no apostrophes, no question marks, spaces as underscores)
            elif normalized_name in available_pdfs:
                pdf_filename = available_pdfs[normalized_name]
                if "'" in card_name or "'" in card_name or "'" in card_name or "'" in card_name or chr(8217) in card_name:
                    print(f"DEBUG: Found match with normalized name: '{normalized_name}'")
            # Try with underscores instead of spaces (fallback)
            elif card_name.replace(' ', '_').lower() in available_pdfs:
                pdf_filename = available_pdfs[card_name.replace(' ', '_').lower()]
            
            if pdf_filename:
                card_list.append((pdf_filename, quantity))
            else:
                print(f"⚠️  Warning: No PDF found for card '{card_name}'")
    
    return card_list

# Main logic
def make_card_sheets():
    from math import ceil
    from pdf2image import convert_from_path
    
    # Get cards with quantities
    card_list = get_card_list_with_quantities()
    
    # Expand the list based on quantities
    expanded_cards = []
    for filename, quantity in card_list:
        for _ in range(quantity):
            expanded_cards.append(filename)
    
    num_cards = len(expanded_cards)
    num_per_sheet = CARDS_PER_ROW * CARDS_PER_COL
    num_sheets = ceil(num_cards / num_per_sheet)
    card_idx = 0
    
    print(f"📊 Total cards to print: {num_cards}")
    print(f"📄 Number of sheets needed: {num_sheets}")
    
    # Create one multi-page PDF file
    c = canvas.Canvas("card_sheets.pdf", pagesize=letter)
    
    for sheet_num in range(num_sheets):
        # Add a new page for each sheet (except the first one)
        if sheet_num > 0:
            c.showPage()
        
        for row in range(CARDS_PER_COL):
            for col in range(CARDS_PER_ROW):
                if card_idx >= num_cards:
                    break
                x = X_MARGIN + col * CARD_WIDTH
                y = PAGE_HEIGHT - Y_MARGIN - (row + 1) * CARD_HEIGHT
                card_path = os.path.join(dir_with_cards, expanded_cards[card_idx])
                draw_card(c, card_path, x, y)
                card_idx += 1
    
    c.save()
    print(f"✅ Created 1 multi-page PDF with {num_sheets} pages: card_sheets.pdf")

if __name__ == "__main__":
    make_card_sheets() 