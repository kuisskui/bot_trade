import script.mt5.mt5_api as mt5
from strategy.order import Order


class BotTrade:
    def __init__(self, bot_id, lot):
        self.bot_id: int = bot_id
        self.lot = lot
        self.position_ticket = None

    def trade(self, order: Order):
        if order.order_type == 'buy':
            self.exit_order()
            self.position_ticket = mt5.place_trade(
                order.symbol,
                self.lot,
                order.order_type,
            )
        elif order.order_type == 'sell':
            self.exit_order()
            self.position_ticket = mt5.place_trade(
                order.symbol,
                self.lot,
                order.order_type,
            )
        elif order.order_type == 'exit':
            self.exit_order()
        else:
            pass

    def update(self, order: Order):
        self.trade(order)

    def exit_order(self):
        if self.position_ticket is not None:
            position = mt5.positions_get(ticket=self.position_ticket)
            mt5.close_position(position)
            self.position_ticket = None
