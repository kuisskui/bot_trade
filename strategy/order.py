class Order:
    def __init__(self, symbol, lot, order_type):
        self.symbol: str = symbol
        self.lot: float = lot
        self.order_type: str = order_type
