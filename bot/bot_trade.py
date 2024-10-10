import script.mt5.mt5_api as mt5
from strategy.order import Order


class BotTrade:
    def __init__(self, bot_id, lot):
        self.bot_id: int = bot_id
        self.lot = lot
        self.position_ticket = None

    def trade(self, order: Order):
        if order.order_type == 'buy':
            self.position_ticket = mt5.place_trade(
                order.symbol,
                self.lot,
                order.order_type,
            )
        elif order.order_type == 'sell':
            self.position_ticket = mt5.place_trade(
                order.symbol,
                self.lot,
                order.order_type,
            )
        elif order.order_type == 'exit':
            position = mt5.positions_get(ticket=self.position_ticket)
            mt5.close_position(position)
            self.position_ticket = None
        else:
            pass

    def update(self, order: Order):
        self.trade(order)
