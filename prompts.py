
SCENARIOS = [
    #{
        #"id": 1,
        #"scenario_name": "Double Charge Conflict",
        #"intent": "payment_issue",
        #"expected_satisfaction": "unsatisfied",
        #"expected_quality_score": 2,
        #"expected_mistakes": ["ignored_question", "no_resolution"],
        #"prompt_instruction": """
        #Сгенерируй диалог (5-6 реплик).
        #КОНТЕКСТ: У клиента дважды списали деньги за подписку.
        #ПОВЕДЕНИЕ АГЕНТА: Отвечает только сухими шаблонами, не говорит конкретно, когда вернут деньги.
        #ПОВЕДЕНИЕ КЛИЕНТА: В конце формально говорит 'спасибо', но чувствуется скрытое недовольство.
        #"""
   # },
    #{
        #"id": 2,
        #"scenario_name": "Account Access Rude Tone",
        #"intent": "technical_error",
        #"expected_satisfaction": "unsatisfied",
        #"expected_quality_score": 1,
        #"expected_mistakes": ["rude_tone"],
       # "prompt_instruction": """
        #Сгенерируй диалог. Кент не может зайти в аккаунт.
        #АГЕНТ: Хамит, говорит 'читайте инструкцию' и 'у нас всё работает, это у вас проблемы'.
        #КЛИЕНТ: В ярости, требует менеджера.
        #"""
    #},
    #{
     #   "id": 3,
      #  "scenario_name": "Successful Upgrade",
       # "intent": "feature_request",
        #"expected_satisfaction": "satisfied",
        #"expected_quality_score": 5,
        #"expected_mistakes": [],
        #"prompt_instruction": """
        #Сгенерируй диалог. Клиент хочет перейти на VIP-тариф.
        #АГЕНТ: Очень вежлив, быстро помогает, делает скидку.
        #КЛИЕНТ: Счастлив, благодарит в конце.
        #"""
    #},
    # --- СЮДА ТЫ МОЖЕШЬ ДОПИСЫВАТЬ НОВЫЕ БЛОКИ ---
    # Просто копируй структуру выше, меняй ID и текст в prompt_instruction

    {
    "id": 1,
        "scenario_name": "Payment Success Resolution",
        "intent": "payment_issue",
        "expected_satisfaction": "satisfied",
        "expected_quality_score": 5,
        "expected_mistakes": [],
        "prompt_instruction":
            """
             Сгенеруй діалог на українській мові (6-7 речень). Клієнт має проблеми з оплатою.
             КОНТЕКСТ: У клієнта виникає помилка при спробі оплати.
             АГЕНТ: Ввічливий, тактовний, оперативний, емпатичний та стрессостійкий. Дає чітке пояснення в чому може бути проблема.
             Пропонує конкретні кроки щоб вирішити: перевірити карту, спосіб оплати та просить повторити спробу. Допомогає вирішити.
             КЛІЄНТ: Дякує агенту, проблема вирішена тому кліент залишається задоволеним.
             """
    },
]