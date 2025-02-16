import requests
import pytest

BASE_URL = "https://qa-internship.avito.com/api/1"

def create_item(payload):
    url = f"{BASE_URL}/item"
    return requests.post(url, json=payload)

def get_item(item_id):
    url = f"{BASE_URL}/item/{item_id}"
    return requests.get(url)

def get_statistic(item_id):
    url = f"{BASE_URL}/statistic/{item_id}"
    return requests.get(url)

def get_items_by_seller(seller_id):
    url = f"{BASE_URL}/{seller_id}/item"
    return requests.get(url)


# --------------------------
# Положительные тест-кейсы
# --------------------------

@pytest.mark.parametrize("seller_id", [12416, 999999, 111111])
def test_create_item_valid(seller_id):
    """
    API_TC_001, API_TC_002, API_TC_003:
    Создание объявления с корректными данными.
    """
    payload = {
        "sellerId": seller_id,
        "name": "iPhone XR",
        "price": 1500,
        "statistics": {
            "contacts": 50,
            "likes": 12,
            "viewCount": 416
        }
    }
    response = create_item(payload)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    resp_json = response.json()
    assert "status" in resp_json, "Response does not contain 'status' field"
    try:
        item_id = resp_json["status"].split(" - ")[1]
    except IndexError:
        pytest.fail("Response status format unexpected")
    
    # Получаем объявление
    get_response = get_item(item_id)
    assert get_response.status_code == 200, f"GET item expected 200 OK, got {get_response.status_code}"
    item_data = get_response.json()[0]
    
    # Из-за известного бага API_BUG_001 поле name может отличаться
    if item_data.get("name") != payload["name"]:
        pytest.xfail("Known bug API_BUG_001: 'name' field does not match expected value")
    
    assert item_data.get("sellerId") == payload["sellerId"], "sellerId mismatch"
    assert item_data.get("price") == payload["price"], "price mismatch"
    stats = item_data.get("statistics", {})
    assert stats.get("contacts") == payload["statistics"]["contacts"], "contacts mismatch"
    assert stats.get("likes") == payload["statistics"]["likes"], "likes mismatch"
    assert stats.get("viewCount") == payload["statistics"]["viewCount"], "viewCount mismatch"


# --------------------------
# Негативные тест-кейсы
# --------------------------

@pytest.mark.parametrize("missing_field", ["sellerId", "name", "price", "statistics"])
def test_create_item_missing_fields(missing_field):
    """
    API_TC_004:
    Проверка создания объявления при отсутствии обязательного поля.
    Ожидается статус 400, но из-за багов API возвращает 200.
    """
    payload = {
        "sellerId": 12416,
        "name": "iPhone XR",
        "price": 1500,
        "statistics": {
            "contacts": 50,
            "likes": 12,
            "viewCount": 416
        }
    }
    payload.pop(missing_field)
    response = create_item(payload)
    if response.status_code == 200:
        pytest.xfail(f"Known bug API_BUG_002/003/004: API returns 200 OK when '{missing_field}' is missing")
    assert response.status_code == 400, f"Expected 400 Bad Request when '{missing_field}' is missing"


@pytest.mark.parametrize("invalid_sellerId", [-1, "abc123", 999999999999999])
def test_create_item_invalid_sellerId(invalid_sellerId):
    """
    API_TC_005:
    Проверка создания объявления с некорректными значениями sellerId.
    """
    payload = {
        "sellerId": invalid_sellerId,
        "name": "iPhone XR",
        "price": 1500,
        "statistics": {
            "contacts": 50,
            "likes": 12,
            "viewCount": 416
        }
    }
    response = create_item(payload)
    if response.status_code == 200:
        pytest.xfail("Known bug API_BUG_004: API returns 200 OK for invalid sellerId")
    assert response.status_code == 400


def test_create_item_empty_body():
    """
    API_TC_009:
    Проверка отправки запроса POST без тела.
    """
    url = f"{BASE_URL}/item"
    response = requests.post(url, json={})
    if response.status_code == 200:
        pytest.xfail("Known bug API_BUG_003: API returns 200 OK when body is empty")
    assert response.status_code == 400


@pytest.mark.parametrize("invalid_id", [1234567890, "1234567890", None, "", "      "])
def test_get_item_invalid_id(invalid_id):
    """
    API_TC_011:
    Проверка GET запроса с некорректным идентификатором объявления.
    """
    url = f"{BASE_URL}/item/{invalid_id}"
    response = requests.get(url)
    if response.status_code == 404:
        pytest.xfail("Known bug API_BUG_003: API returns 404 OK when body is empty")
    assert response.status_code == 400, f"Expected 400 Bad Request for invalid id: {invalid_id}"


def test_get_statistic_valid():
    """
    API_TC_012:
    Проверка получения статистики объявления по его id.
    """
    payload = {
        "sellerId": 12416,
        "name": "iPhone XR",
        "price": 1500,
        "statistics": {
            "contacts": 50,
            "likes": 12,
            "viewCount": 416
        }
    }
    response = create_item(payload)
    assert response.status_code == 200
    try:
        item_id = response.json()["status"].split(" - ")[1]
    except Exception:
        pytest.fail("Unable to extract item id from response")
    
    stat_response = get_statistic(item_id)
    assert stat_response.status_code == 200
    stat_data = stat_response.json()[0]
    if stat_data.get("likes") != payload["statistics"]["likes"]:
        pytest.xfail("Known bug API_BUG_006: 'likes' value in statistic does not match expected")
    assert stat_data.get("contacts") == payload["statistics"]["contacts"]
    assert stat_data.get("likes") == payload["statistics"]["likes"]
    assert stat_data.get("viewCount") == payload["statistics"]["viewCount"]


def test_get_items_by_seller_valid():
    """
    API_TC_014:
    Проверка получения списка объявлений продавца по корректному sellerId.
    """
    seller_id = 12416
    payload = {
        "sellerId": seller_id,
        "name": "iPhone XR",
        "price": 1500,
        "statistics": {
            "contacts": 50,
            "likes": 12,
            "viewCount": 416
        }
    }
    response = create_item(payload)
    assert response.status_code == 200
    
    items_response = get_items_by_seller(seller_id)
    assert items_response.status_code == 200
    items_data = items_response.json()
    # Если ответ приходит в виде словаря, считаем это ошибкой формата
    if isinstance(items_data, dict):
        pytest.xfail("Known bug API_BUG_007: Response format for seller items is incorrect")
    else:
        assert isinstance(items_data, list)
        assert len(items_data) > 0, "Expected at least one item in seller's items list"