import os
import sys
import json
import time
from dotenv import load_dotenv

from openai import OpenAI
import google.generativeai as genai

from prompts import create_random_scenario

MODEL_GEMINI = "gemini-2.5-flash"
TEMPERATURE = 0.2

load_dotenv()

OPENAIkey = os.getenv("OPENAI_API_KEY")
GEMINIkey = os.getenv("GOOGLE_API_KEY")

if not OPENAIkey and not GEMINIkey:
    print("Немає ключів для OpenAI і Gemini.")
    sys.exit(1)

if GEMINIkey:
    genai.configure(api_key=GEMINIkey)
    gemini_model = genai.GenerativeModel(MODEL_GEMINI)

if OPENAIkey:
    openai_client = OpenAI(api_key=OPENAIkey)


def generate_dialog(prompt_instruction: str) -> str:
    """ Використовуємо OpenAI. """
    if OPENAIkey:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt_instruction}],
                temperature=TEMPERATURE
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Помилка в OpenAI ({e}). Використовуємо Gemini...")

    if GEMINIkey:
        while True:
            try:
                response = gemini_model.generate_content(
                    prompt_instruction,
                    generation_config={"temperature": TEMPERATURE}
                )
                return response.text.strip()
            except Exception as e:
                error_msg = str(e)
                # помилка ліміту (429)
                if "429" in error_msg or "quota" in error_msg.lower():
                    print(f"Досягнено ліміту (429)! Чекаємо 60 секунд і надсилаємо цей же сценарій...")
                    time.sleep(60)
                else:
                    # інша помилка (наприклад, інтернет відпав)
                    print(f"Помилка в Gemini ({e}). Не вдалося згенерувати діалог.")
                    sys.exit(1)

    print("Обидві ШІ недоступні.")
    sys.exit(1)


def main():
    results = []
    TOTAL_DIALOGS = 20  # ліміт на день, щоб не зловити бан по API
                        # README

    for i in range(1, TOTAL_DIALOGS + 1):
        scenario = create_random_scenario(i)
        scenario_id = scenario.get("id")

        if not scenario.get("prompt_instruction"):
            print(f"Пропускаємо сценарій {scenario_id} (нема промпта).")
            continue

        try:
            print(f"Генеруємо сценарій {scenario_id} з 20 (Інтент: {scenario.get('intent')}) ...")
            dialog = generate_dialog(scenario["prompt_instruction"])

            if not dialog:
                print(f"ШІ повернула порожню відповідь на сценарій {scenario_id}. Виходимо.")
                sys.exit(1)

            results.append({
                "id": scenario_id,
                "scenario_name": scenario.get("scenario_name"),
                "intent": scenario.get("intent"),
                "expected_satisfaction": scenario.get("expected_satisfaction"),
                "expected_quality_score": scenario.get("expected_quality_score"),
                "agent_mistakes": scenario.get("agent_mistakes", []),  # Ключ під вимоги ТЗ
                "dialog": dialog
            })
            print(f"Сценарій {scenario_id} успішно згенеровано.")
            time.sleep(5)

        except Exception as e:
            print(f"Сценарій {scenario_id} звершився з помилкою ({e}).")
            continue

    with open("output/raw_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Готово! raw_data.json збережена. Успішно згенеровано унікальних діалогів: {len(results)}")


if __name__ == "__main__":
    main()
