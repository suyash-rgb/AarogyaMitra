import pandas as pd
import re
import os

def fix_mojibake(text):
    if pd.isna(text):
        return text
    text = str(text)
    
    # Common windows-1252 to utf-8 mojibake replacements
    replacements = {
        'â€™': "'",
        'â€œ': '"',
        'â€': '"',
        'â€˜': "'",
        '’': "'",
        '‘': "'",
        '“': '"',
        '”': '"',
        '\ufffd': "'", # The unicode replacement character
    }
    
    for k, v in replacements.items():
        if k:
            text = text.replace(k, v)
    
    # Remove excessive spaces and newlines
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def localize_western_terms(text):
    if pd.isna(text):
        return text
    text = str(text)
    # Use regex with word boundaries for safe replacement (case insensitive)
    replacements = {
        r'\b911\b': '108',
        r'\bemergency room\b': 'emergency ward',
        r'\bacetaminophen\b': 'Paracetamol',
        r'\btylenol\b': 'Paracetamol',
        r'\badvil\b': 'Ibuprofen',
        r'\bmotrin\b': 'Ibuprofen',
        r'\baleve\b': 'Naproxen'
    }
    for k, v in replacements.items():
        text = re.sub(k, v, text, flags=re.IGNORECASE)
    return text

def clean_answer(text):
    if pd.isna(text):
        return text
    text = str(text)
    
    # Remove [] brackets ONLY from answers (as requested originally)
    text = text.replace('[', '').replace(']', '')
    
    # Clean mojibake etc
    text = fix_mojibake(text)
    
    # Localize Western medical and geographical phrases
    text = localize_western_terms(text)
    
    # Remove Excel formula prefixes at the start (+, -, =, @)
    text = re.sub(r'^[\=\+\-\@\s]+', '', text)
    
    return text

def clean_question(text):
    if pd.isna(text):
        return text
    text = str(text)
    text = fix_mojibake(text)
    text = localize_western_terms(text)
    return text

def strip_quotes(text):
    if pd.isna(text):
        return text
    text = str(text).strip()
    # Remove enclosing quotes
    text = re.sub(r'^["\']+|["\']+$', '', text)
    return text.strip()

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(base_dir, 'datasets', 'fine-tuning', 'custom-dataset-archive', 'merged_data.csv')
    
    print(f"Reading dataset from: {file_path}")
    df = pd.read_csv(file_path, encoding='utf-8')

    # Remove first column if it's the serial number
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    else:
        df = df.iloc[:, 1:]

    # 1. Drop any nulls in question or answer
    df = df.dropna(subset=['question', 'answer'])

    # 2. Strip enclosing quotes and clean text
    df['question'] = df['question'].apply(strip_quotes).apply(clean_question)
    df['answer'] = df['answer'].apply(strip_quotes).apply(clean_answer)

    # 3. Filtering logic: remove answers with < 3 sentences OR word count < 32
    df['sentence_count'] = df['answer'].astype(str).str.count(r'\.')
    df['word_count'] = df['answer'].astype(str).apply(lambda x: len(x.split()))
    
    original_count = len(df)
    # Keep only those that have >= 3 sentences AND >= 32 words
    df = df[(df['sentence_count'] >= 3) & (df['word_count'] >= 32)]
    print(f"Dropped {original_count - len(df)} QA pairs due to length constraints (<3 sentences or <32 words).")

    # 4. Handle Duplicates
    # Create a clean question for duplicate matching (strips brackets just for matching)
    df['match_question'] = df['question'].str.replace(r'^\[|\]$', '', regex=True).str.strip()
    
    # Calculate answer length
    df['ans_len'] = df['answer'].str.len()
    
    # Flag if original question had brackets
    df['has_brackets'] = df['question'].str.startswith('[') & df['question'].str.endswith(']')

    # Sort so that for any duplicate `match_question`:
    # - Longer answers come first (ans_len False ascending -> Descending)
    # - Non-bracketed questions come first (has_brackets True ascending -> False before True)
    df = df.sort_values(by=['ans_len', 'has_brackets'], ascending=[False, True])
    
    # Drop duplicates keeping the first occurrence
    original_len = len(df)
    df = df.drop_duplicates(subset=['match_question'], keep='first')
    new_len = len(df)
    print(f"Removed {original_len - new_len} duplicate questions.")

    # Cleanup temporary columns
    df = df.drop(columns=['match_question', 'ans_len', 'has_brackets', 'sentence_count', 'word_count'])

    # 5. Prune rows 301-314
    # We enforce exactly 300 rows at maximum to fulfill the "remove questions 301-314" request.
    if len(df) > 300:
        df = df.iloc[:300]
        print("Truncated dataset to 300 rows (removed rows 301+).")

    output_path = os.path.join(base_dir, 'datasets', 'fine-tuning', 'custom-dataset-archive', 'cleaned_merged_data_v2.csv')
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Cleaned dataset saved to {output_path}")

if __name__ == '__main__':
    main()
