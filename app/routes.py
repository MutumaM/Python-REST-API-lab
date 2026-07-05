from flask import Blueprint, request, jsonify
from app import storage
from app.models import InventoryItem
from app import external_api
import itertools


bp = Blueprint("routes", __name__)
id_counter = itertools.count(1)


@bp.route("/items", methods=["GET"])
def get_items():
    items = storage.get_all()
    return jsonify([item.to_dict() for item in items])


@bp.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = storage.get_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item.to_dict())


@bp.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    new_item = InventoryItem(
        id=next(id_counter),
        name=data["name"],
        quantity=data["quantity"],
        price=data["price"],
        barcode=data.get("barcode")
    )
    storage.add_item(new_item)
    return jsonify(new_item.to_dict()), 201


@bp.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    updated = storage.update_item(item_id, data)
    if updated is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(updated.to_dict())

@bp.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    success = storage.delete_item(item_id)
    if not success:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Item deleted"})

@bp.route("/products/barcode/<barcode>", methods=["GET"])
def product_by_barcode(barcode):
    product = external_api.get_product_by_barcode(barcode)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


@bp.route("/products/search", methods=["GET"])
def product_by_name():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Please provide a name query param"}), 400
    results = external_api.search_product_by_name(name)
    return jsonify(results)