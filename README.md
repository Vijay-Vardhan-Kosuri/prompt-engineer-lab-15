# Multimodal Receipt Extraction Experiment

## Aim
Explore multimodal prompting using a vision-capable LLM (e.g., GPT-4o, Claude 3.5 Sonnet, Gemini, Grok Vision, etc.). Write a prompt that analyzes a restaurant receipt image, extracts structured information, and returns it as JSON.

## Task
Given an image of a restaurant receipt, extract:
- Restaurant Name
- Date
- Items Ordered (list of name + price)
- Subtotal
- Tax
- Total
- (Optional) Tip

Return a JSON object. Optionally validate that subtotal + tax (+ tip) ≈ total.

## Directory Structure
```
receipt_experiment/
├── README.md
├── generate_receipts.py          # Script to regenerate synthetic receipts
├── ground_truth.json             # Ground-truth values for the samples
├── prompts/
│   └── receipt_extraction_prompt.txt   # Ready-to-use multimodal prompt
├── images/                       # Source receipt images
│   ├── receipt_01_golden_wok.jpg
│   ├── receipt_02_bella_italia.jpg
│   └── receipt_03_blue_plate.jpg
└── output/                       # Sample outputs + expected results
    ├── receipt_01_golden_wok.jpg
    ├── receipt_02_bella_italia.jpg
    ├── receipt_03_blue_plate.jpg
    ├── expected_output_01.json
    ├── expected_output_02.json
    └── expected_output_03.json
```

## Sample Receipts (3)
1. **The Golden Wok** – Asian cuisine, no tip
2. **Bella Italia Trattoria** – Italian, includes tip
3. **Blue Plate Diner** – American diner, no tip

All images are synthetic high-quality JPGs generated with Python/Pillow for reproducibility and clear text.

## How to Test
1. Load any image from `images/` or `output/`.
2. Use the prompt in `prompts/receipt_extraction_prompt.txt` together with the image.
3. Send to a multimodal model that accepts image + text.
4. Compare the model’s JSON output against the corresponding `expected_output_XX.json`.

### Example (OpenAI-style pseudocode)
```python
import base64
from openai import OpenAI

client = OpenAI()

with open("images/receipt_01_golden_wok.jpg", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

prompt = open("prompts/receipt_extraction_prompt.txt").read()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                }
            ]
        }
    ],
    response_format={"type": "json_object"}  # if supported
)

print(response.choices[0].message.content)
```

## Expected Output Schema
See `prompts/receipt_extraction_prompt.txt` and the `expected_output_*.json` files.

## Notes
- Images contain slight paper texture for realism.
- Tax rates and tip presence vary across samples to test robustness.
- All ground-truth calculations are consistent within ±0.02 tolerance.
