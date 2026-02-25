import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAIkey = os.getenv("OPENAI_API_KEY")
GEMINIkey = os.getenv("GOOGLE_API_KEY")

model = genai.GenerativeModel(
    'gemini-2.5-flash',
    generation_config={"response_mime_type": "application/json"}
)
while True:
    try:
        with open("test_chat.txt", "r", encoding="utf-8") as f:
            chat_content = f.read()
    except FileNotFoundError:
        print("Помилка: Файл test_chat.txt не знайдено! Спочатку запустіть generate.py.")
        exit()

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
        agent_mistakes: [список помилок зі списку: incorrect_info, ignored_question, unnecessary_escalation, no_resolution, long_response_time, "data_privacy_violation". Якщо немає - пустий список]
    }}
    """

    response = model.generate_content(analysis_prompt)

    print("\n---Результат аналізу діалогу---")
    print(response.text)

    time.sleep(5)