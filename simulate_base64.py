#!/usr/bin/env python3
"""Helper: encode a receipt image to Base64 (useful when calling vision APIs)."""

import base64
import sys
import os

def encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python simulate_base64.py <path_to_jpg>")
        print("Example: python simulate_base64.py images/receipt_01_golden_wok.jpg")
        sys.exit(1)

    img_path = sys.argv[1]
    if not os.path.exists(img_path):
        print(f"File not found: {img_path}")
        sys.exit(1)

    b64 = encode_image(img_path)
    print(f"Base64 length: {len(b64)} characters")
    print("--- First 120 chars ---")
    print(b64[:120] + "...")
    print("--- Last 40 chars ---")
    print("..." + b64[-40:])
    # Optionally write full base64 to a file
    out_path = img_path.replace(".jpg", ".b64.txt")
    with open(out_path, "w") as f:
        f.write(b64)
    print(f"\nFull Base64 written to: {out_path}")
