<h1 align="center">
  SKELAR AI TEST TASK
</h1>

<div align="center">
  <strong>Analysing AI</strong><br>
  ⚒️🤖💬
</div>

<div align="center"> 
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python&logoColor=white" alt="Python Version" />
  </a>
  </br>Даний проєкт автоматизує аналіз роботи служби підтримки. Він генерує датасет чатів між клієнтом та сапорт-агентом і оцінює якість роботи підтримки за допомогою LLM.
</div>

## Table of contents

* [Table of contents](#table-of-contents)
* [Prerequisites](#prerequisites)
* [Копіювання проєкту](#копіювання-проєкту)
* [Встановлення та налаштування](#встановлення-та-налаштування)
* [Запуск через Docker (Рекомендовано)](#запуск-через-docker-рекомендовано)
* [Структура проєкту](#структура-проєкту)

## 

Для того, щоб отримати копію цього проєкту на свій комп'ютер, виконайте команду в терміналі:
```bash
git clone https://github.com/ваш_username/nash_proect_1.git
```

## Prerequisites

Перед початком переконайтеся, що у вас встановлені:
* **Git** — [завантажити](https://git-scm.com/)
* **Python** — [завантажити](https://www.python.org/)
*Опціонально*
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
Створіть файл `.env` у корені проєкту та додайте ваші API ключі
```python
OPENAI_API_KEY=ваш_openai_ключ
GOOGLE_API_KEY=ваш_gemini_ключ
```

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
Скрипти запустятся послідовно
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

## Структура проєкту

* `generate.py`: Генератор діалогів. Створює вхідні дані для аналізу
* `analyze.py`: Аналізатор діалогів. Проводить оцінку та формує звіт.
* `prompts.py`: Логіка сценаріїв: типи клієнтів, поведінка агентів та інтенти.
* `output/`: Директорія для результатів. Містить `raw_data.json`, `analyzed_data.json` та *фінальний* `comparison_report.json`.
* `entrypoint.sh`: Скрипт автоматизації для Docker-контейнера.