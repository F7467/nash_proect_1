<h1 align="center">
  SKELAR AI TEST TASK
</h1>

<div align="center">
  <strong>Analysing AI</strong><br>
  ⚒️🤖💬
</div>

<div align="center"> 
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)">
  </a>
  <a>
    <img src="https://img.shields.io/badge/Google%20Gemini-886FBF?logo=googlegemini&logoColor=fff">
  </a>
  </br>Даний проєкт автоматизує аналіз роботи служби підтримки. Він генерує датасет чатів між клієнтом та сапорт-агентом і оцінює якість роботи підтримки за допомогою LLM.
</div>

## Table of contents

* [Table of contents](#table-of-contents)
* [Tech stack](#tech-stack)
* [Prerequisites](#prerequisites)
* [Копіювання проєкту](#копіювання-проєкту)
* [Встановлення та налаштування](#встановлення-та-налаштування)
* [Запуск через Docker (Рекомендовано)](#запуск-через-docker-рекомендовано)
* [Змінна кількості діалогів](#змінна-кількості-діалогів)
* [Результати аналізу](#результати-аналізу)
* [Структура проєкту](#структура-проєкту)

## Tech stack

* Python
* Gemini API/Open AI
* JSON
* Enviromental Variables (.env)
* Docker (optional)


## Prerequisites

Перед початком переконайтеся, що у вас встановлені:
* **Git** — [завантажити](https://git-scm.com/)
* **Python** — [завантажити](https://www.python.org/).

*Опціонально*:
* **Docker** — [завантажити](https://www.docker.com/)

## Копіювання проєкту

* В консолі пропишіть команду
```bash
git clone https://github.com/F7467/nash_proect_1.git
```
* Після чого перейдіть в папку проєкту
```bash
cd nash_proect_1
```

## Встановлення та налаштування

0. **Налаштування API ключів**  
Створіть файл `.env` (або приберіть `.example` з файлу `.env.example`) у корені проєкту та додайте ваші API ключі. 
```python
OPENAI_API_KEY=ваш_openai_ключ
GOOGLE_API_KEY=ваш_gemini_ключ
```
> *ВАЖЛИВО*: переконайтеся, що навколо знаку «дорівнює» немає пробілів

1. **Налаштуйте `venv` та акивуйте його**
```bash
python -m venv .venv
```

* *Windows (PowerShell)*: 
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
* *Mac/Linux*: 
   ```bash
   source .venv/bin/activate
   ```

2. **Встановіть необхідні бібліотеки**
```bash
pip install -r requirements.txt
```

3. **Запустіть**  
Скрипти запустятся послідовно.
> *ВАЖЛИВО*: generate.py ОБОВʼЯЗКОВО має запуститися та завершитися перед запуском analyze.py
```bash
python generate.py && python analyze.py
```

## Запуск через Docker (Рекомендовано) 

1. Зберіть образ
```bash
docker build -t ai-test-task .
```

2. Запустіть контейнер з виводом результатів
```bash
docker run --env-file .env -v $(pwd)/output:/app/output ai-test-task
```

## Змінна кількості діалогів

Ви можете налаштувати обсяг згенерованих даних у файлі `generate.py`
* `TOTAL_DIALOGS` змінна, що визначає кількість діалогів що будуть згенеровані. За замовчуванням встановлено 20.
* Як змінити:
1. Відкрийте файл `generate.py`
2. Перейдіть на рядок `70`
3. Замініть число на потрібне

> *ВАЖЛИВО*: збільшення кількості діалогів призведе до більшої витрати токенів API-ключів

## Результати аналізу
Після завершення роботи обох скриптів у папці /output з'являться наступні дані:
* `raw_data.json`: згенеровані діалоги з очікуваними оцінками
* `analyzed_data.json`: Результат аналізу кожного діалогу моделлю Gemini (Intent, Satisfaction, Score, Mistakes).
* `comparison_report.json`: фінальний звіт, що порівнює очікувані результати сценарію з реальними висновками ШІ.

## Структура проєкту

* `generate.py`: генератор діалогів. Створює вхідні дані для аналізу
* `analyze.py`: аналізатор діалогів. Проводить оцінку та формує звіт
* `prompts.py`: логіка сценаріїв: типи клієнтів, поведінка агентів та інтенти
* `output/`: директорія для результатів. Сюди зберігаються `raw_data.json`, `analyzed_data.json` та *фінальний* `comparison_report.json`
* *`raw_data.json`* — початкові діалоги
* *`analyzed_data.json`* — детальні висновки ШІ по кожному чату.
* *`comparison_report.json`* — головний результат проєкту, що містить зведену статистику та порівняльний аналіз
* `entrypoint.sh`: скрипт автоматизації для Docker-контейнера