import os
import sys
import time
import re
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Force unbuffered UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DATASET_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'structured_govt_schemes.xlsx')
TARGET_COLUMNS = ['Benefits', 'Eligibility', 'ApplicationProcess', 'Documents', 'Beneficiaries', 'Subcategories', 'Faqs']

TAB_MAPPING = {
    'Benefits': 'Benefits',
    'Eligibility': 'Eligibility',
    'ApplicationProcess': 'Application Process',
    'Documents': 'Documents Required',
    'Faqs': 'Frequently Asked Questions',
    'Details': 'Details'
}

def clean_for_excel(text):
    if not isinstance(text, str):
        return text
    illegal_xml_chars_re = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]')
    return illegal_xml_chars_re.sub('', text)

def is_cell_empty(val):
    if pd.isna(val) or val is None:
        return True
    if isinstance(val, str) and not val.strip():
        return True
    return False

def extract_tab_text(driver, tab_name):
    """Dynamically clicks tab and slices exact body text rendered between header list and footer."""
    try:
        spans = driver.find_elements(By.XPATH, f"//span[contains(text(), '{tab_name}')]")
        target_span = None
        for s in spans:
            txt = s.text.strip()
            if txt == tab_name or (tab_name == "Documents Required" and "Documents" in txt):
                target_span = s
                break
                
        if target_span:
            driver.execute_script("arguments[0].click();", target_span)
            time.sleep(0.7)
            
        body_text = driver.find_element(By.TAG_NAME, "body").text
        lines = body_text.split('\n')
        
        start_idx = None
        stop_idx = None
        
        for i, line in enumerate(lines):
            if line.strip() == "Frequently Asked Questions" and start_idx is None:
                start_idx = i + 1
            elif line.strip() == "Was this helpful?":
                stop_idx = i
                break
                
        if start_idx is not None and stop_idx is not None and start_idx < stop_idx:
            content_lines = [l.strip() for l in lines[start_idx:stop_idx] if l.strip()]
            if content_lines and content_lines[0] in ["Online", "Offline"]:
                content_lines.pop(0)
            res = "\n".join(content_lines).strip()
            return res if res else None
            
    except Exception as e:
        print(f"    [!] Exception extracting '{tab_name}': {e}", flush=True)
        
    return None

def main():
    if not os.path.exists(DATASET_PATH):
        print(f"[!] Dataset file not found at: {DATASET_PATH}", flush=True)
        return

    df = pd.read_excel(DATASET_PATH)
    
    rows_to_process = []
    for idx, row in df.iterrows():
        missing = [col for col in TARGET_COLUMNS if col in df.columns and is_cell_empty(row[col])]
        if missing:
            rows_to_process.append((idx, row['Slug'], row['SchemeName'], missing))
            
    print(f"Total schemes in dataset: {len(df)}", flush=True)
    print(f"Total schemes with missing fields: {len(rows_to_process)}", flush=True)
    
    if not rows_to_process:
        print("[+] All target columns are fully populated! No missing values remaining.", flush=True)
        return

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    updated_count = 0

    try:
        for count, (idx, slug, name, missing) in enumerate(rows_to_process, 1):
            url = f"https://www.myscheme.gov.in/schemes/{slug}"
            print(f"\n[{count}/{len(rows_to_process)}] Scraping Index #{idx+1}: '{name}' ({slug})", flush=True)
            print(f"  Missing fields: {missing}", flush=True)
            
            try:
                driver.get(url)
                time.sleep(2.5)
                
                row_updated = False
                for col in missing:
                    tab_name = TAB_MAPPING.get(col, col)
                    extracted_text = extract_tab_text(driver, tab_name)
                    
                    if extracted_text:
                        clean_text = clean_for_excel(extracted_text)
                        df.at[idx, col] = clean_text
                        row_updated = True
                        print(f"  [+] Extracted '{col}': {clean_text[:60]}...", flush=True)
                    else:
                        print(f"  [-] Could not extract '{col}' (Page might not have this section)", flush=True)

                if row_updated:
                    updated_count += 1
                    if updated_count % 5 == 0:
                        df.to_excel(DATASET_PATH, index=False, engine='openpyxl')
                        print(f"  [✓] Progress saved to Excel (Total updated so far: {updated_count})", flush=True)

            except Exception as e:
                print(f"  [x] Error loading {slug}: {e}", flush=True)

            time.sleep(random.uniform(0.3, 0.6))

    finally:
        driver.quit()
        df.to_excel(DATASET_PATH, index=False, engine='openpyxl')
        print(f"\n[+] Web scraping run complete! Total schemes updated: {updated_count}", flush=True)

if __name__ == '__main__':
    main()
