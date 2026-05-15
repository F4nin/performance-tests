# Анализ улучшений: seeds/builder.py и seeds/dumps.py

Коммит: `a75c9a2` — «Реализация билдера сидинга»

---

## seeds/builder.py

### 1. Дублирование кода: `build_debit_card_account_result` и `build_credit_card_account_result`

**Проблема.** Оба метода полностью идентичны по логике — открывают счёт, извлекают ID первой карты,
затем в точности одним и тем же образом строят все вложенные объекты (виртуальные карты,
физические карты, все виды операций). Единственное различие — вызов разного API:
`open_debit_card_account` против `open_credit_card_account`.
Дублирование нарушает принцип DRY: при добавлении нового типа операции придётся менять код в двух местах.

**Решение.** Выделить приватный метод, принимающий `Callable` для открытия счёта:

```python
def _build_card_account_result(self, account_opener: Callable, plan: SeedAccountsPlan, user_id: str) -> SeedAccountResult:
    response = account_opener(user_id=user_id)
    card_id = response.account.cards[0].id
    account_id = response.account.id
    # ... единая сборка результата
```

**Источники:**
- Hunt A., Thomas D. *The Pragmatic Programmer.* Addison-Wesley, 2019. Tip 11: «Don't Repeat Yourself (DRY)».
- Martin R. C. *Clean Code.* Prentice Hall, 2008. Ch. 3: Functions — «Don't Repeat Yourself».

---

### 2. Неверный тип возвращаемого значения у `build_transfer_operation_result`

**Проблема.** Метод аннотирован как `-> SeedCardResult`, но возвращает объект `SeedOperationResult`.
Это явная ошибка типизации, которая вводит в заблуждение инструменты статического анализа (mypy, pyright)
и всех, кто читает код.

**Решение.** Исправить аннотацию:

```python
def build_transfer_operation_result(self, card_id: str, account_id: str) -> SeedOperationResult:
```

**Источники:**
- PEP 484 — Type Hints. https://peps.python.org/pep-0484/
- mypy — Static Type Checker for Python. https://mypy.readthedocs.io/

---

### 3. Отсутствие аннотации возвращаемого типа у `build_http_seeds_builder`

**Проблема.** Фабрика `build_grpc_seeds_builder` аннотирована `-> SeedsBuilder`,
а `build_http_seeds_builder` — нет. Непоследовательность затрудняет автодополнение в IDE
и проверку типов.

**Решение.** Добавить аннотацию:

```python
def build_http_seeds_builder() -> SeedsBuilder:
```

**Источники:**
- PEP 484 — Type Hints. https://peps.python.org/pep-0484/

---

### 4. Отсутствие docstring у части методов

**Проблема.** Методы `build_transfer_operation_result`, `build_cash_withdrawal_operation_result`
и `build_virtual_card_result` не имеют документации, в то время как остальные методы задокументированы
в Google-style. Нарушается единообразие — при просмотре класса непонятно, чем руководствоваться.

**Решение.** Добавить docstring по единому шаблону (Google style) и убедиться, что docstring класса
в атрибутах `Attributes:` перечисляет все четыре клиента.

**Источники:**
- Google Python Style Guide — Docstrings.
  https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
- PEP 257 — Docstring Conventions. https://peps.python.org/pep-0257/

---

### 5. Использование `response.account.id` вместо локальной переменной `account_id`

**Проблема.** В `build_debit_card_account_result` для виртуальных и физических карт
передаётся `response.account.id`, хотя на строку выше уже вычислен `account_id = response.account.id`.
Это мелкая непоследовательность, снижающая читаемость и создающая лишние обращения к атрибуту.

**Решение.** Везде внутри метода использовать уже вычисленный `account_id`.

**Источники:**
- Martin R. C. *Clean Code.* Ch. 2: Meaningful Names — «Use Intention-Revealing Names».

---

### 6. Синхронное последовательное выполнение всех запросов

**Проблема.** Метод `build` создаёт всех пользователей последовательно: каждый API-вызов блокирует
поток до получения ответа. При создании 100 пользователей с 5 счетами и 10 операциями каждый —
это тысячи блокирующих запросов. Для performance-тестирования, где сидинг должен быть быстрым,
это критический bottleneck.

**Решение.** Использовать асинхронный подход (`asyncio` + `async/await`) или
`concurrent.futures.ThreadPoolExecutor`/`ProcessPoolExecutor` для параллельного создания пользователей.

