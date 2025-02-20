# Тест-кейсы для проверки API микросервиса объявлений

Данный документ содержит подробное описание тест-кейсов для проверки работы API микросервиса, отвечающего за создание и получение объявлений. Каждый кейс описывает цель проверки, пошаговую инструкцию, ожидаемый результат и фактический результат, основанный на выполнении автотестов (см. файл test_api.py). Некоторые тесты помечены как «ожидающие сбой» (xfail) ввиду известных дефектов, подробнее о которых указано в файле BUGS.md.

> **Примечание:** Фактические результаты в некоторых тестах указывают на несоответствие ожидаемому поведению (например, возврат статуса 200 вместо 400 или несовпадение значения поля `name`). Эти отклонения зафиксированы в автотестах и документированы как баги (например, API_BUG_001, API_BUG_002/003/004 и т.д.).

---

## API_TC_001: Создание объявления с типовыми данными (POST /api/1/item)

**Приоритет:** Высокий

**Цель:** Проверить, что API успешно принимает корректный POST-запрос для создания объявления и возвращает статус 200, а затем GET-запрос возвращает данные, совпадающие с исходными.

**Шаги:**
1. Отправить POST-запрос по адресу `/api/1/item` с телом:
   ```json
   {
     "sellerId": 12416,
     "name": "iPhone XR",
     "price": 1500,
     "statistics": {
       "contacts": 50,
       "likes": 12,
       "viewCount": 416
     }
   }
   ```
2. Убедиться, что ответ имеет статус 200 и содержит поле `status` со строкой вида:
   ```
   "Announcement saved - <item_id>"
   ```
3. Извлечь идентификатор объявления из ответа.
4. Выполнить GET-запрос по адресу `/api/1/item/{item_id}`.
5. Сравнить полученные поля (`sellerId`, `name`, `price`, `statistics`) с данными, отправленными в POST-запросе.

**Ожидаемый результат:**
- Статус ответа — 200.
- Данные, возвращаемые GET-запросом, полностью совпадают с отправленными (формат даты `createdAt` должен соответствовать ISO 8601).

**Фактический результат:**  
- POST-запрос возвращает статус 200.
- GET-запрос возвращает данные, однако значение поля `name` не совпадает с ожидаемым ("iPhone XR"). Тест помечен как xfail с сообщением:
  > "Known bug API_BUG_001: 'name' field does not match expected value"

---

## API_TC_002: Проверка верхней границы значения sellerId (POST /api/1/item)

**Приоритет:** Высокий

**Цель:** Убедиться, что API корректно обрабатывает значение `sellerId`, близкое к верхнему пределу допустимого диапазона.

**Шаги:**
1. Отправить POST-запрос с телом:
   ```json
   {
     "sellerId": 999999,
     "name": "iPhone XR",
     "price": 1500,
     "statistics": {
       "contacts": 50,
       "likes": 12,
       "viewCount": 416
     }
   }
   ```
2. Проверить, что возвращается статус 200 и из ответа можно извлечь идентификатор объявления.
3. Выполнить GET-запрос по адресу `/api/1/item/{item_id}` и сравнить полученные данные с исходными.

**Ожидаемый результат:**
- Статус ответа — 200.
- Все поля, включая `sellerId` (999999), совпадают с переданными значениями.

**Фактический результат:**  
- POST-запрос с sellerId 999999 возвращает статус 200, но значение поля `name` не соответствует ожидаемому, что зафиксировано как баг API_BUG_001 (тест помечен как xfail).

---

## API_TC_003: Проверка нижней границы значения sellerId (POST /api/1/item)

**Приоритет:** Высокий

**Цель:** Проверить корректную обработку минимально допустимого значения `sellerId`.

**Шаги:**
1. Отправить POST-запрос с телом:
   ```json
   {
     "sellerId": 111111,
     "name": "iPhone XR",
     "price": 1500,
     "statistics": {
       "contacts": 50,
       "likes": 12,
       "viewCount": 416
     }
   }
   ```
