import os
import re
import sys
import time
import random
import pandas as pd
from seleniumbase import Driver

# Ensure stdout uses UTF-8 encoding to avoid Windows cp1252 UnicodeEncodeError for symbols like ₹ (\u20b9)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Define dataset path
DATASET_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'structured_govt_schemes.xlsx')

# Target columns to enrich if missing
TARGET_COLUMNS = ['Documents', 'Benefits', 'ApplicationProcess', 'Beneficiaries', 'Department', 'Eligibility']

SECTION_HEADERS = [
    "Details", 
    "Benefits", 
    "Eligibility", 
    "Application Process", 
    "Documents Required", 
    "Frequently Asked Questions", 
    "Sources And References"
]

def clean_for_excel(text):
    if not isinstance(text, str):
        return text
    illegal_xml_chars_re = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]')
    return illegal_xml_chars_re.sub('', text)

def safe_str(val):
    if val is None:
        return ""
    return str(val).encode('utf-8', errors='replace').decode('utf-8')

def parse_myscheme_text(lines):
    """Extracts structured sections line-by-line directly from myscheme rendered page body text."""
    start_idx = 0
    for i, line in enumerate(lines):
        if "Check Eligibility" in line or ("Details" in line and i > 15):
            start_idx = i
            break

    current_section = None
    section_lines = {h: [] for h in SECTION_HEADERS}
    
    i = start_idx
    while i < len(lines):
        line_str = lines[i].strip()
        
        matched_header = None
        for h in SECTION_HEADERS:
            if line_str == h:
                matched_header = h
                break
        
        if matched_header:
            current_section = matched_header
            # Skip repeating header line if duplicate
            if i + 1 < len(lines) and lines[i+1].strip() == matched_header:
                i += 1
            # Skip mode badges under Application Process
            if i + 1 < len(lines) and lines[i+1].strip() in ["Online", "Offline"]:
                i += 1
                if i + 1 < len(lines) and lines[i+1].strip() == matched_header:
                    i += 1
        elif current_section:
            if line_str in ["Was this helpful?", "News and Updates", "Share", "©2026", "Footer"]:
                break
            section_lines[current_section].append(line_str)
        i += 1

    result = {}
    for h, lns in section_lines.items():
        text_str = "\n".join([l for l in lns if l]).strip()
        result[h] = text_str if text_str else None

    return result

def is_cell_empty(val):
    if pd.isna(val) or val is None:
        return True
    if isinstance(val, str) and not val.strip():
        return True
    return False

def main():
    if not os.path.exists(DATASET_PATH):
        print(f"[!] Dataset not found at {DATASET_PATH}")
        return

    df = pd.read_excel(DATASET_PATH)
    
    rows_to_process = []
    for idx, row in df.iterrows():
        missing_fields = [col for col in TARGET_COLUMNS if col in df.columns and is_cell_empty(row[col])]
        if missing_fields:
            rows_to_process.append((idx, row, missing_fields))
            
    print(f"Total schemes in dataset: {len(df)}")
    print(f"Found {len(rows_to_process)} schemes with missing target data.")
    
    if not rows_to_process:
        print("[+] No missing target data found! All target columns are populated.")
        return

    updated_schemes_count = 0
    driver = Driver(uc=True, headless=True)

    try:
        for count, (idx, row, missing_fields) in enumerate(rows_to_process, 1):
            slug = str(row['Slug']).strip()
            scheme_name = safe_str(row['SchemeName'])
            url = f"https://www.myscheme.gov.in/schemes/{slug}"
            
            try:
                print(f"\n[{count}/{len(rows_to_process)}] Scraping index #{idx+1}: '{scheme_name}' ({slug})")
            except Exception:
                print(f"\n[{count}/{len(rows_to_process)}] Scraping index #{idx+1}: ({slug})")
            
            try:
                driver.get(url)
                time.sleep(2.0)
                body_text = driver.find_element("tag name", "body").text
                
                lines = body_text.split("\n")
                parsed = parse_myscheme_text(lines)
                
                parsed_map = {
                    'Benefits': parsed.get('Benefits'),
                    'ApplicationProcess': parsed.get('Application Process'),
                    'Documents': parsed.get('Documents Required'),
                    'Eligibility': parsed.get('Eligibility'),
                }

                row_updated = False
                for field in missing_fields:
                    val = parsed_map.get(field)
                    if val and str(val).strip() and str(val).strip().lower() not in ["null", "none"]:
                        if is_cell_empty(df.at[idx, field]):
                            clean_val = clean_for_excel(str(val).strip())
                            df.at[idx, field] = clean_val
                            try:
                                print(f"  [+] Filled '{field}': {clean_val[:60]}...")
                            except Exception:
                                print(f"  [+] Filled '{field}'")
                            row_updated = True
                
                if row_updated:
                    updated_schemes_count += 1
                    df.to_excel(DATASET_PATH, index=False, engine='openpyxl')
            except Exception as e:
                print(f"  [x] Error scraping {slug}: {e}")

            time.sleep(random.uniform(0.5, 1.0))

    finally:
        try:
            driver.quit()
        except Exception:
            pass

    print(f"\n[+] Scraping session finished! Total schemes updated in this run: {updated_schemes_count}")

if __name__ == '__main__':
    main()
