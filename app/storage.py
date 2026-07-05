import json
from app.models import InventoryItem

FILE_PATH = "data/inventory.json"


def load_items():
    with open(FILE_PATH, "r") as f:
        data = json.load(f)
    return [InventoryItem.from_dict(item) for item in data]


def save_items(items):
    data = [item.to_dict() for item in items]
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def get_all():
    return load_items()


def get_by_id(item_id):
    items = load_items()
    for item in items:
        if item.id == item_id:
            return item
    return None


def add_item(item):
    items = load_items()
    items.append(item)
    save_items(items)
    return item


def update_item(item_id, updated_data):
    items = load_items()
    for item in items:
        if item.id == item_id:
            item.name = updated_data.get("name", item.name)
            item.quantity = updated_data.get("quantity", item.quantity)
            item.price = updated_data.get("price", item.price)
            item.barcode = updated_data.get("barcode", item.barcode)
            save_items(items)
            return item
    return None


def delete_item(item_id):
    items = load_items()
    new_items = [item for item in items if item.id != item_id]
    if len(new_items) == len(items):
        return False
    save_items(new_items)
    return True