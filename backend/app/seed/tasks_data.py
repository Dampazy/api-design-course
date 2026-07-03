from __future__ import annotations

# task_type values match app.models.task.TaskType.
# options schema by type:
#   SINGLE_CHOICE / MULTIPLE_CHOICE -> {"choices": [str, ...]}
#   FILL_BLANK / JSON_FIX           -> None
#   ORDERING                        -> {"items": [str, ...]}  (shown in this, shuffled order)
#   MATCHING                        -> {"left": [str, ...], "right": [str, ...]}
#
# correct_answer schema by type:
#   SINGLE_CHOICE  -> int (index into choices)
#   MULTIPLE_CHOICE -> [int, ...] (indices into choices)
#   FILL_BLANK     -> str
#   ORDERING       -> [int, ...] (sequence of item-indices producing the correct order)
#   MATCHING       -> {"<left_index>": <right_index>, ...}
#   JSON_FIX       -> dict (the corrected JSON object)

TASKS = [
    # --- Block 1: rest-basics-http-methods ---
    {
        "theory_slug": "rest-basics-http-methods",
        "order_index": 1,
        "title": "Метод для частичного обновления",
        "statement_markdown": (
            "Какой HTTP-метод следует использовать для **частичного** "
            "обновления ресурса (обновить только часть полей, не заменяя "
            "ресурс целиком)?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {"choices": ["GET", "POST", "PUT", "PATCH"]},
        "correct_answer": 3,
        "check_config": {},
        "explanation_markdown": (
            "`PATCH` предназначен для частичного обновления. `PUT` "
            "используется для полной замены ресурса, `POST` — для создания "
            "или неидемпотентных действий, `GET` — только для чтения."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "rest-basics-http-methods",
        "order_index": 2,
        "title": "Идемпотентные методы",
        "statement_markdown": (
            "Какие из перечисленных HTTP-методов являются **идемпотентными** "
            "(повторное выполнение приводит к тому же состоянию сервера, что "
            "и однократное)? Выберите все подходящие варианты."
        ),
        "task_type": "MULTIPLE_CHOICE",
        "options": {"choices": ["GET", "POST", "PUT", "DELETE", "PATCH"]},
        "correct_answer": [0, 2, 3],
        "check_config": {},
        "explanation_markdown": (
            "GET, PUT и DELETE идемпотентны. POST не идемпотентен (создаёт "
            "новый ресурс при каждом вызове). PATCH формально не гарантирует "
            "идемпотентность."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "rest-basics-http-methods",
        "order_index": 3,
        "title": "Safe-метод для чтения",
        "statement_markdown": (
            "Заполните пропуск: метод **___** используется для получения "
            "представления ресурса и является *safe* (не изменяет состояние "
            "сервера)."
        ),
        "task_type": "FILL_BLANK",
        "options": None,
        "correct_answer": "GET",
        "check_config": {"case_sensitive": False},
        "explanation_markdown": "Правильный ответ — GET.",
        "is_final_test": False,
    },
    # --- Block 2: status-codes-error-handling ---
    {
        "theory_slug": "status-codes-error-handling",
        "order_index": 1,
        "title": "Соответствие кодов ответа их значению",
        "statement_markdown": (
            "Сопоставьте каждый код ответа HTTP с его значением."
        ),
        "task_type": "MATCHING",
        "options": {
            "left": ["404", "201", "409", "422"],
            "right": [
                "Unprocessable Entity",
                "Not Found",
                "Conflict",
                "Created",
            ],
        },
        "correct_answer": {"0": 1, "1": 3, "2": 2, "3": 0},
        "check_config": {},
        "explanation_markdown": (
            "404 — Not Found, 201 — Created, 409 — Conflict, "
            "422 — Unprocessable Entity."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "status-codes-error-handling",
        "order_index": 2,
        "title": "Код при успешном создании ресурса",
        "statement_markdown": (
            "Какой код ответа следует вернуть при успешном создании нового "
            "ресурса через `POST`?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {
            "choices": ["200 OK", "201 Created", "202 Accepted", "204 No Content"]
        },
        "correct_answer": 1,
        "check_config": {},
        "explanation_markdown": (
            "201 Created — стандартный код при успешном создании ресурса, "
            "часто сопровождается заголовком Location."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "status-codes-error-handling",
        "order_index": 3,
        "title": "Исправление Problem Details",
        "statement_markdown": (
            "Дан фрагмент тела ошибки. Приведите его к формату RFC 7807 "
            "Problem Details, добавив недостающее обязательное поле "
            "`status` со значением `409`:\n\n"
            "```json\n"
            '{"type": "https://example.com/errors/conflict", '
            '"title": "Ресурс уже существует"}\n'
            "```"
        ),
        "task_type": "JSON_FIX",
        "options": None,
        "correct_answer": {
            "type": "https://example.com/errors/conflict",
            "title": "Ресурс уже существует",
            "status": 409,
        },
        "check_config": {},
        "explanation_markdown": (
            "RFC 7807 требует поле `status`, дублирующее HTTP-код ответа, "
            "для удобства логирования и отладки на стороне клиента."
        ),
        "is_final_test": False,
    },
    # --- Block 3: resource-naming-versioning ---
    {
        "theory_slug": "resource-naming-versioning",
        "order_index": 1,
        "title": "Нарушение конвенции именования",
        "statement_markdown": (
            "В каком из перечисленных URL нарушена RESTful-конвенция "
            "именования ресурсов?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {
            "choices": [
                "GET /orders/42",
                "POST /orders",
                "GET /orders/42/items",
                "GET /getOrderById?id=42",
            ]
        },
        "correct_answer": 3,
        "check_config": {},
        "explanation_markdown": (
            "`/getOrderById` содержит глагол в пути — HTTP-метод уже несёт "
            "семантику действия, дублирование избыточно и нарушает "
            "единообразие интерфейса REST."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "resource-naming-versioning",
        "order_index": 2,
        "title": "Путь для списка заказов пользователя",
        "statement_markdown": (
            "Укажите корректный (RESTful) путь для получения списка заказов "
            "пользователя с id=42."
        ),
        "task_type": "FILL_BLANK",
        "options": None,
        "correct_answer": "/users/42/orders",
        "check_config": {
            "case_sensitive": False,
            "alternative_answers": ["users/42/orders", "/users/42/orders/"],
        },
        "explanation_markdown": (
            "Вложенность `/users/{id}/orders` явно отражает отношение "
            "«заказы принадлежат пользователю»."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "resource-naming-versioning",
        "order_index": 3,
        "title": "Шаги эволюции API без breaking changes",
        "statement_markdown": (
            "Расставьте по порядку шаги безопасной эволюции публичного API "
            "с версии v1 на v2 без breaking changes для существующих "
            "клиентов v1."
        ),
        "task_type": "ORDERING",
        "options": {
            "items": [
                "Уведомить клиентов о сроке поддержки v1 (deprecation notice)",
                "Спроектировать v2 с изменениями, сохранив v1 без изменений",
                "Отключить v1 после истечения срока поддержки",
                "Опубликовать v2 и документацию, оставив v1 работающим параллельно",
                "Дождаться миграции активных клиентов на v2, отслеживая трафик на v1",
            ]
        },
        "correct_answer": [1, 3, 0, 4, 2],
        "check_config": {},
        "explanation_markdown": (
            "Порядок: спроектировать v2 не трогая v1 → опубликовать v2 "
            "параллельно с v1 → уведомить о сроке поддержки v1 → дождаться "
            "миграции клиентов → отключить v1."
        ),
        "is_final_test": False,
    },
    # --- Block 4: auth-authorization ---
    {
        "theory_slug": "auth-authorization",
        "order_index": 1,
        "title": "Authentication vs Authorization",
        "statement_markdown": (
            "Что из перечисленного относится к **Authentication (AuthN)**, "
            "а не к Authorization (AuthZ)? Выберите все подходящие варианты."
        ),
        "task_type": "MULTIPLE_CHOICE",
        "options": {
            "choices": [
                "Проверка логина и пароля пользователя",
                "Проверка, что у пользователя есть роль admin для доступа к /admin",
                "Верификация подписи JWT-токена и извлечение user id",
                "Проверка, что скоуп токена включает orders:write",
            ]
        },
        "correct_answer": [0, 2],
        "check_config": {},
        "explanation_markdown": (
            "Проверка логина/пароля и верификация подписи токена "
            "подтверждают личность (AuthN). Проверка роли и скоупа — это "
            "уже проверка прав (AuthZ)."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "auth-authorization",
        "order_index": 2,
        "title": "Шаги OAuth2 Authorization Code Flow",
        "statement_markdown": (
            "Расставьте по порядку шаги OAuth2 Authorization Code Flow."
        ),
        "task_type": "ORDERING",
        "options": {
            "items": [
                "Сервер авторизации перенаправляет пользователя обратно с authorization code",
                "Приложение перенаправляет пользователя на сервер авторизации с client_id и redirect_uri",
                "Приложение использует access_token для запросов к API",
                "Пользователь логинится и подтверждает запрошенные права",
                "Приложение обменивает code и client_secret на access_token",
            ]
        },
        "correct_answer": [1, 3, 0, 4, 2],
        "check_config": {},
        "explanation_markdown": (
            "Порядок: перенаправление на сервер авторизации → логин и "
            "согласие пользователя → редирект с authorization code → обмен "
            "code на access_token → использование access_token."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "auth-authorization",
        "order_index": 3,
        "title": "Заголовок для Bearer JWT",
        "statement_markdown": (
            "Укажите название HTTP-заголовка, используемого для передачи "
            "Bearer JWT-токена в запросе."
        ),
        "task_type": "FILL_BLANK",
        "options": None,
        "correct_answer": "Authorization",
        "check_config": {"case_sensitive": False},
        "explanation_markdown": (
            "Стандартный заголовок — `Authorization: Bearer <token>`."
        ),
        "is_final_test": False,
    },
    # --- Block 5: pagination-filtering-idempotency ---
    {
        "theory_slug": "pagination-filtering-idempotency",
        "order_index": 1,
        "title": "Параметры курсорной пагинации",
        "statement_markdown": (
            "Какие query-параметры характерны именно для **cursor-based** "
            "(курсорной) пагинации, а не offset-based?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {
            "choices": [
                "limit и offset",
                "page и per_page",
                "limit и cursor",
                "start и end",
            ]
        },
        "correct_answer": 2,
        "check_config": {},
        "explanation_markdown": (
            "Курсорная пагинация использует непрозрачный `cursor`, "
            "кодирующий позицию последнего элемента предыдущей страницы, "
            "вместе с `limit`."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "pagination-filtering-idempotency",
        "order_index": 2,
        "title": "Сценарий → тип пагинации",
        "statement_markdown": (
            "Сопоставьте сценарий использования с более подходящим типом "
            "пагинации."
        ),
        "task_type": "MATCHING",
        "options": {
            "left": [
                "Нужен произвольный переход на страницу N в админ-панели",
                "Высоконагруженная лента с частыми вставками новых записей",
                "Небольшой справочник с постраничной навигацией",
            ],
            "right": ["cursor-based", "offset-based"],
        },
        "correct_answer": {"0": 1, "1": 0, "2": 1},
        "check_config": {},
        "explanation_markdown": (
            "Offset-based удобна для произвольного перехода по страницам "
            "небольших наборов данных. Cursor-based устойчива к вставкам и "
            "эффективна на больших высоконагруженных выборках."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "pagination-filtering-idempotency",
        "order_index": 3,
        "title": "Заголовок защиты от дублирования платежа",
        "statement_markdown": (
            "Укажите точное имя HTTP-заголовка, который нужно добавить к "
            "POST-запросу на оплату, чтобы избежать создания дублирующего "
            "платежа при повторной отправке одного и того же запроса "
            "(например, из-за таймаута на клиенте)."
        ),
        "task_type": "FILL_BLANK",
        "options": None,
        "correct_answer": "Idempotency-Key",
        "check_config": {"case_sensitive": False},
        "explanation_markdown": (
            "`Idempotency-Key` — уникальный ключ попытки операции; сервер "
            "возвращает сохранённый результат первого запроса с этим "
            "ключом, не выполняя операцию повторно."
        ),
        "is_final_test": False,
    },
    # --- Block 6: documentation-rate-limiting-hateoas ---
    {
        "theory_slug": "documentation-rate-limiting-hateoas",
        "order_index": 1,
        "title": "Заголовок повторного запроса при 429",
        "statement_markdown": (
            "Какой HTTP-заголовок в ответе сигнализирует клиенту о "
            "превышении лимита частоты запросов и подсказывает, через "
            "сколько секунд можно повторить запрос?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {
            "choices": ["ETag", "Retry-After", "Cache-Control", "Content-Range"]
        },
        "correct_answer": 1,
        "check_config": {},
        "explanation_markdown": (
            "`Retry-After` указывает клиенту, через сколько секунд (или к "
            "какой дате) имеет смысл повторить запрос."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "documentation-rate-limiting-hateoas",
        "order_index": 2,
        "title": "Код ответа при превышении rate limit",
        "statement_markdown": (
            "Укажите числовой HTTP-код ответа, который сервер должен "
            "вернуть при превышении лимита частоты запросов (rate limit)."
        ),
        "task_type": "FILL_BLANK",
        "options": None,
        "correct_answer": "429",
        "check_config": {},
        "explanation_markdown": "429 Too Many Requests.",
        "is_final_test": False,
    },
    {
        "theory_slug": "documentation-rate-limiting-hateoas",
        "order_index": 3,
        "title": "Поле, реализующее HATEOAS",
        "statement_markdown": (
            "В приведённом ниже примере JSON-ответа найдите поле, "
            "реализующее принцип HATEOAS:\n\n"
            "```json\n"
            '{"id": 42, "status": "pending", "amount": 1500, '
            '"_links": {"self": {"href": "/orders/42"}}}\n'
            "```"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {"choices": ["id", "status", "_links", "amount"]},
        "correct_answer": 2,
        "check_config": {},
        "explanation_markdown": (
            "`_links` содержит гиперссылки на доступные из текущего "
            "состояния действия — это и есть реализация HATEOAS."
        ),
        "is_final_test": False,
    },
    # --- Final test (7 questions, transfer of knowledge, no duplicates) ---
    {
        "theory_slug": "rest-basics-http-methods",
        "order_index": 4,
        "title": "[Финальный тест] Повторный DELETE",
        "statement_markdown": (
            "Клиент отправляет `DELETE`-запрос на уже удалённый ранее "
            "ресурс повторно. Согласно определению идемпотентности, это "
            "должно:"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {
            "choices": [
                "Привести сервер в то же состояние, что и после первого "
                "удаления (ресурса по-прежнему нет)",
                "Восстановить ресурс",
                "Вызвать ошибку 500",
                "Создать новый ресурс с тем же id",
            ]
        },
        "correct_answer": 0,
        "check_config": {},
        "explanation_markdown": (
            "Идемпотентность гарантирует одинаковое конечное состояние "
            "сервера при повторных вызовах, даже если код ответа при "
            "повторе может отличаться (например, 404 вместо 204)."
        ),
        "is_final_test": True,
    },
    {
        "theory_slug": "status-codes-error-handling",
        "order_index": 4,
        "title": "[Финальный тест] Коды класса 4xx",
        "statement_markdown": (
            "Какие из следующих кодов относятся к классу ошибок клиента "
            "(4xx)?"
        ),
        "task_type": "MULTIPLE_CHOICE",
        "options": {"choices": ["400", "404", "500", "429", "503"]},
        "correct_answer": [0, 1, 3],
        "check_config": {},
        "explanation_markdown": "400, 404 и 429 — коды класса 4xx (ошибка клиента). 500 и 503 — класс 5xx (ошибка сервера).",
        "is_final_test": True,
    },
    {
        "theory_slug": "resource-naming-versioning",
        "order_index": 4,
        "title": "[Финальный тест] Опциональное поле и breaking change",
        "statement_markdown": (
            "Является ли добавление нового опционального поля в JSON-ответ "
            "существующего эндпоинта breaking change? Ответьте «да» или «нет»."
        ),
        "task_type": "FILL_BLANK",
        "options": None,
        "correct_answer": "нет",
        "check_config": {"case_sensitive": False},
        "explanation_markdown": (
            "Добавление нового опционального поля не breaking change при "
            "соблюдении принципа tolerant reader на стороне клиентов."
        ),
        "is_final_test": True,
    },
    {
        "theory_slug": "auth-authorization",
        "order_index": 4,
        "title": "[Финальный тест] Смысл Bearer-токена",
        "statement_markdown": (
            "Токен передан в заголовке `Authorization: Bearer eyJhbGciOi...`. "
            "Что представляет собой этот токен в контексте OAuth2/JWT?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {
            "choices": [
                "Ключ шифрования базы данных",
                "Access-токен, подтверждающий права клиента на действие "
                "от имени пользователя",
                "Пароль пользователя в открытом виде",
                "CSRF-токен формы",
            ]
        },
        "correct_answer": 1,
        "check_config": {},
        "explanation_markdown": (
            "Bearer-токен — это access token, дающий его предъявителю "
            "доступ к ресурсам от имени пользователя, без передачи пароля."
        ),
        "is_final_test": True,
    },
    {
        "theory_slug": "pagination-filtering-idempotency",
        "order_index": 4,
        "title": "[Финальный тест] Причина пропусков в offset-пагинации",
        "statement_markdown": (
            "Почему offset-based пагинация может пропускать или дублировать "
            "элементы при активной вставке новых записей между запросами "
            "страниц?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {
            "choices": [
                "Потому что сервер кэширует старые данные",
                "Потому что позиция (offset) сдвигается относительно "
                "изменяющегося набора данных",
                "Потому что offset требует авторизации",
                "Потому что offset несовместим с сортировкой",
            ]
        },
        "correct_answer": 1,
        "check_config": {},
        "explanation_markdown": (
            "Offset — это позиция в наборе данных на момент запроса; если "
            "набор меняется между запросами страниц, позиции элементов "
            "сдвигаются, что приводит к пропускам/дублям."
        ),
        "is_final_test": True,
    },
    {
        "theory_slug": "documentation-rate-limiting-hateoas",
        "order_index": 4,
        "title": "[Финальный тест] Источник Swagger UI",
        "statement_markdown": (
            "Какой инструмент/формат позволяет автоматически сгенерировать "
            "интерактивную документацию (Swagger UI) прямо из кода "
            "FastAPI-приложения?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {
            "choices": [
                "README.md",
                "OpenAPI-схема, генерируемая FastAPI из аннотаций типов",
                "Дамп базы данных",
                "Файл .env",
            ]
        },
        "correct_answer": 1,
        "check_config": {},
        "explanation_markdown": (
            "FastAPI автоматически строит OpenAPI-схему из аннотаций типов "
            "и Pydantic-моделей и на её основе рендерит Swagger UI на /docs."
        ),
        "is_final_test": True,
    },
    {
        "theory_slug": "status-codes-error-handling",
        "order_index": 5,
        "title": "[Финальный тест] Исправление Problem Details (422)",
        "statement_markdown": (
            "Дан ответ сервера на ошибку валидации без обязательного поля "
            "`status` формата RFC 7807. Приведите его к корректному виду, "
            "добавив поле `status` со значением `422`:\n\n"
            "```json\n"
            '{"type": "https://example.com/errors/validation", '
            '"title": "Некорректные данные"}\n'
            "```"
        ),
        "task_type": "JSON_FIX",
        "options": None,
        "correct_answer": {
            "type": "https://example.com/errors/validation",
            "title": "Некорректные данные",
            "status": 422,
        },
        "check_config": {},
        "explanation_markdown": (
            "422 Unprocessable Entity — код для семантически невалидных, "
            "но синтаксически корректных запросов."
        ),
        "is_final_test": True,
    },
    # --- Additional practice tasks (batch 2): "write the request yourself"
    # (API_REQUEST) plus one more question per block reinforcing the
    # extended theory sections (checklists, decision trees, PKCE, etc.) ---
    {
        "theory_slug": "rest-basics-http-methods",
        "order_index": 4,
        "title": "Запрос на полную замену ресурса",
        "statement_markdown": (
            "Напишите запрос для **полной замены** статьи с id=15 (у вас "
            "уже готов JSON с новым содержимым статьи — важно выбрать "
            "подходящий HTTP-метод и путь, тело запроса можно не писать)."
        ),
        "task_type": "API_REQUEST",
        "options": None,
        "correct_answer": {"method": "PUT", "path": "/articles/15"},
        "check_config": {},
        "explanation_markdown": (
            "`PUT /articles/15` — полная замена существующего ресурса. "
            "`PATCH` подошёл бы только для частичного обновления."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "rest-basics-http-methods",
        "order_index": 5,
        "title": "Что не входит в чек-лист перед отправкой запроса",
        "statement_markdown": (
            "Что из перечисленного **не** относится к чек-листу «перед "
            "отправкой запроса» из этого блока теории?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {
            "choices": [
                "Соответствие метода характеру операции",
                "Риск дублирования при повторной отправке POST",
                "Название СУБД, используемой на сервере",
                "Наличие Content-Type для запроса с телом",
            ]
        },
        "correct_answer": 2,
        "check_config": {},
        "explanation_markdown": (
            "Чек-лист касается семантики запроса на стороне клиента; "
            "внутренняя реализация сервера (например, конкретная СУБД) "
            "клиенту не видна и не должна на неё влиять."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "status-codes-error-handling",
        "order_index": 4,
        "title": "Запрос на отмену подписки",
        "statement_markdown": (
            "Напишите запрос на отмену подписки с id=9 (это бизнес-команда, "
            "а не просто изменение одного поля — используйте под-ресурс с "
            "существительным-командой в пути, как в примере с публикацией "
            "статьи из блока 1)."
        ),
        "task_type": "API_REQUEST",
        "options": None,
        "correct_answer": {"method": "POST", "path": "/subscriptions/9/cancel"},
        "check_config": {},
        "explanation_markdown": (
            "`POST /subscriptions/9/cancel` — команда-действие с побочными "
            "эффектами (например, немедленное прекращение доступа), "
            "смоделированная как под-ресурс."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "status-codes-error-handling",
        "order_index": 5,
        "title": "Код ответа для отрицательной цены",
        "statement_markdown": (
            "Сервер получил синтаксически валидный JSON, но поле `price` "
            "в нём отрицательное. Согласно дереву решений из теории, какой "
            "код ответа следует вернуть?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {
            "choices": [
                "400 Bad Request",
                "404 Not Found",
                "422 Unprocessable Entity",
                "500 Internal Server Error",
            ]
        },
        "correct_answer": 2,
        "check_config": {},
        "explanation_markdown": (
            "JSON синтаксически корректен, но не проходит бизнес-валидацию "
            "— это случай `422 Unprocessable Entity`, а не `400` (который "
            "про синтаксические ошибки)."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "resource-naming-versioning",
        "order_index": 4,
        "title": "Запрос на вложенный ресурс",
        "statement_markdown": (
            "Напишите запрос для получения комментария с id=301 к статье "
            "с id=15, используя вложенный путь."
        ),
        "task_type": "API_REQUEST",
        "options": None,
        "correct_answer": {"method": "GET", "path": "/articles/15/comments/301"},
        "check_config": {},
        "explanation_markdown": (
            "`GET /articles/15/comments/301` — вложенность отражает "
            "отношение «комментарий принадлежит статье»."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "resource-naming-versioning",
        "order_index": 5,
        "title": "Версионирование через дату релиза",
        "statement_markdown": (
            "Какая компания из рассмотренных примеров использует "
            "версионирование API через заголовок с **датой релиза**, а не "
            "номером версии?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {"choices": ["Twitter/X", "GitHub", "Stripe", "Facebook"]},
        "correct_answer": 2,
        "check_config": {},
        "explanation_markdown": (
            "Stripe использует заголовок `Stripe-Version` со значением-"
            "датой (например, `2024-06-20`), а не номером вроде `v2`."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "auth-authorization",
        "order_index": 4,
        "title": "Код ответа при нехватке скоупа",
        "statement_markdown": (
            "Токен клиента валиден (аутентификация прошла успешно), но у "
            "него нет нужного скоупа для запрошенной операции. Какой код "
            "ответа должен вернуть сервер?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {
            "choices": [
                "401 Unauthorized",
                "403 Forbidden",
                "400 Bad Request",
                "404 Not Found",
            ]
        },
        "correct_answer": 1,
        "check_config": {},
        "explanation_markdown": (
            "401 означает «вы не аутентифицированы», а токен валиден — "
            "значит, дело в правах, и корректный код — 403 Forbidden."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "auth-authorization",
        "order_index": 5,
        "title": "Расширение OAuth2 для мобильных приложений",
        "statement_markdown": (
            "Как называется расширение OAuth2 (RFC 7636), позволяющее "
            "безопасно использовать Authorization Code Flow в мобильных и "
            "SPA-приложениях без хранения `client_secret`?"
        ),
        "task_type": "FILL_BLANK",
        "options": None,
        "correct_answer": "PKCE",
        "check_config": {"case_sensitive": False},
        "explanation_markdown": (
            "PKCE (Proof Key for Code Exchange) заменяет постоянный "
            "`client_secret` на одноразовую пару code_verifier/code_challenge."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "pagination-filtering-idempotency",
        "order_index": 4,
        "title": "Запрос с фильтром, сортировкой и пагинацией",
        "statement_markdown": (
            "Напишите запрос на получение оплаченных заказов "
            "(`status=paid`), отсортированных по дате создания по "
            "убыванию, не более 20 штук за раз."
        ),
        "task_type": "API_REQUEST",
        "options": None,
        "correct_answer": {
            "method": "GET",
            "path": "/orders",
            "query": {"status": "paid", "sort": "-created_at", "limit": "20"},
        },
        "check_config": {},
        "explanation_markdown": (
            "`GET /orders?status=paid&sort=-created_at&limit=20` — порядок "
            "query-параметров в URL не важен, автопроверка сравнивает их "
            "как набор пар ключ-значение."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "pagination-filtering-idempotency",
        "order_index": 5,
        "title": "Пагинация vs rate limiting",
        "statement_markdown": (
            "Чем rate limiting принципиально отличается от пагинации?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {
            "choices": [
                "Rate limiting ограничивает частоту запросов во времени, "
                "пагинация — размер одного ответа",
                "Это два названия одного и того же механизма",
                "Пагинация применяется только к POST-запросам",
                "Rate limiting нужен только для платных API",
            ]
        },
        "correct_answer": 0,
        "check_config": {},
        "explanation_markdown": (
            "Пагинация решает задачу «сколько записей вернуть за раз», "
            "rate limiting — «сколько запросов можно сделать за период "
            "времени». Механизмы независимы и часто используются вместе."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "documentation-rate-limiting-hateoas",
        "order_index": 4,
        "title": "Заголовок отключения эндпоинта",
        "statement_markdown": (
            "Какой HTTP-заголовок (RFC 8594) сообщает клиенту дату, когда "
            "эндпоинт будет отключён?"
        ),
        "task_type": "FILL_BLANK",
        "options": None,
        "correct_answer": "Sunset",
        "check_config": {"case_sensitive": False},
        "explanation_markdown": (
            "Заголовок `Sunset` указывает дату отключения ресурса/эндпоинта, "
            "часто в паре с заголовком `Deprecation`."
        ),
        "is_final_test": False,
    },
    {
        "theory_slug": "documentation-rate-limiting-hateoas",
        "order_index": 5,
        "title": "Проверка подлинности webhook-запроса",
        "statement_markdown": (
            "Как webhook-эндпоинт должен проверять, что входящий "
            "`POST`-запрос действительно прислан доверенным сервером, а не "
            "злоумышленником?"
        ),
        "task_type": "SINGLE_CHOICE",
        "options": {
            "choices": [
                "Проверить IP-адрес отправителя вручную",
                "Сверить криптографическую подпись тела запроса из "
                "заголовка (например, X-Hub-Signature-256)",
                "Довериться, если Content-Type: application/json",
                "Проверить, что запрос пришёл по HTTPS",
            ]
        },
        "correct_answer": 1,
        "check_config": {},
        "explanation_markdown": (
            "Только криптографическая подпись, вычисленная общим секретом, "
            "надёжно доказывает, что тело запроса не подделано и прислано "
            "именно ожидаемым отправителем."
        ),
        "is_final_test": False,
    },
    # --- Additional final test question (transfer of skill: write a
    # cursor-paginated request from scratch) ---
    {
        "theory_slug": "pagination-filtering-idempotency",
        "order_index": 6,
        "title": "[Финальный тест] Запрос со курсорной пагинацией",
        "statement_markdown": (
            "Напишите запрос для получения следующей страницы отзывов к "
            "товару с id=88, используя курсорную пагинацию: не более 10 "
            "записей за раз, курсор следующей страницы — `eyJpZCI6MzB9`."
        ),
        "task_type": "API_REQUEST",
        "options": None,
        "correct_answer": {
            "method": "GET",
            "path": "/products/88/reviews",
            "query": {"limit": "10", "cursor": "eyJpZCI6MzB9"},
        },
        "check_config": {},
        "explanation_markdown": (
            "`GET /products/88/reviews?limit=10&cursor=eyJpZCI6MzB9` — "
            "вложенный путь для отзывов конкретного товара плюс параметры "
            "курсорной пагинации."
        ),
        "is_final_test": True,
    },
]
