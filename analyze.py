import os
import sys
import json
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINIkey = os.getenv("GOOGLE_API_KEY")

if not GEMINIkey:
    print("Ключа Gemini немає. Аналізувати нічим. Завершуємо роботу.")
    sys.exit(1)

# Налаштовуємо модель
genai.configure(api_key=GEMINIkey)
model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_all_dialogues():
    try:
        with open("output/raw_data.json", "r", encoding="utf-8") as f:
            dataset = json.load(f)
            print(f"Знайдено {len(dataset)} діалогів для аналізу. Опрацьовуємо...")
    except Exception as e:
        print(f"Помилка завантаження raw_data.json ({e}).")
        sys.exit(1)

    analyzed_results = []

    for item in dataset:
        scenario_id = item.get("id")
        dialog_text = item.get("dialog")

        if not dialog_text:
            print(f"Пропускаємо {scenario_id} (тексту діалогу нема).")
            continue

        print(f"Аналізуємо діалог {scenario_id}...")

        analysis_prompt = f"""
        Проаналізуй діалог між клієнтом та сапортом і виведи результат ТІЛЬКИ у форматі JSON.

        ДІАЛОГ ДЛЯ АНАЛІЗУ:
        {dialog_text}

        JSON Структура для відповіді (Ключі мають бути в подвійних лапках):
        {{
            "intent": "payment_issue" або "technical_error" або "account_access" або "tariff_question" або "refund_request" або "other",
            "satisfaction": "satisfied" або "neutral" або "unsatisfied",
            "quality_score": оцінка роботи сапорт-агента від 1 до 5 (числом),
            "agent_mistakes": ["incorrect_info", "ignored_question", "hallucinated_info", "robotic_tone", "rude_tone", "too_short_reply", "passive_agression", "jargon_overload", "contradictory_info", "outdated_info", "overly_verbose", "assumption_based_reply", "unnecessary_escalation", "no_resolution", "long_response_time", "data_privacy_violation"] (якщо помилок немає - порожній список [])
        }}
        """
        while True:
            try:
                response = model.generate_content(
                    analysis_prompt,
                    #response_mime_type для гарантованого JSON, temperature=0.1 для стабільності аналітики
                    generation_config={"response_mime_type": "application/json", "temperature": 0.1}
                )
                parsed_analysis = json.loads(response.text)
                item["ai_analysis"] = parsed_analysis
                analyzed_results.append(item)

                print(f"ID {scenario_id} оброоблено.")
                time.sleep(6)
                break

            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    print(f"Досягнено ліміту (429)! Чекаємо 60 секунд і надсилаємо {scenario_id}...")
                    time.sleep(60)
                else:
                    print(f"Критична помилка на ID {scenario_id} ({e})")
                    item["ai_analysis"] = {"error": str(e)}
                    analyzed_results.append(item)
                    break

    with open("output/analyzed_data.json", "w", encoding="utf-8") as out:
        json.dump(analyzed_results, out, indent=4, ensure_ascii=False)
        print("\nУсі дані успішно проаналізовані та збережені в analyzed_data.json!")


def compare_results():
    """
    Порівнюємо результати
    """
    print("\nПочинаємо порівняння...")

    try:
        with open("output/analyzed_data.json", "r", encoding="utf-8") as f:
            analyzed_data = json.load(f)
    except Exception as e:
        print(f"Не вдалось відкрити analyzed_data.json ({e})")
        sys.exit(1)

    comparison_results = []
    total_matches = 0
    total_fields_checked = 0

    for item in analyzed_data:
        scenario_id = item.get("id")
        ai_result = item.get("ai_analysis", {})

        if "error" in ai_result:
            print(f"Пропускаємо порівняння для ID {scenario_id} через помилку аналізу.")
            continue

        expected_intent = item.get("intent")
        expected_satisfaction = item.get("expected_satisfaction")
        expected_quality_score = item.get("expected_quality_score")
        expected_mistakes = set(item.get("agent_mistakes", []))

        ai_intent = ai_result.get("intent")
        ai_satisfaction = ai_result.get("satisfaction")
        ai_quality_score = ai_result.get("quality_score")
        ai_mistakes = set(ai_result.get("agent_mistakes", []))

        matches = 0
        differences = {}

        #  Intent
        total_fields_checked += 1
        if str(ai_intent) == str(expected_intent):
            matches += 1
            total_matches += 1
        else:
            differences["intent"] = {"expected": expected_intent, "ai_got": ai_intent}

        #Satisfaction
        total_fields_checked += 1
        if str(ai_satisfaction) == str(expected_satisfaction):
            matches += 1
            total_matches += 1
        else:
            differences["satisfaction"] = {"expected": expected_satisfaction, "ai_got": ai_satisfaction}

        # Quality Score
        total_fields_checked += 1
        if str(ai_quality_score) == str(expected_quality_score):
            matches += 1
            total_matches += 1
        else:
            differences["quality_score"] = {"expected": expected_quality_score, "ai_got": ai_quality_score}

        # Agent Mistakes
        total_fields_checked += 1
        if ai_mistakes == expected_mistakes:
            matches += 1
            total_matches += 1
        else:
            differences["agent_mistakes"] = {"expected": list(expected_mistakes), "ai_got": list(ai_mistakes)}

        comparison_results.append({
            "id": scenario_id,
            "expectation_reality_matches": matches,
            "differences": differences,
            "is_perfect_match": matches == 4
        })

    with open("output/comparison_report.json", "w", encoding="utf-8") as out:
        json.dump(comparison_results, out, indent=4, ensure_ascii=False)

    accuracy = (total_matches / total_fields_checked * 100) if total_fields_checked > 0 else 0
    print(f"Порівняння завершено! Звіт збережено у comparison_report.json.")
    print(f"Загальна точність аналізу ШІ: {accuracy:.2f}%")


if __name__ == "__main__":
    analyze_all_dialogues()
    compare_results()
