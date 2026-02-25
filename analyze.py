import os
import json
import time  # ДОДАЛИ TIME ДЛЯ ПАУЗ
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()
GEMINIkey = os.getenv("GOOGLE_API_KEY")

if not GEMINIkey:
    print("❌ Ключі відсутні! Завершую роботу.")
    exit()

genai.configure(api_key=GEMINIkey)
model = genai.GenerativeModel("gemini-2.0-flash")


def analyze_dialogue():
    try:
        with open("test_chat.txt", "r", encoding="utf-8") as f:
            chat_content = f.read()
            if not chat_content.strip():
                print("❌ Файл test_chat.txt пустий!")
                return
    except FileNotFoundError:
        print("❌ Помилка: Файл test_chat.txt не знайдено!")
        return

    print("🕵️‍♂️ Аналізую останній діалог...")

    analysis_prompt = f"""
    Проаналізуй діалог між клієнтом та сапортом і виведи результат ТІЛЬКИ у форматі JSON.

    ДІАЛОГ ДЛЯ АНАЛІЗУ:
    {chat_content}

    JSON Структура для відповіді (Ключі мають бути в подвійних лапках):
    {{
        "intent": "payment_issue" або "technical_error" або "account_access" або "tariff_question" або "refund_request" або "other",
        "satisfaction": "satisfied" або "neutral" або "unsatisfied",
        "quality_score": оцінка від 1 до 5 (числом),
        "expected_mistakes": ["incorrect_info", "ignored_question", "hallucinated_info", "robotic_tone", "rude_tone", "too_short_reply", "passive_agression", "jargon_overload", "contradictory_info", "outdated_info", "overly_verbose", "assumption_based_reply", "unnecessary_escalation", "no_resolution", "long_response_time"] (якщо немає - порожній список [])
    }}
    """

    # === ТОЙ САМИЙ БРОНЕБІЙНИЙ ЦИКЛ ===
    while True:
        try:
            response = model.generate_content(
                analysis_prompt,
                generation_config={"response_mime_type": "application/json"}
            )

            result = json.loads(response.text)
            print(json.dumps(result, indent=4, ensure_ascii=False))

            with open("analysis_result.json", "w", encoding="utf-8") as out:
                json.dump(result, out, indent=4, ensure_ascii=False)
                print("\n✅ Результат збережений в analysis_result.json")

            # Якщо все пройшло успішно, ламаємо цикл і йдемо далі!
            break

        except Exception as e:
            error_msg = str(e)
            # Якщо Гугл знову кидається 429 помилкою
            if "429" in error_msg or "quota" in error_msg.lower():
                print(f"🛑 Гугл душить лімітами (429)! Спимо 60 секунд і добиваємо його...")
                time.sleep(60)
            else:
                # Якщо помилка в чомусь іншому (наприклад, ШІ віддав кривий JSON)
                print(f"❌ Критична помилка (не ліміти): {e}")
                break


if __name__ == "__main__":
    analyze_dialogue()