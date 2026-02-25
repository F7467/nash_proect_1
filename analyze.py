import os
from pyexpat import model
import time
import json
from google import genai
from google.genai import types
from prompts import SCENARIOS
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAIkey = os.getenv("OPENAI_API_KEY")
GEMINIkey = os.getenv("GOOGLE_API_KEY")

if not OPENAIkey and not GEMINIkey:
    print("Ключі відсутні")

gemini_client = None
if GEMINIkey:
    genai.configure(api_key=GEMINIkey)

openai_client = None
if OPENAIkey:
    openai_client = OpenAI(api_key=OPENAIkey)

def analyze_dialogue():
    try:
        with open("test_chat.txt", "r", encoding="utf-8") as f:
            data = json.load(f)
            chat_content = data.get("dialogue", str(data))
    except FileNotFoundError:
        print("Помилка: Файл test_chat.txt не знайдено! Спочатку запустіть generate.py.")
        return
    except json.JSONDecodeError:
        print("Файл пустий або формат JSON пошкоджений.")
        return

    print("Аналізую останній діалог...")

    analysis_prompt = f"""
    Проаналізуй діалог між клієнтом та сапортом і виведи результат ТІЛЬКИ у форматі JSON.

    ДІАЛОГ ДЛЯ АНАЛІЗУ:
    {chat_content}

    JSON Стркуктура для відповіді:
    {{
        intent: "payment_issue" / "technical_error" / "account_access" / "tariff_question" / "refund" / "other",
        satisfaction: "satisfied" / "neutral" / "unsatisfied",
        quality_score: 1-5,
        expected_mistakes: [список помилок зі списку: incorrect_info, ignored_question, hallucinated_info, robotic_tone, rude_tone, too_short_reply, passive_agression, jargon_overload, contradictory_info, outdated_info, overly_verbose, assumption_based_reply, unnecessary_escalation, no_resolution, long_response_time. Якщо немає - пустий список]
    }}
    """
    try:
        response = gemini_client.models.generate_content(
            model = 'gemini-2.5-flash',
            contents = analysis_prompt,
            config = types.GenerateContentConfig(
                response_mime_type = "application/json",
            ),
        )

        result = json.loads(response.text)
        print(json.dumps(result, indent=4, ensure_ascii=False))
        
        with open("analysis_result.json", "w", encoding = "utf-8") as out:
            json.dump(result, out, indent=4, ensure_ascii = False)
            print("\nРезультат збережений в analysis_result.json")

    except Exception as e:
        print(f"Помилка при зверненні до ШІ: {e}")

if __name__ == "__main__":
    analyze_dialogue()