2. Убедиться, что сервер возвращает статус 200 и корректно формирует идентификатор объявления.
3. Выполнить GET-запрос по адресу `/api/1/item/{item_id}`.
4. Сравнить полученные данные с исходным payload.

**Ожидаемый результат:**
- Статус — 200.
- Данные объявления (в том числе `sellerId`: 111111) полностью соответствуют отправленным значениям.

**Фактический результат:**  
- GET-запрос возвращает статус 200, однако поле `name` не совпадает с ожидаемым ("iPhone XR"). Тест помечен как xfail.

---

## API_TC_004: Проверка отсутствия обязательных полей (POST /api/1/item)

**Приоритет:** Высокий

**Цель:** Убедиться, что API возвращает ошибку (400 Bad Request) при отсутствии любого из обязательных полей.

**Шаги:**
1. Для каждого варианта:
   - Удалить из тела запроса одно из обязательных полей: `sellerId`, `name`, `price` или `statistics`.
   - Отправить POST-запрос по адресу `/api/1/item`.
2. Проверить статус ответа и сообщение об ошибке.

**Ожидаемый результат:**
- Для каждого запроса статус должен быть 400, с сообщением, указывающим на отсутствие конкретного обязательного поля.

**Фактический результат:**  
- API возвращает статус 200 во всех случаях, что противоречит ожиданиям. Тесты помечены как xfail с сообщением:
  > "Known bug API_BUG_002/003/004: API returns 200 OK when '<поле>' is missing"

---

## API_TC_005: Проверка некорректных значений для sellerId (POST /api/1/item)

**Приоритет:** Высокий

**Цель:** Проверить, что API отклоняет запросы с неверным форматом или значениями для `sellerId`.

**Шаги для воспроизведения:**
1. Отправить POST-запрос, где `sellerId` равен -1.
2. Отправить POST-запрос, где `sellerId` – строка (например, "abc123").
3. Отправить POST-запрос, где `sellerId` – чрезмерно большое число (например, 999999999999999).
4. Проверить статус каждого запроса.

**Ожидаемый результат:**
- Для каждого запроса должен быть возвращён статус 400 с описанием ошибки.

**Фактический результат:**  
- Для значений -1 и 999999999999999 сервер возвращает статус 200 (тесты помечены как xfail с сообщением: "Known bug API_BUG_004: API returns 200 OK for invalid sellerId").
- Для "abc123" сервер корректно возвращает статус 400.

---

## API_TC_006: Проверка некорректных значений для поля name (POST /api/1/item)

**Приоритет:** Высокий

**Цель:** Проверить, что API отклоняет запросы с недопустимыми значениями поля `name`.

**Шаги для воспроизведения (рекомендуемые сценарии):**
1. Отправить POST-запрос, где `name` задано как слишком короткая строка (например, "X").
2. Отправить POST-запрос, где `name` состоит только из цифр (например, "123456").
3. Отправить POST-запрос, где `name` состоит только из пробелов.
4. Отправить POST-запрос, где длина `name` превышает допустимый максимум.
5. Отправить POST-запрос без поля `name` (см. API_TC_004).

**Ожидаемый результат:**
- Для каждого варианта сервер должен вернуть статус 400 с сообщением об ошибке, указывающим на некорректное значение поля `name`.

**Фактический результат:**  
- Аналогичные проверки (например, отсутствие поля `name`) показывают, что API возвращает статус 200, что является ошибкой, как зафиксировано в API_TC_004.

---

## API_TC_007: Проверка некорректных значений для поля price (POST /api/1/item)

**Приоритет:** Высокий

**Цель:** Убедиться, что API отклоняет запросы, где значение поля `price` является неверным.

**Шаги для воспроизведения (рекомендуемые сценарии):**
1. Отправить POST-запрос с отрицательным значением для `price` (например, -1500).
2. Отправить POST-запрос, где `price` задан как строка (например, "1500").
3. Отправить POST-запрос, где `price` имеет значение null.
4. Отправить POST-запрос, где `price` равно 0.
5. Отправить POST-запрос с чрезмерно большим значением для `price`.
6. Отправить POST-запрос без поля `price` (см. API_TC_004).

