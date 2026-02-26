#!/bin/bash
set -e

echo "Запуск Етапу 1: Генерація діалогів..."
python generate.py

echo "Запуск Етапу 2: Аналіз діалогів..."
python analyze.py

echo "Процес завершено успішно!"