```python
import asyncio

async def build_async(self, plan: SeedsPlan) -> SeedsResult:
    users = await asyncio.gather(*[
        self.build_user_async(plan=plan.users)
        for _ in range(plan.users.count)
    ])
    return SeedsResult(users=list(users))
```

**Источники:**
- Python docs — `asyncio`. https://docs.python.org/3/library/asyncio.html
- Python docs — `concurrent.futures`. https://docs.python.org/3/library/concurrent.futures.html
- Beazley D. *Python Cookbook.* O'Reilly, 2013. Ch. 12: Concurrency.

---

### 7. Отсутствие логирования

**Проблема.** Нет ни одной строки логирования. Если при сидинге упадёт запрос
(сетевая ошибка, gRPC-ошибка), единственная информация — трассировка стека.
Непонятно, на каком шаге (какой пользователь, какой счёт, какая операция) произошла ошибка.

**Решение.** Добавить вызовы `logging.debug`/`logging.info` в начале каждого метода
и `logging.error` в блоках `except`.

**Источники:**
- Python docs — `logging`. https://docs.python.org/3/library/logging.html
- Python docs — Logging HOWTO. https://docs.python.org/3/howto/logging.html

---

### 8. Нет протокола (Protocol/ABC) для клиентов

**Проблема.** Тип аргументов в `__init__` задан через union:
`UsersGatewayGRPCClient | UsersGatewayHTTPClient`. Это означает, что `SeedsBuilder`
жёстко связан с двумя конкретными реализациями. Добавление третьего типа клиента
(например, mock-клиента для юнит-тестов) потребует изменения сигнатуры конструктора.

**Решение.** Ввести `Protocol` или `ABC` для каждого клиента:

```python
from typing import Protocol

class UsersGatewayClient(Protocol):
    def create_user(self) -> ...: ...
```

После этого `__init__` принимает `UsersGatewayClient`, не завися от конкретной реализации.

**Источники:**
- PEP 544 — Protocols: Structural subtyping. https://peps.python.org/pep-0544/
- Python docs — `typing.Protocol`. https://docs.python.org/3/library/typing.html#typing.Protocol
- Percival H., Gregory B. *Architecture Patterns with Python.* O'Reilly, 2020. Ch. 3: Abstractions.

---

## seeds/dumps.py

### 9. Race condition при создании директории

**Проблема.** Паттерн `if not os.path.exists("dumps"): os.mkdir("dumps")` содержит
классический TOCTOU (Time-Of-Check / Time-Of-Use) race condition:
между проверкой и созданием другой поток или процесс может создать директорию,
что вызовет `FileExistsError`. Особенно опасно при параллельном запуске сидинга.

**Решение.** Использовать атомарный вызов:

```python
os.makedirs("dumps", exist_ok=True)
```

**Источники:**
- Python docs — `os.makedirs`. https://docs.python.org/3/library/os.html#os.makedirs
- CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition.
  https://cwe.mitre.org/data/definitions/367.html

---

### 10. Жёстко прописанный путь и его дублирование

**Проблема.** Строка `"dumps"` встречается дважды в двух разных форматах:
`"dumps"` (в `os.path.exists`) и `"./dumps/"` (в `open`). При изменении пути
надо будет менять его в нескольких местах, рискуя забыть про одно из них.

**Решение.** Вынести в модульную константу:

```python
_DUMPS_DIR = Path("dumps")

def save_seeds_result(result: SeedsResult, scenario: str) -> None:
    _DUMPS_DIR.mkdir(exist_ok=True)
    (_DUMPS_DIR / f"{scenario}_seeds.json").write_text(
        result.model_dump_json(), encoding="utf-8"
    )
```

Использование `pathlib.Path` вместо строк делает работу с путями надёжнее и читаемее.

**Источники:**
- Python docs — `pathlib`. https://docs.python.org/3/library/pathlib.html
- Hunt A., Thomas D. *The Pragmatic Programmer.* Tip 27: «Don't Repeat Yourself».

---

### 11. Избыточный режим открытия файла `'w+'`

**Проблема.** `open(f"./dumps/{scenario}_seeds.json", 'w+', ...)` открывает файл
для чтения и записи (`w+`), хотя в методе выполняется только запись.
Это избыточно и вводит читателя в заблуждение.

**Решение.** Использовать `'w'`:

```python
with open(f"./dumps/{scenario}_seeds.json", 'w', encoding="utf-8") as file:
```

