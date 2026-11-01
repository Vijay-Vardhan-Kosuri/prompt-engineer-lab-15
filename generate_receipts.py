#!/usr/bin/env python3
"""Generate synthetic restaurant receipt images for multimodal prompting experiment."""

from PIL import Image, ImageDraw, ImageFont
import os
import random
from datetime import datetime, timedelta

OUTPUT_DIR = "images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Try to use a monospace-like font; fall back to default
try:
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    font_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 18)
except Exception:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_mono = ImageFont.load_default()

def create_receipt(filename, restaurant_name, date_str, items, tax_rate=0.08, tip=None, address=None, phone=None):
    """Create a realistic-looking receipt image."""
    width = 400
    # Calculate height based on content
    base_height = 200
    item_height = 30 * len(items)
    height = base_height + item_height + 180
    if tip:
        height += 40

    img = Image.new("RGB", (width, height), color=(255, 255, 250))  # Off-white paper
    draw = ImageDraw.Draw(img)

    y = 20

    # Header - Restaurant name
    draw.text((width // 2, y), restaurant_name, font=font_large, fill=(20, 20, 20), anchor="mt")
    y += 40

    if address:
        draw.text((width // 2, y), address, font=font_small, fill=(60, 60, 60), anchor="mt")
        y += 22
    if phone:
        draw.text((width // 2, y), phone, font=font_small, fill=(60, 60, 60), anchor="mt")
        y += 25

    # Separator
    draw.line([(30, y), (width - 30, y)], fill=(100, 100, 100), width=1)
    y += 15

    # Date and time
    draw.text((30, y), f"Date: {date_str}", font=font_small, fill=(40, 40, 40))
    y += 25

    draw.line([(30, y), (width - 30, y)], fill=(180, 180, 180), width=1)
    y += 15

    # Items
    subtotal = 0.0
    for name, price in items:
        draw.text((30, y), name, font=font_mono, fill=(20, 20, 20))
        price_str = f"${price:.2f}"
        draw.text((width - 30, y), price_str, font=font_mono, fill=(20, 20, 20), anchor="rt")
        subtotal += price
        y += 28

    y += 5
    draw.line([(30, y), (width - 30, y)], fill=(100, 100, 100), width=1)
    y += 15

    # Subtotal
    draw.text((30, y), "Subtotal", font=font_medium, fill=(30, 30, 30))
    draw.text((width - 30, y), f"${subtotal:.2f}", font=font_medium, fill=(30, 30, 30), anchor="rt")
    y += 28

    # Tax
    tax = round(subtotal * tax_rate, 2)
    draw.text((30, y), f"Tax ({int(tax_rate*100)}%)", font=font_medium, fill=(30, 30, 30))
    draw.text((width - 30, y), f"${tax:.2f}", font=font_medium, fill=(30, 30, 30), anchor="rt")
    y += 28

    if tip is not None:
        draw.text((30, y), "Tip", font=font_medium, fill=(30, 30, 30))
        draw.text((width - 30, y), f"${tip:.2f}", font=font_medium, fill=(30, 30, 30), anchor="rt")
        y += 28
        total = round(subtotal + tax + tip, 2)
    else:
        total = round(subtotal + tax, 2)

    # Total
    draw.line([(30, y), (width - 30, y)], fill=(50, 50, 50), width=2)
    y += 12
    draw.text((30, y), "TOTAL", font=font_large, fill=(0, 0, 0))
    draw.text((width - 30, y), f"${total:.2f}", font=font_large, fill=(0, 0, 0), anchor="rt")
    y += 45

    # Footer
    draw.line([(30, y), (width - 30, y)], fill=(180, 180, 180), width=1)
    y += 15
    draw.text((width // 2, y), "Thank you for dining with us!", font=font_small, fill=(80, 80, 80), anchor="mt")
    y += 22
    draw.text((width // 2, y), "Please come again", font=font_small, fill=(100, 100, 100), anchor="mt")

    # Add slight noise / paper texture feel (simple dots)
    for _ in range(80):
        px = random.randint(10, width - 10)
        py = random.randint(10, height - 10)
        draw.point((px, py), fill=(220, 220, 210))

    img.save(os.path.join(OUTPUT_DIR, filename), "JPEG", quality=92)
    print(f"Created: {filename} | Subtotal: ${subtotal:.2f} Tax: ${tax:.2f} Total: ${total:.2f}")
    return {
        "restaurant_name": restaurant_name,
        "date": date_str.split()[0] if " " in date_str else date_str,
        "items": [{"name": n, "price": p} for n, p in items],
        "subtotal": round(subtotal, 2),
        "tax": tax,
        "total": total,
        "tip": tip
    }

# Generate 3 sample receipts
receipts_meta = []

# Receipt 1 - Asian restaurant
meta1 = create_receipt(
    "receipt_01_golden_wok.jpg",
    "The Golden Wok",
    "2026-03-15 19:42",
    [
        ("Spring Rolls (2pc)", 5.99),
        ("Kung Pao Chicken", 14.99),
        ("Fried Rice", 3.99),
        ("Green Tea", 2.50),
    ],
    tax_rate=0.0825,
    address="142 Market Street, San Francisco",
    phone="(415) 555-0199"
)
receipts_meta.append(meta1)

# Receipt 2 - Italian / Pizza
meta2 = create_receipt(
    "receipt_02_bella_italia.jpg",
    "Bella Italia Trattoria",
    "2026-04-02 13:15",
    [
        ("Margherita Pizza", 16.50),
        ("Caesar Salad", 9.75),
        ("Tiramisu", 7.50),
        ("Espresso", 3.25),
        ("Sparkling Water", 2.00),
    ],
    tax_rate=0.0875,
    tip=8.00,
    address="88 Oak Avenue, Chicago, IL",
    phone="(312) 555-8741"
)
receipts_meta.append(meta2)

# Receipt 3 - American diner / burger
meta3 = create_receipt(
    "receipt_03_blue_plate.jpg",
    "Blue Plate Diner",
    "2026-05-20 12:30",
    [
        ("Classic Cheeseburger", 12.99),
        ("French Fries", 4.50),
        ("Chocolate Milkshake", 5.75),
        ("Apple Pie Slice", 6.25),
    ],
    tax_rate=0.075,
    address="500 Main Blvd, Austin, TX",
    phone="(512) 555-3322"
)
receipts_meta.append(meta3)

# Save ground truth JSON for reference
import json
with open("ground_truth.json", "w") as f:
    json.dump(receipts_meta, f, indent=2)

print("\nGround truth saved to ground_truth.json")
print("Done generating receipts.")
