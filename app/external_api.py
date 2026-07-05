import requests

BASE_URL = "https://world.openfoodfacts.org"
HEADERS = {"User-Agent": "InventorySystem - Python - Version 1.0"}


def get_product_by_barcode(barcode):
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None

    try:
        data = response.json()
    except ValueError:
        return None

    if data.get("status") != 1:
        return None

    product = data["product"]
    return {
        "name": product.get("product_name"),
        "brand": product.get("brands"),
        "barcode": barcode,
        "image": product.get("image_url"),
        "categories": product.get("categories")
    }


def search_product_by_name(name):
    url = f"{BASE_URL}/api/v2/search"
    params = {
        "search_terms": name,
        "page_size": 5,
        "fields": "product_name,brands,code,image_url"
    }
    response = requests.get(url, params=params, headers=HEADERS)

    if response.status_code != 200:
        return []

    try:
        data = response.json()
    except ValueError:
        return []

    products = data.get("products", [])
    results = []
    for product in products:
        results.append({
            "name": product.get("product_name"),
            "brand": product.get("brands"),
            "barcode": product.get("code"),
            "image": product.get("image_url")
        })
    return results