import os
import sys
import time
import json
from pathlib import Path

backend_dir = Path(r'D:\MCA Sage Uni\Semester-3\Project Ideas\ArogyaMitra\fastapi_backend')
sys.path.insert(0, str(backend_dir))

os.environ['HF_HOME'] = str(backend_dir / 'models' / 'huggingface')
os.environ['TRANSFORMERS_CACHE'] = str(backend_dir / 'models' / 'huggingface')

import asyncio
from app.utils.language import detect_indic_language
from app.services.translation_service import translation_service
from app.services.llm_service import get_llm_service

async def run_sync_benchmark():
    test_cases = [
        {
            'language_name': 'Hindi (Devanagari)',
            'target_tag': 'hin_Deva',
            'query': 'मुझे पिछले 3 दिनों से तेज़ बुखार, सिरदर्द और ठंड लग रही है। मुझे क्या करना चाहिए?'
        },
        {
            'language_name': 'Bengali (Bangla)',
            'target_tag': 'ben_Beng',
            'query': 'আমার গত ৩ দিন ধরে খুব জ্বর, মাথা ব্যথা এবং পেটে ব্যথা হচ্ছে। আমার কী করা উচিত?'
        },
        {
            'language_name': 'Marathi (Devanagari)',
            'target_tag': 'mar_Deva',
            'query': 'मला गेल्या ३ दिवसांपासून तीव्र ताप, डोकेदुखी आणि सर्दी आहे. मी काय केले पाहिजे?'
        }
    ]

    llm_service = get_llm_service()
    await translation_service._load_models()
    llm_service._initialize_model()

    results = []
    print('=== INDIC STACK MULTI-LANGUAGE LATENCY BENCHMARK ===\n')

    for tc in test_cases:
        lang_name = tc['language_name']
        raw_query = tc['query']
        
        t0 = time.time()
        
        # Stage 1: IndicLID
        t1 = time.time()
        det_lang = detect_indic_language(raw_query)
        t_lid = round(time.time() - t1, 4)
        
        # Stage 2: Indic -> English Translation
        t2 = time.time()
        en_prompt = await translation_service.translate(raw_query, src_lang=det_lang, tgt_lang='eng_Latn')
        t_trans_in = round(time.time() - t2, 3)
        
        # Stage 3: Qwen 3.5 2B LLM
        t3 = time.time()
        llm_out = llm_service.generate_response(
            prompt=en_prompt,
            target_intent='indic_pipeline_benchmark',
            max_tokens=150,
            repeat_penalty=1.15
        )
        en_resp = llm_out['response']
        t_llm = round(time.time() - t3, 3)
        
        # Stage 4: English -> Indic Translation
        t4 = time.time()
        final_resp = await translation_service.translate(en_resp, src_lang='eng_Latn', tgt_lang=det_lang)
        t_trans_out = round(time.time() - t4, 3)
        
        t_total = round(time.time() - t0, 3)
        
        entry = {
            'language_name': lang_name,
            'detected_language': det_lang,
            'raw_query': raw_query,
            'translated_prompt': en_prompt,
            'english_response': en_resp,
            'final_response': final_resp,
            'stage_breakdown_sec': {
                'indic_lid': t_lid,
                'indic_to_en_trans': t_trans_in,
                'qwen35_2b_llm': t_llm,
                'en_to_indic_trans': t_trans_out
            },
            'total_pipeline_time_sec': t_total
        }
        results.append(entry)
        
        # Write log entry
        log_jsonl = backend_dir / 'logs' / 'llm_evaluations.jsonl'
        log_data = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'pipeline_stage': 'ORCHESTRATED_INDIC_STACK',
            'language_name': lang_name,
            'detected_language': det_lang,
            'prompt': raw_query,
            'translated_prompt': en_prompt,
            'english_response': en_resp,
            'response': final_resp,
            'execution_time_sec': t_llm,
            'total_pipeline_time_sec': t_total,
            'stage_breakdown_sec': entry['stage_breakdown_sec'],
            'target_intent': 'indic_pipeline_benchmark'
        }
        with open(log_jsonl, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_data, ensure_ascii=False) + '\n')
            
        print(f'Done {lang_name} | Total: {t_total}s | LID: {t_lid}s | In-Trans: {t_trans_in}s | LLM: {t_llm}s | Out-Trans: {t_trans_out}s')

    out_file = backend_dir / 'logs' / 'indic_benchmark_results.json'
    out_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
    print('\nBenchmark complete!')

asyncio.run(run_sync_benchmark())
