# Changes

## ЛР 1. Dockerfile
- Приложение Habit Tracker (FastAPI): /health, /habits, /habits/{id}/check
- Хранение привычек в JSON-файле, путь задаётся через DATA_DIR
- Хороший Dockerfile и Dockerfile.bad с 4 плохими практиками
- .dockerignore, README с описанием практик

## ЛР 2. Docker Compose
- Файлы ЛР 1 перенесены в lab1/, compose-проект лежит в lab2/
- Сервисы: init (схема БД), app (FastAPI), db (PostgreSQL)
- docker-compose.yml: сборка образа habit-tracker:2.0, container_name, depends_on, volume, порт, command, healthcheck, сеть habit-net
- Переменные в lab2/.env, ответы на вопросы в README