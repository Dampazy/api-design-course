# Проектирование API — интерактивная учебная платформа

Учебная веб-платформа для изучения принципов проектирования REST API:
6 теоретических блоков, 18 практических заданий с автопроверкой ответов и
итоговый тест. Backend на FastAPI, frontend на React.

**Репозиторий:** [github.com/Dampazy/api-design-course](https://github.com/Dampazy/api-design-course)
**Демо (после подключения к Render):** см. [docs/DEPLOY.md](docs/DEPLOY.md)

## Реквизиты практики

- **Тема:** «Создание интерактивных методических материалов по
  проектированию API»
- **Обучающийся:** Вангонен Артём Вадимович
- **Направление подготовки:** 09.03.03 Прикладная информатика
  (профиль: интеллектуальные инфокоммуникационные технологии)
- **Вид/тип практики:** учебная, ознакомительная
- **Место прохождения:** ФГАОУ ВО «СПбПУ», Институт компьютерных наук и
  кибербезопасности, Высшая школа программной инженерии
- **Руководитель практической подготовки:** Жаранова Анастасия Олеговна
- **Сроки практики:** 10.06.2026 – 08.07.2026

## Быстрый старт

```bash
# Backend
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m app.seed.seed
uvicorn app.main:app --reload --port 8000

# Frontend (в отдельном терминале)
cd frontend
npm install
npm run dev
```

Откройте [http://localhost:5173](http://localhost:5173). Подробности —
в [docs/SETUP.md](docs/SETUP.md).

## Структура репозитория

```
backend/    — FastAPI-приложение, автопроверка ответов, тесты (pytest)
frontend/   — React SPA, страницы теории/практики/прогресса, Playwright-тесты
docs/       — методические материалы и отчёт по практике
scripts/    — scripts/run_all_tests.sh — запуск всех тестов одной командой
```

## Документация

- [docs/SETUP.md](docs/SETUP.md) — подробная инструкция по запуску и тестированию
- [docs/DEPLOY.md](docs/DEPLOY.md) — деплой на Render.com (постоянная ссылка для показа)
- [docs/student-guide/theory-conspect.md](docs/student-guide/theory-conspect.md) — полный конспект теории курса
- [docs/student-guide/glossary.md](docs/student-guide/glossary.md) — глоссарий терминов
- [docs/report/](docs/report/) — отчёт по практике (обзор аналогов, архитектура, аналитика, заключение)

## Тесты

45 backend-тестов (pytest) + 4 frontend smoke-теста (Playwright):

```bash
./scripts/run_all_tests.sh
```