Или ещё лучше — `pathlib.Path.write_text()`, как показано выше.

**Источники:**
- Python docs — Built-in function `open`. https://docs.python.org/3/library/functions.html#open

---

### 12. Отсутствие валидации аргумента `scenario`

**Проблема.** `scenario` напрямую подставляется в путь к файлу.
Если передать строку вида `../../etc/cron.d/evil` — возможен path traversal.
Даже без злого умысла, пробел или спецсимвол в имени сценария может сломать логику.

**Решение.** Валидировать `scenario` перед использованием:

```python
import re

_SAFE_SCENARIO = re.compile(r'^[a-zA-Z0-9_\-]+$')

def _validate_scenario(scenario: str) -> None:
    if not _SAFE_SCENARIO.match(scenario):
        raise ValueError(f"Invalid scenario name: {scenario!r}")
```

**Источники:**
- OWASP — Path Traversal.
  https://owasp.org/www-community/attacks/Path_Traversal
- CWE-22: Improper Limitation of a Pathname to a Restricted Directory.
  https://cwe.mitre.org/data/definitions/22.html

---

### 13. Неинформативная ошибка при отсутствии файла в `load_seeds_result`

**Проблема.** Если файл `{scenario}_seeds.json` не существует, Python выбросит
`FileNotFoundError` с сообщением о системном пути — без контекста о том, какой
сценарий запрашивался и где его искать.

**Решение.** Обернуть в `try/except` с понятным сообщением:

```python
def load_seeds_result(scenario: str) -> SeedsResult:
    path = _DUMPS_DIR / f"{scenario}_seeds.json"
    try:
        return SeedsResult.model_validate_json(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Seeds dump for scenario '{scenario}' not found at {path}. "
            "Run the seeder first."
        )
```

**Источники:**
- Python docs — Errors and Exceptions. https://docs.python.org/3/tutorial/errors.html
- Martin R. C. *Clean Code.* Ch. 7: Error Handling.

---

## seeds/schema/result.py

### 14. `get_next_user` использует `list.pop(0)` — O(n) сложность

**Проблема.** `self.users.pop(0)` — операция O(n): Python сдвигает все оставшиеся элементы
в памяти. При списке из 1000 пользователей это приводит к 1 000 000 операций за полный обход.

**Решение.** Использовать `collections.deque` (O(1) для `popleft`) или хранить
текущий индекс итерации:

```python
from collections import deque

class SeedsResult(BaseModel):
    users: deque[SeedUserResult] = Field(default_factory=deque)

    def get_next_user(self) -> SeedUserResult:
        if not self.users:
            raise RuntimeError("SeedsResult: нет доступных пользователей")
        return self.users.popleft()
```

**Источники:**
- Python docs — `collections.deque`. https://docs.python.org/3/library/collections.html#collections.deque
- Python Time Complexity (Wiki). https://wiki.python.org/moin/TimeComplexity

---

### 15. Нарушение PEP 8: три пустые строки между методами класса

**Проблема.** Между методами `get_next_user` и `get_random_user` в `result.py` (строки 86–89)
стоят три пустые строки. PEP 8 требует одну пустую строку между методами одного класса.

**Решение.** Оставить ровно одну пустую строку.

**Источники:**
- PEP 8 — Style Guide for Python Code: Blank Lines.
  https://peps.python.org/pep-0008/#blank-lines

---

## Итог

| # | Файл            | Категория          | Приоритет |
|---|-----------------|--------------------|-----------|
| 1 | builder.py      | Дублирование кода  | Высокий   |
| 2 | builder.py      | Ошибка типизации   | Высокий   |
| 3 | builder.py      | Непоследовательность | Низкий  |
| 4 | builder.py      | Документация        | Низкий   |
| 5 | builder.py      | Читаемость          | Низкий   |
| 6 | builder.py      | Производительность  | Средний  |
| 7 | builder.py      | Наблюдаемость       | Средний  |
| 8 | builder.py      | Архитектура         | Средний  |
| 9 | dumps.py        | Race condition      | Высокий  |
|10 | dumps.py        | Дублирование пути   | Средний  |
|11 | dumps.py        | Избыточный режим    | Низкий   |
|12 | dumps.py        | Безопасность        | Средний  |
|13 | dumps.py        | Обработка ошибок    | Средний  |
|14 | schema/result.py| Производительность  | Средний  |
|15 | schema/result.py| Стиль кода          | Низкий   |
