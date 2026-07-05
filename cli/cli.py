import argparse
import requests

BASE_URL = "http://127.0.0.1:5000"


def list_items():
    response = requests.get(f"{BASE_URL}/items")
    items = response.json()
    for item in items:
        print(item)


def add_item(name, quantity, price, barcode):
    data = {"name": name, "quantity": quantity, "price": price, "barcode": barcode}
    response = requests.post(f"{BASE_URL}/items", json=data)
    print(response.json())


def update_item(item_id, name, quantity, price):
    data = {}
    if name:
        data["name"] = name
    if quantity is not None:
        data["quantity"] = quantity
    if price is not None:
        data["price"] = price
    response = requests.put(f"{BASE_URL}/items/{item_id}", json=data)
    print(response.json())


def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    print(response.json())

def search_product(name):
    response = requests.get(f"{BASE_URL}/products/search", params={"name": name})
    products = response.json()
    if not products:
        print("No products found (or search is temporarily unavailable).")
        return
    for product in products:
        print(product)

def main():
    parser = argparse.ArgumentParser(description="Inventory CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("name")
    add_parser.add_argument("quantity", type=int)
    add_parser.add_argument("price", type=float)
    add_parser.add_argument("--barcode", default=None)

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--name")
    update_parser.add_argument("--quantity", type=int)
    update_parser.add_argument("--price", type=float)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("id", type=int)

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("name")

    args = parser.parse_args()

    if args.command == "list":
        list_items()
    elif args.command == "add":
        add_item(args.name, args.quantity, args.price, args.barcode)
    elif args.command == "update":
        update_item(args.id, args.name, args.quantity, args.price)
    elif args.command == "delete":
        delete_item(args.id)
    elif args.command == "search":
        search_product(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()