**Ожидаемый результат:**
- Для каждого варианта сервер должен вернуть статус 400 с соответствующим сообщением об ошибке для поля `price`.

**Фактический результат:**  
- При отсутствии поля `price` сервер возвращает статус 200 (как и в API_TC_004). Остальные сценарии не протестированы отдельно, но предполагается аналогичное поведение (возврат 200 вместо 400).

---

## API_TC_008: Проверка некорректных значений для поля statistics (POST /api/1/item)

**Приоритет:** Высокий

**Цель:** Проверить, что API корректно обрабатывает неверно заданное поле `statistics`.

**Шаги для воспроизведения:**
1. Отправить POST-запрос, где `statistics` имеет значение null:
   ```json
   {
     "sellerId": 12416,
     "name": "iPhone XR",
     "price": 1500,
     "statistics": null
   }
   ```
2. Отправить POST-запрос, где в `statistics` значения заданы отрицательно:
   ```json
   {
     "sellerId": 12416,
     "name": "iPhone XR",
     "price": 1500,
     "statistics": {
         "contacts": -50,
         "likes": -12,
         "viewCount": -416
     }
   }
   ```
3. Отправить POST-запрос, где значения в `statistics` указаны как строки:
   ```json
   {
     "sellerId": 12416,
     "name": "iPhone XR",
     "price": 1500,
     "statistics": {
         "contacts": "fifty",
         "likes": "twelve",
         "viewCount": "four hundred"
     }
   }
   ```
4. Отправить POST-запрос без поля `statistics`.

**Ожидаемый результат:**
- Для каждого запроса должен быть возвращён статус 400.
- Тело ответа должно содержать сообщение о некорректном формате или отсутствии поля `statistics`.

**Фактический результат:**  
- API возвращает статус 200 при отсутствии поля `statistics` (см. API_TC_004); для других вариантов поведение аналогично, что свидетельствует о дефекте.

---

## API_TC_009: Пустое тело запроса (POST /api/1/item)

**Приоритет:** Высокий

**Цель:** Проверить обработку запроса без содержимого.

**Шаги для воспроизведения:**
1. Отправить POST-запрос по адресу `/api/1/item` с телом: `{}`.

**Ожидаемый результат:**
- Статус ответа — 400 Bad Request.
- Тело ответа должно содержать сообщение об ошибке, указывающее на некорректное тело запроса.

**Фактический результат:**  
- API возвращает статус 200, что противоречит ожиданиям; тест помечен как xfail с сообщением:
  > "Known bug API_BUG_003: API returns 200 OK when body is empty"

---

## API_TC_010: Получение объявления по идентификатору (GET /api/1/item/{id})

**Приоритет:** Высокий

**Цель:** Проверить, что GET-запрос возвращает корректное объявление по заданному идентификатору.

**Шаги для воспроизведения:**
1. Создать объявление (см. API_TC_001) и извлечь его идентификатор.
2. Выполнить GET-запрос по адресу `/api/1/item/{item_id}`.
3. Убедиться, что ответ содержит:
   - Поле `createdAt` в формате ISO 8601.
   - Поле `id`, совпадающее с извлечённым идентификатором.
   - Поля `name`, `price`, `sellerId` и `statistics`, совпадающие с исходными данными.

**Ожидаемый результат:**
- Статус — 200.
- Все возвращаемые поля соответствуют данным, переданным при создании объявления.

**Фактический результат:**  
- GET-запрос возвращает статус 200, однако значение поля `name` не совпадает с ожидаемым ("iPhone XR"). Это зафиксировано как баг API_BUG_001.

---

## API_TC_011: Проверка запроса с некорректным идентификатором объявления (GET /api/1/item/{id})

**Приоритет:** Высокий

**Цель:** Убедиться, что API возвращает ошибку при использовании некорректного формата идентификатора объявления.

**Шаги для воспроизведения:**
1. Отправить GET-запрос по адресу `/api/1/item/{id}` с использованием следующих значений:
   - Число (например, 1234567890)
   - Строка "invalidID"
   - Null, пустая строка или строка, состоящая только из пробелов.
