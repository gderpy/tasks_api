# Tasks API
Мини-сервис на FastAPI для портфолио.

## Быстрый старт
poetry install
poetry run uvicorn app.main:app --reload

## Проверка
GET /health, GET /version
poetry run pytest
