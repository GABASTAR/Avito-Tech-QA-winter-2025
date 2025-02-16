# Решение тестового задания для стажировки QA (Зимняя волна 2025)

Добро пожаловать в репозиторий с решениями двух заданий для стажировки QA. В данном репозитории представлены два самостоятельных задания:

- **Task 1** – задание на ручное тестирование веб-страницы (поиск багов, анализ приоритетов и оформление баг-репортов).
- **Task 2** – задание на тестирование API микросервиса объявлений (разработка тест-кейсов, автоматизация тестов и оформление баг-репортов).

---

## Структура репозитория

```
.
├── Task 1
│   ├── images/           # Скриншоты страницы для анализа багов
│   └── BUGS.md           # Баг-репорты, составленные по результатам ручного тестирования
├── Task 2
│   ├── BUGS.md           # Баг-репорты, составленные при тестировании API
│   ├── TESTCASES.md      # Подробное описание тест-кейсов для API
│   └── test_api.py       # Автоматизированные тесты API, реализованные на Python (pytest + requests)
└── README.md             # Данное руководство
```

---

## Описание заданий

### Task 1: Ручное тестирование веб-страницы

В задании представлено изображение поисковой выдачи (скриншот) веб-страницы. Задача заключалась в том, чтобы:
- Проанализировать функциональность страницы.
- Найти и описать баги, определив их приоритеты (high, medium, low).
- Оформить результаты в виде подробных баг-репортов.

Скриншоты для анализа находятся в каталоге `Task 1/images/`, а баг-репорты – в файле `Task 1/BUGS.md`.

### Task 2: Тестирование API микросервиса объявлений

В задании представлен микросервис с четырьмя эндпоинтами:
- Создать объявление (`POST /api/1/item`)
- Получить объявление по ID (`GET /api/1/item/{id}`)
- Получить все объявления по идентификатору продавца (`GET /api/1/{sellerId}/item`)
- Получить статистику объявления (`GET /api/1/statistic/{id}`)

Задача состояла в следующем:
- Составить подробные тест-кейсы для проверки работы API и оформить их в файле `Task 2/TESTCASES.md`.
- Автоматизировать тест-кейсы (реализация – в файле `Task 2/test_api.py`) и запустить их, проверив, что тесты проходят.
- В случае обнаружения дефектов оформить баг-репорты в файле `Task 2/BUGS.md`.
  
---

## Инструкция по использованию

### 1. Клонирование репозитория

```bash
git clone https://github.com/GABASTAR/Avito-Tech-QA-winter-2025.git
cd Avito-Tech-QA-winter-2025
```

### 2. Работа с Task 1

- **Анализ скриншотов:**  
  Перейдите в каталог `Task 1/images/` для просмотра скриншотов.
  
- **Баг-репорты:**  
  Изучите файл `Task 1/BUGS.md`, где оформлены найденные баги, их описание, приоритет и шаги воспроизведения.

### 3. Работа с Task 2

#### Подготовка окружения

1. Убедитесь, что у вас установлен Python 3.7+.
2. Перейдите в каталог `Task 2`.
3. Установите необходимые зависимости:
   ```bash
   pip install pytest requests
   ```

#### Автоматизированное тестирование API

- **Запуск тестов:**
  Из каталога `Task 2` выполните:
  ```bash
  pytest -v
  ```
  Тесты в файле `test_api.py` выполнятся и покажут, какие кейсы проходят, а какие – имеют известные проблемы (отмеченные как xfail). Подробное описание тест-кейсов находится в файле `Task 2/TESTCASES.md`.

- **Баг-репорты по API:**  
  Результаты ручного и автоматизированного тестирования оформлены в файле `Task 2/BUGS.md`.

---

## Дополнительная информация

- **Стиль оформления:**  
  Все документы (BUGS.md, TESTCASES.md) оформлены с учетом рекомендаций предыдущих потоков. Особое внимание уделено четкости описания шагов, ожидаемых результатов и приоритета выявленных дефектов.
  
- **Контактная информация:**  
  Если у вас возникнут вопросы или потребуется дополнительная информация, свяжитесь с автором через email: adam.alfara@yandex.ru.

---

Спасибо за внимание!