2. Проверить статус ответа для каждого варианта.

**Ожидаемый результат:**
- Для каждого варианта статус должен быть 400 Bad Request.
- Ответ содержит сообщение о некорректном идентификаторе.

**Фактический результат:**  
- Большинство вариантов возвращают статус 400, за исключением некоторых случаев (например, пустая строка) – тест помечен как xfail в одном из вариантов с сообщением, связанным с известной ошибкой.

---

## API_TC_012: Получение статистики объявления (GET /api/1/statistic/{id})

**Приоритет:** Высокий

**Цель:** Проверить корректное получение статистики (contacts, likes, viewCount) для объявления.

**Шаги для воспроизведения:**
1. Создать объявление (см. API_TC_001) и извлечь его идентификатор.
2. Отправить GET-запрос по адресу `/api/1/statistic/{item_id}`.
3. Проверить, что ответ содержит поля:
   - `contacts`
   - `likes`
   - `viewCount`
   При этом значения должны быть неотрицательными и совпадать с теми, что были переданы в POST.

**Ожидаемый результат:**
- Статус — 200.
- Статистика совпадает с исходными значениями.

**Фактический результат:**  
- GET-запрос возвращает статус 200, однако значение `likes` отличается от ожидаемого (тест помечен как xfail с сообщением "Known bug API_BUG_006: 'likes' value in statistic does not match expected").

---

## API_TC_013: Проверка запроса статистики с некорректным идентификатором (GET /api/1/statistic/{id})

**Приоритет:** Высокий

**Цель:** Убедиться, что API возвращает ошибку при запросе статистики с неверным идентификатором.

**Шаги для воспроизведения:**
1. Отправить GET-запрос по адресу `/api/1/statistic/{id}`, используя некорректные значения:
   - Число (например, 1234567890)
   - Строка с особыми символами (например, "!@#$%^&*()")
   - Пустая строка или строка, состоящая только из пробелов.
2. Проверить статус ответа.

**Ожидаемый результат:**
- Статус — 400 Bad Request.
- Ответ содержит сообщение об ошибке, указывающее на некорректный идентификатор.

**Фактический результат:**  
- При использовании некорректных идентификаторов сервер возвращает статус 400, что соответствует ожидаемому результату.

---

## API_TC_014: Получение списка объявлений продавца (GET /api/1/{sellerId}/item)

**Приоритет:** Средний

**Цель:** Проверить, что API возвращает список объявлений для указанного продавца.

**Шаги для воспроизведения:**
1. Создать одно или несколько объявлений с определенным `sellerId` (например, 12416).
2. Отправить GET-запрос по адресу `/api/1/{sellerId}/item`.
3. Проверить, что ответ является массивом:
   - Если объявления существуют – массив содержит элементы;
   - Если объявлений нет – возвращается пустой массив.

**Ожидаемый результат:**
- Статус — 200.
- Ответ – массив с данными объявлений или пустой массив.

**Фактический результат:**  
- GET-запрос возвращает статус 200. Если ответ приходит в виде словаря, тест помечается как xfail с сообщением:
  > "Known bug API_BUG_007: Response format for seller items is incorrect"

---

## API_TC_015: Проверка некорректного значения sellerId при получении объявлений (GET /api/1/{sellerId}/item)

**Приоритет:** Средний

**Цель:** Убедиться, что API возвращает ошибку при передаче недопустимого значения `sellerId` для получения списка объявлений.

**Шаги для воспроизведения:**
1. Отправить GET-запрос по адресу `/api/1/{sellerId}/item` с использованием следующих недопустимых значений:
   - Значение, выходящее за допустимый диапазон (например, 1000000 или 111110).
   - Строковое значение с недопустимыми символами (например, "invalidSeller").
2. Проверить статус ответа для каждого варианта.

**Ожидаемый результат:**
- Статус — 400 Bad Request.
- Ответ содержит сообщение об ошибке, связанное с некорректным значением `sellerId`.

**Фактический результат:**  
- В некоторых случаях сервер возвращает статус 200 вместо 400, что зафиксировано как дефект (согласно баг-репорту API_BUG_008).

---