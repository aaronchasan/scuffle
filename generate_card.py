from jinja2 import Template
from weasyprint import HTML

# Load your template
with open("card_template.html", "r") as f:
    template = Template(f.read())

# Card data
card_data = {
    "name": "Bubble Blaster",
    "buy_power": "Draw 1 card",
    "cost": 3,
    "played_power": "Steal 1 gumball from opponent",
    "hand_power": "Gain 1 point at end of round",
    "gumball_wad": "Wad 1 gumball for trade"
}

# Render HTML
html = template.render(card_data)

# Export to PDF
HTML(string=html).write_pdf("card_output.pdf")

print("✅ Done! Check your project folder for card_output.pdf")
