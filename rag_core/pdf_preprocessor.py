import pytesseract
from pdf2image import convert_from_path
import unicodedata
import re
import os
from PIL import ImageOps

def extract_text_ocr(pdf_path, lang="ben", poppler_path=None):
    print("Converting PDF pages to images:")
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
    all_text = ""

    for idx, page in enumerate(pages):
        print(f"OCR processing in page {idx + 1}/{len(pages)}")
        #grayscale and threshold
        gray = page.convert("L")
        thresholded = gray.point(lambda x: 0 if x < 160 else 255, '1')
        #OCR with Tesseract
        raw_text = pytesseract.image_to_string(thresholded, lang=lang)
        cleaned_text = clean_text(raw_text)
        all_text += f"\n\n=== PAGE {idx + 1} ===\n\n{cleaned_text}\n"
    return all_text.strip()


def clean_text(text):
    text = unicodedata.normalize("NFC", text)
    #Handling Bangla, digits, MCQ symbols and punctuation
    text = re.sub(r"[^\u0980-\u09FF০-৯\s।,:()?%\-\n]", "", text)
    #Normalize MCQ numbering
    text = re.sub(r"(?m)^([০-৯]{1,3})[।:\.]", r"\1।", text)
    #Remove trailing board names after '?'
    text = re.sub(r"(?<=\?)\s+.*", "", text)
    #Merge lines sif paragrapghs
    text = re.sub(r"(?<![।\n])\n(?![০-৯]{1,3}।|\([কখগঘ]\))", " ", text)
    # Filter headers & footers
    skip_pattern = re.compile(
        r"(অনলাইন ব্যাচ|বোর্ড|পৃষ্ঠা|www\.|প্রশ্নপত্র|২০২[০-৯]|২০[০-৯]{2}|[০-৯]+ টাকায়|শ্রেণি|অধিভুক্ত|Online Class|Batch|ঢা. বো.|য. বো.)",
        re.IGNORECASE
    )

    clean_lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line or len(line) < 5:
            continue
        if skip_pattern.search(line):
            continue
        bangla_chars = sum('\u0980' <= ch <= '\u09FF' for ch in line)
        if bangla_chars / len(line) >= 0.5:
            clean_lines.append(line)
    return "\n".join(clean_lines).strip()

def save_text(text, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
