import csv
import os
from jinja2 import Template
from weasyprint import HTML

def build_icon_html(icon_spec: str, css_class: str) -> str:
    if not icon_spec:
        return ""
    pieces = []
    for part in icon_spec.split("|"):
        try:
            name, qty = part.split(":")
            qty = int(qty)
            for _ in range(qty):
                pieces.append(f'<img src="icons/{name}" class="icon">')
        except ValueError as e:
            print(f"❌ Error parsing icon spec '{part}': {e}")
            print(f"   Expected format: 'filename.svg:quantity'")
            continue
        except Exception as e:
            print(f"❌ Unexpected error parsing icon spec '{part}': {e}")
            continue
    return f'<span class="icon-row {css_class}">' + "".join(pieces) + "</span>"

def generate_cards_from_csv(csv_file, output_dir="cards_output"):
    """Generate multiple cards from a CSV file"""
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load the template
    with open("card_template.html", "r") as f:
        template = Template(f.read())
    
    # Read CSV file
    cards_generated = 0
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Clean up the data (remove extra whitespace)
            card_data = {key.strip(): value.strip() if isinstance(value, str) else value 
                        for key, value in row.items()}

            # Add icon HTML to the card data
            card_data["gumball_icon_html"] = build_icon_html(card_data.get("gumball_icons", ""), "gumball-icons")
            card_data["played_icon_html"] = build_icon_html(card_data.get("played_icons", ""), "played-icons")
            card_data["hand_icon_html"] = build_icon_html(card_data.get("hand_icons", ""), "hand-icons")
            card_data["buy_power_icon_html"] = build_icon_html(card_data.get("buy_power_icons", ""), "buy-power-icons")
        
            # Generate filename from card name (sanitize for filesystem)
            card_name = card_data.get('name', f'card_{cards_generated}')
            safe_filename = "".join(c for c in card_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_filename = safe_filename.replace(' ', '_')
            
            # Render HTML
            html = template.render(card_data)
            # Export to PDF
            pdf_filename = f"{safe_filename}.pdf"
            pdf_path = os.path.join(output_dir, pdf_filename)
            
            try:
                HTML(string=html, base_url=os.getcwd()).write_pdf(pdf_path)
                print(f"✅ Generated: {pdf_filename}")
                cards_generated += 1
            except Exception as e:
                print(f"❌ Error generating {pdf_filename}: {e}")
    
    print(f"\n🎉 Successfully generated {cards_generated} cards in '{output_dir}' folder!")

def generate_single_card(card_data, output_filename="card_output.pdf"):
    """Generate a single card (for backward compatibility)"""
    
    # Load the template
    with open("card_template.html", "r") as f:
        template = Template(f.read())
    
    # Render HTML
    html = template.render(card_data)
    
    # Export to PDF
    HTML(string=html).write_pdf(output_filename)
    print(f"✅ Generated: {output_filename}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # If CSV file provided as argument
        csv_file = sys.argv[1]
        if os.path.exists(csv_file):
            generate_cards_from_csv(csv_file)
        else:
            print(f"❌ CSV file '{csv_file}' not found!")
    else:
        # Default behavior - generate single card
        card_data = {
            "name": "Bubble Blaster",
            "buy_power": "Draw 1 card",
            "cost": 3,
            "played_power": "Steal 1 gumball from opponent",
            "hand_power": "Gain 1 point at end of round",
            "gumball_wad": "Wad 1 gumball for trade"
        }
        generate_single_card(card_data) 