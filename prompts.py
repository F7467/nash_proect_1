# Добавь это в список SCENARIOS в файле prompts.py

  #  {
       # "id": 2,
        #"intent": "технічна помилка / доступ",
       #"expected_satisfaction": "unsatisfied",
        #"expected_quality_score":
        #"expected_mistakes": ["rude_tone", "incorrect_info"],
        #"prompt_instruction": """
        #Згенеруй діалог. Клієнт не може залогінитись в систему.
        #Агент замість допомоги каже: 'Це ваші проблеми, читайте інструкцію, у нас все працює'.
        #Агент відверто грубіянить (rude_tone).
        #Наприкінці клієнт вимагає покликати менеджера і каже, що напише скаргу.


# prompts.py — Твой пульт управления контентом

SCENARIOS = [
    {
        "id": 1,
        "scenario_name": "Double Charge Conflict",
        "intent": "payment_issue",
        "expected_satisfaction": "unsatisfied",
        "expected_quality_score": 2,
        "expected_mistakes": ["ignored_question", "no_resolution"],
        "prompt_instruction": """
        Сгенерируй диалог (5-6 реплик). 
        КОНТЕКСТ: У клиента дважды списали деньги за подписку. 
        ПОВЕДЕНИЕ АГЕНТА: Отвечает только сухими шаблонами, не говорит конкретно, когда вернут деньги.
        ПОВЕДЕНИЕ КЛИЕНТА: В конце формально говорит 'спасибо', но чувствуется скрытое недовольство.
        """
    },
    {
        "id": 2,
        "scenario_name": "Account Access Rude Tone",
        "intent": "technical_error",
        "expected_satisfaction": "unsatisfied",
        "expected_quality_score": 1,
        "expected_mistakes": ["rude_tone"],
        "prompt_instruction": """
        Сгенерируй диалог. Кент не может зайти в аккаунт. 
        АГЕНТ: Хамит, говорит 'читайте инструкцию' и 'у нас всё работает, это у вас проблемы'. 
        КЛИЕНТ: В ярости, требует менеджера.
        """
    },
    {
        "id": 3,
        "scenario_name": "Successful Upgrade",
        "intent": "feature_request",
        "expected_satisfaction": "satisfied",
        "expected_quality_score": 5,
        "expected_mistakes": [],
        "prompt_instruction": """
        Сгенерируй диалог. Клиент хочет перейти на VIP-тариф. 
        АГЕНТ: Очень вежлив, быстро помогает, делает скидку. 
        КЛИЕНТ: Счастлив, благодарит в конце.
        """
    },
    # --- СЮДА ТЫ МОЖЕШЬ ДОПИСЫВАТЬ НОВЫЕ БЛОКИ ---
    # Просто копируй структуру выше, меняй ID и текст в prompt_instruction
]