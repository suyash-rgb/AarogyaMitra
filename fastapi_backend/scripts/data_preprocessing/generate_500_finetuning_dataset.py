import pandas as pd
import ast
import random

file_path = r'D:\MCA Sage Uni\Semester-3\Project Ideas\ArogyaMitra\fastapi_backend\datasets\fine-tuning\custom-dataset-archive\cleaned_merged_data_v2.csv'
df = pd.read_csv(file_path, encoding='utf-8-sig')

# --- 1. Score the Dataset ---
def calculate_quality_score(answer):
    ans_str = str(answer)
    word_count = len(ans_str.split())
    sentence_count = ans_str.count('.')
    punctuation_count = ans_str.count(',') + ans_str.count(':') + ans_str.count(';')
    
    # Heuristic for "detailed step-by-step instructions"
    score = (word_count * 0.5) + (sentence_count * 5) + (punctuation_count * 2)
    return score

df['quality_score'] = df['answer'].apply(calculate_quality_score)
df_sorted = df.sort_values(by='quality_score', ascending=False)

# Select Top 50
top_50 = df_sorted.head(50)

# --- 2. Dynamic Oversampling ---
final_rows = []

# Fallback robust templates
fallback_templates = [
    "How do I treat {}?",
    "What is the first aid for {}?",
    "What should I do in case of {}?",
    "Can you provide treatment steps for {}?",
    "Please tell me the protocol for {}?",
    "Help, what is the remedy for {}?",
    "What are the emergency steps for {}?",
    "How to manage {} at home?",
    "What is the procedure for {}?",
    "How can I help someone with {}?"
]

for idx, row in top_50.iterrows():
    ans = row['answer']
    raw_q = str(row['question']).strip()
    
    variants = []
    # Attempt to parse the array format
    if raw_q.startswith('[') and raw_q.endswith(']'):
        try:
            parsed = ast.literal_eval(raw_q)
            if isinstance(parsed, list):
                variants = parsed
        except:
            variants = [raw_q]
    else:
        variants = [raw_q]
        
    # Filter sensible variants (length >= 3 words)
    valid_variants = [v for v in variants if len(str(v).split()) >= 3]
    
    # If no valid variants, extract a base condition name (very basic heuristic) 
    # and synthetically generate from templates
    if not valid_variants:
        # Extract last word or use whole string if short
        base_cond = raw_q.split()[-1].replace('?', '').replace(']', '').replace('"', '')
        if len(base_cond) < 3: base_cond = "this condition"
        valid_variants = [t.format(base_cond) for t in fallback_templates]
        
    # Generate exactly 10 rows for this answer using round-robin on the variants
    for i in range(10):
        chosen_q = valid_variants[i % len(valid_variants)]
        
        # Clean up any residual brackets/quotes just in case
        chosen_q = chosen_q.replace('[', '').replace(']', '').replace('"', '').strip()
        
        final_rows.append({
            'question': chosen_q,
            'answer': ans,
            'source_score': row['quality_score'] # Just for analysis if needed
        })

final_df = pd.DataFrame(final_rows)

# Shuffle the dataset to ensure conditions are completely mixed
final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to the new file
output_path = r'D:\MCA Sage Uni\Semester-3\Project Ideas\ArogyaMitra\fastapi_backend\datasets\fine-tuning\custom-dataset-archive\500_custom_finetuning_dataset.csv'
final_df[['question', 'answer']].to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"Extraction and Augmentation Complete!")
print(f"Top 50 conditions selected from original dataset.")
print(f"10x dynamic variant oversampling applied.")
print(f"Total Rows generated: {len(final_df)}")
print(f"Dataset successfully saved to: {output_path}")

# Preview some of the diversity
print("-" * 50)
print("Preview of random rows to verify diversity:")
print(final_df.head(10)[['question', 'answer']])
