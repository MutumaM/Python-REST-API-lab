class InventoryItem:
    def __init__(self, id, name, quantity, price, barcode=None):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.barcode = barcode

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "barcode": self.barcode
        }

    @staticmethod
    def from_dict(data):
        return InventoryItem(
            id=data["id"],
            name=data["name"],
            quantity=data["quantity"],
            price=data["price"],
            barcode=data.get("barcode")
        )