# Инструкция по запуску

Проект состоит из двух независимых частей: backend (FastAPI, Python) и
frontend (React, Vite). Для локальной разработки оба запускаются
одновременно на разных портах.

## Требования

- Python 3.9+ (проверено на 3.9.6)
- Node.js 20.18+ и npm (проверено на Node v20.18.0 / npm 10.8.2)

## Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Заполнить SQLite базу контентом курса (идемпотентно, можно перезапускать)
python -m app.seed.seed

# Запустить сервер
uvicorn app.main:app --reload --port 8000
```

Проверка: [http://localhost:8000/api/health](http://localhost:8000/api/health)
должен вернуть `{"status": "ok"}`. Интерактивная документация API (Swagger
UI, автоматически сгенерированная FastAPI) — на
[http://localhost:8000/docs](http://localhost:8000/docs).

## Frontend

В отдельном терминале:

```bash
cd frontend
npm install
npm run dev
```

Откройте [http://localhost:5173](http://localhost:5173). Vite dev-сервер
проксирует все запросы `/api/*` на backend (`localhost:8000`), см.
`frontend/vite.config.js`.

> Примечание: в `npm audit` может отображаться moderate/high advisory для
> `esbuild` — он касается только dev-сервера (риск для локальной разработки
> на доверенной машине отсутствует) и не влияет на production-сборку
> (`npm run build`).

## Тесты

Backend (pytest, 45 тестов — unit-тесты чекера автопроверки + integration
тесты эндпоинтов, включая провокационные edge cases):

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

Frontend smoke-тесты (Playwright, реальный браузер Chromium):

```bash
cd frontend
npx playwright install chromium   # один раз
npx playwright test
```

Оба набора тестов одной командой (поднимает backend/frontend, если они ещё
не запущены):

```bash
./scripts/run_all_tests.sh
```

## Структура портов

| Сервис | Порт | Назначение |
|---|---|---|
| Backend (uvicorn) | 8000 | REST API, Swagger UI на `/docs` |
| Frontend (Vite) | 5173 | Веб-интерфейс курса |
