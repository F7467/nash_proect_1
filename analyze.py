import os
import json
import time
from dotenv import load_dotenv
import google.generativeai as genai
from prompts import SCENARIOS

from openai import OpenAI

from generate import OPENAIkey
MODEL_GEMINI = "gemini-2.5-flash"

load_dotenv()
GEMINIkey = os.getenv("GOOGLE_API_KEY")
OPENAIkey = os.getenv("OPENAI_API_KEY")

if not GEMINIkey:
    print(" Ключі відсутні! Завершую роботу.")
    #exit()

genai.configure(api_key=GEMINIkey)

model = genai.GenerativeModel("gemini-2.5-flash")

if not OPENAIkey and not GEMINIkey:
    print("FATAL ERROR: ДОСТУП ДО ДВУХ ШІ ЗАРАЗ ВІДСУТНІЙ!")
    exit()

if GEMINIkey:
    genai.configure(api_key=GEMINIkey)
    gemini_model = genai.GenerativeModel(MODEL_GEMINI)

if OPENAIkey:
    openai_client = OpenAI(api_key=OPENAIkey)

def analyze_all_dialogues():
    try:
        with open("raw_data.json", "r", encoding="utf-8") as f:
            dataset = json.load(f)
            print(f" Знайдено {len(dataset)} діалогів для аналізу!")
    except FileNotFoundError:
        print(" Помилка: Файл raw_data.json не знайдено!")
        return
    except json.JSONDecodeError:
        print(" Помилка: raw_data.json пошкоджений або пустий.")
        return

    analyzed_results = []

    for item in dataset:
        scenario_id = item.get("id")
        dialog_text = item.get("dialog")

        if not dialog_text:
            print(f" Скіпаємо ID {scenario_id} - там немає тексту діалогу.")
            continue

        print(f" Аналізую діалог ID {scenario_id}...")

        analysis_prompt = f"""
        Проаналізуй діалог між клієнтом та сапортом і виведи результат ТІЛЬКИ у форматі JSON.

        ДІАЛОГ ДЛЯ АНАЛІЗУ:
        {dialog_text}

        JSON Структура для відповіді (Ключі мають бути в подвійних лапках):
        {{
            "intent": "payment_issue" або "technical_error" або "account_access" або "tariff_question" або "refund_request" або "other",
            "satisfaction": "satisfied" або "neutral" або "unsatisfied",
            "quality_score": оцінка від 1 до 5 (числом),
            "expected_mistakes": ["incorrect_info", "ignored_question", "hallucinated_info", "robotic_tone", "rude_tone", "too_short_reply", "passive_agression", "jargon_overload", "contradictory_info", "outdated_info", "overly_verbose", "assumption_based_reply", "unnecessary_escalation", "no_resolution", "long_response_time", "data_privacy_violation"] (якщо немає - порожній список [])
        }}
        """
        while True:
            try:
                response = model.generate_content(
                    analysis_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                parsed_analysis = json.loads(response.text)
                item["ai_analysis"] = parsed_analysis
                analyzed_results.append(item)

                print(f" ID {scenario_id} успішно проаналізовано!")
                time.sleep(6) 
                break  

            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    print(f" Гугл виставив блок (429)! Спимо 60 секунд і добиваємо ID {scenario_id}...")
                    time.sleep(60)
                else:
                    print(f" Критична помилка на ID {scenario_id}: {e}")
                    item["ai_analysis"] = {"error": str(e)}
                    analyzed_results.append(item)
                    break

    with open("analyzed_data.json", "w", encoding="utf-8") as out:
        json.dump(analyzed_results, out, indent=4, ensure_ascii=False)
        print("\n УСІ ДАНІ УСПІШНО ПРОАНАЛІЗОВАНІ ТА ЗБЕРЕЖЕНІ В analyzed_data.json!")

def compare_results(analyzed_file="analyzed_data.json", prompts_file="prompts.json", output_file="comparison_report.json"):
    """
    Порівнює результати ШІ з очікуваними (еталонними) даними.
    """
    print("\n Починаю порівняння з еталонними промптами...")
    
    try:
        with open(analyzed_file, "r", encoding="utf-8") as f:
            analyzed_data = json.load(f)
        
        with open(prompts_file, "r", encoding="utf-8") as f:
            prompts_data = json.load(f)
            
    except FileNotFoundError as e:
        print(f" Помилка завантаження файлів для порівняння: {e}")
        return

    prompts_dict = {item["id"]: item for item in prompts_data}
    comparison_results = []
    
    total_matches = 0
    total_fields_checked = 0

    for item in analyzed_data:
        scenario_id = item.get("id")
        ai_result = item.get("ai_analysis", {})
        
        if "error" in ai_result:
            continue

        expected_result = prompts_dict.get(scenario_id, {}).get("expected", {})
        
        if not expected_result:
            print(f" Не знайдено еталонних даних (очікувань) для ID {scenario_id}")
            continue

        keys_to_compare = ["intent", "satisfaction", "quality_score"]
        matches = 0
        differences = {}

        for key in keys_to_compare:
            total_fields_checked += 1
            if str(ai_result.get(key)) == str(expected_result.get(key)):
                matches += 1
                total_matches += 1
            else:
                differences[key] = {
                    "expected": expected_result.get(key),
                    "ai_got": ai_result.get(key)
                }

        total_fields_checked += 1
        ai_mistakes = set(ai_result.get("expected_mistakes", []))
        expected_mistakes = set(expected_result.get("expected_mistakes", []))
        
        if ai_mistakes == expected_mistakes:
            matches += 1
            total_matches += 1
        else:
            differences["expected_mistakes"] = {
                "expected": list(expected_mistakes),
                "ai_got": list(ai_mistakes)
            }

        comparison_results.append({
            "id": scenario_id,
            "expectation_reality_matches": matches,  
            "differences": differences,
            "is_perfect_match": matches == 4
        })

    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(comparison_results, out, indent=4, ensure_ascii=False)
    
    accuracy = (total_matches / total_fields_checked * 100) if total_fields_checked > 0 else 0
    print(f" Порівняння завершено! Збережено у {output_file}.")
    print(f" Загальна точність моделі: {accuracy:.2f}%")

if __name__ == "__main__":
    analyze_all_dialogues()