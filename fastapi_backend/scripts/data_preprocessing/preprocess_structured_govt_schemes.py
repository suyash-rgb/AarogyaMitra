import os
import re
import pandas as pd

# File paths
HS_PATH = r'D:\MCA Sage Uni\Semester-3\Project Ideas\ArogyaMitra\fastapi_backend\datasets\health_schemes.xlsx'
SGS_PATH = r'D:\MCA Sage Uni\Semester-3\Project Ideas\ArogyaMitra\fastapi_backend\datasets\structured_govt_schemes.xlsx'

def clean_for_excel(text):
    if not isinstance(text, str):
        return text
    illegal_xml_chars_re = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]')
    return illegal_xml_chars_re.sub('', text)

def to_camel_case(s):
    return ''.join(word.capitalize() for word in str(s).split('_'))

def preprocess_and_merge():
    print(f'Loading health_schemes from: {HS_PATH}')
    hs = pd.read_excel(HS_PATH)
    print(f'Loading structured_govt_schemes from: {SGS_PATH}')
    sgs = pd.read_excel(SGS_PATH)

    print(f'Initial health schemes shape: {hs.shape}')
    print(f'Initial structured govt schemes shape: {sgs.shape}')

    # Standardize column names to CamelCase
    sgs.columns = [to_camel_case(col) for col in sgs.columns]
    hs.columns = [to_camel_case(col) for col in hs.columns]

    # Index by cleaned slug
    hs['SlugClean'] = hs['Slug'].astype(str).str.strip().str.lower()
    sgs['SlugClean'] = sgs['Slug'].astype(str).str.strip().str.lower()

    hs_indexed = hs.set_index('SlugClean')
    sgs_indexed = sgs.set_index('SlugClean')

    # Merge / update sgs with non-null values from hs
    cols_to_update = [c for c in sgs.columns if c != 'SlugClean']
    updated_count = 0
    for slug, hs_row in hs_indexed.iterrows():
        if slug in sgs_indexed.index:
            row_changed = False
            for col in cols_to_update:
                if col in hs_indexed.columns:
                    val = hs_row[col]
                    if pd.notna(val) and str(val).strip() and str(val).strip().lower() not in ['null', 'none']:
                        sgs_indexed.loc[slug, col] = val
                        row_changed = True
            if row_changed:
                updated_count += 1

    print(f'[+] Enriched {updated_count} schemes in structured_govt_schemes using health_schemes dataset.')

    sgs_merged = sgs_indexed.reset_index(drop=True)

    # 1. ShortTitle to UPPERCASE
    if 'ShortTitle' in sgs_merged.columns:
        sgs_merged['ShortTitle'] = sgs_merged['ShortTitle'].astype(str).str.upper()

    # 2. Slug to lowercase
    if 'Slug' in sgs_merged.columns:
        sgs_merged['Slug'] = sgs_merged['Slug'].astype(str).str.lower()

    # 3. Fill null State with "Pan India" where Level == "Central"
    if 'State' in sgs_merged.columns and 'Level' in sgs_merged.columns:
        mask_central_null = (sgs_merged['Level'].astype(str).str.strip().str.lower() == 'central') & (sgs_merged['State'].isna() | (sgs_merged['State'].astype(str).str.strip() == ''))
        sgs_merged.loc[mask_central_null, 'State'] = 'Pan India'

    # 4. Fill null References with myscheme URL
    if 'References' in sgs_merged.columns and 'Slug' in sgs_merged.columns:
        mask_null_ref = sgs_merged['References'].isna() | (sgs_merged['References'].astype(str).str.strip() == '')
        sgs_merged.loc[mask_null_ref, 'References'] = 'https://www.myscheme.gov.in/schemes/' + sgs_merged.loc[mask_null_ref, 'Slug']

    # Clean text columns for Excel compatibility
    print('Cleaning illegal XML characters for Excel export...')
    for col in sgs_merged.select_dtypes(include=['object']).columns:
        sgs_merged[col] = sgs_merged[col].apply(clean_for_excel)

    # Save cleaned merged dataset back to SGS_PATH
    print(f'Saving merged & cleaned dataset to: {SGS_PATH}')
    sgs_merged.to_excel(SGS_PATH, index=False, engine='openpyxl')
    print('[+] Dataset successfully merged, cleaned, and saved!')

if __name__ == '__main__':
    preprocess_and_merge()
