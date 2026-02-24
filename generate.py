import os
import json
import time
from dotenv import load_dotenv
from prompts import SCENARIOS

# Нові правильні імпорти
from openai import OpenAI
import google.generativeai as genai

# Повертаємо нашу перевірену і швидку модель
MODEL_GEMINI = "gemini-2.5-flash"
TEMPERATURE = 0.2

load_dotenv()

# Тягнемо правильні назви з твого .env
OPENAIkey = os.getenv("OPENAI_API_KEY")
GEMINIkey = os.getenv("GOOGLE_API_KEY")

if not OPENAIkey and not GEMINIkey:
    print("ключів нема, ребята. ші не працює щас")

# Налаштовуємо Gemini
if GEMINIkey:
    genai.configure(api_key=GEMINIkey)
    gemini_model = genai.GenerativeModel(MODEL_GEMINI)

# Налаштовуємо OpenAI (новий синтаксис)
if OPENAIkey:
    openai_client = OpenAI(api_key=OPENAIkey)


def generate_dialog(prompt_instruction: str) -> str:
    """
  спочатку пробуємо опенаі, якщо падає або немає кредитів - геміні.
  """
    if OPENAIkey:
        try:
            # Сучасний виклик OpenAI
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt_instruction}],
                temperature=TEMPERATURE
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"опенаі гамно не работає: {e}. пробуєм геміні")

    if GEMINIkey:
        try:
            # Виклик Gemini
            response = gemini_model.generate_content(
                prompt_instruction,
                generation_config={"temperature": TEMPERATURE}
            )
            return response.text.strip()
        except Exception as e:
            print(f"геміні тоже гамно не работає: {e}.")
            return "не вдалось згенерувати діалог"

    return "обидві ші недоступні."


def main():
    results = []

    for scenario in SCENARIOS:
        scenario_id = scenario.get("id")
        if not scenario.get("prompt_instruction"):
            print(f"скіпаєм {scenario_id} бо там нема промпта.")
            continue

        try:
            print(f"генерую сценарій {scenario_id} ...")
            dialog = generate_dialog(scenario["prompt_instruction"])

            results.append({
                "id": scenario_id,
                "scenario_name": scenario.get("scenario_name"),
                "intent": scenario.get("intent"),
                "expected_satisfaction": scenario.get("expected_satisfaction"),
                "expected_quality_score": scenario.get("expected_quality_score"),
                "expected_mistakes": scenario.get("expected_mistakes"),
                "dialog": dialog
            })
            # Трохи збільшив паузу, щоб Google точно не плювався лімітами
            time.sleep(6)

        except Exception as e:
            print(f"сценарій {scenario_id} фігня: {e}")
            continue

    with open("raw_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print("raw_data.json збережена")


if __name__ == "__main__":
    main()