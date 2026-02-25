import os
import json
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINIkey = os.getenv("GOOGLE_API_KEY")

if not GEMINIkey:
    print("❌ Ключі відсутні! Завершую роботу.")
    exit()

genai.configure(api_key=GEMINIkey)

# ТВОЯ ВИМОГА: ТІЛЬКИ 2.5-FLASH
model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_all_dialogues():
    # 1. Читаємо весь наш згенерований датасет
    try:
        with open("raw_data.json", "r", encoding="utf-8") as f:
            dataset = json.load(f)
            print(f"📂 Знайдено {len(dataset)} діалогів для аналізу!")
    except FileNotFoundError:
        print("❌ Помилка: Файл raw_data.json не знайдено!")
        return
    except json.JSONDecodeError:
        print("❌ Помилка: raw_data.json пошкоджений або пустий.")
        return

    analyzed_results = []

    # 2. Проходимося по кожному діалогу
    for item in dataset:
        scenario_id = item.get("id")
        dialog_text = item.get("dialog")

        if not dialog_text:
            print(f"⚠️ Скіпаємо ID {scenario_id} - там немає тексту діалогу.")
            continue

        print(f"🕵️‍♂️ Аналізую діалог ID {scenario_id}...")

        analysis_prompt = f"""
        Проаналізуй діалог між клієнтом та сапортом і виведи результат ТІЛЬКИ у форматі JSON.

        ДІАЛОГ ДЛЯ АНАЛІЗУ:
        {dialog_text}

        JSON Структура для відповіді (Ключі мають бути в подвійних лапках):
        {{
            "intent": "payment_issue" або "technical_error" або "account_access" або "tariff_question" або "refund_request" або "other",
            "satisfaction": "satisfied" або "neutral" або "unsatisfied",
            "quality_score": оцінка від 1 до 5 (числом),
            "expected_mistakes": ["incorrect_info", "ignored_question", "hallucinated_info", "robotic_tone", "rude_tone", "too_short_reply", "passive_agression", "jargon_overload", "contradictory_info", "outdated_info", "overly_verbose", "assumption_based_reply", "unnecessary_escalation", "no_resolution", "long_response_time"] (якщо немає - порожній список [])
        }}
        """

        # 3. Бронебійний цикл для кожного запиту
        while True:
            try:
                response = model.generate_content(
                    analysis_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )

                # Розшифровуємо відповідь ШІ
                parsed_analysis = json.loads(response.text)

                # Записуємо результати аналізу всередину нашого об'єкта
                item["ai_analysis"] = parsed_analysis
                analyzed_results.append(item)

                print(f"✅ ID {scenario_id} успішно проаналізовано!")
                time.sleep(6)  # Нормальна пауза, щоб не бісити Гугл відразу
                break  # Виходимо з while і йдемо до наступного ID

            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    print(f"🛑 Гугл виставив блок (429)! Спимо 60 секунд і добиваємо ID {scenario_id}...")
                    time.sleep(60)
                else:
                    print(f"❌ Критична помилка на ID {scenario_id}: {e}")
                    # Якщо сталася якась інша дичина, записуємо помилку і йдемо далі
                    item["ai_analysis"] = {"error": str(e)}
                    analyzed_results.append(item)
                    break

    # 4. Зберігаємо все у новий фінальний файл
    with open("analyzed_data.json", "w", encoding="utf-8") as out:
        json.dump(analyzed_results, out, indent=4, ensure_ascii=False)
        print("\n🎉 УСІ ДАНІ УСПІШНО ПРОАНАЛІЗОВАНІ ТА ЗБЕРЕЖЕНІ В analyzed_data.json!")


if __name__ == "__main__":
    analyze_all_dialogues()