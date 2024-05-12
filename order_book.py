import heapq
import uuid

"""vi ska i detta projekt konstruera en orderbok"""
#general description of an orderbook
""" an order book is a list of buyers and sellers willing to engage in trade, usually trading financial securities.
the order book stores buyers and sellers according to the price they are willing to meet, units willing to buy/sell
among other things.
A matching algorithm is then employed to match a buyer to a seller [given certain criteria are met, like price, among other things]
This makes the order book dynamic as there is an inflow of buyers/sellers and an outflow as they are matched to one another"""

class Order:
    """
    An orderbook consists of different, unique orders. These orders
    will be the objects of this class.

    Attributes:
        side (str): Either 'buy' or 'sell' of an instrument. There are 2 sides.
        price (float): The price for the instrument for either a buyer or seller.
        quantity (int): The number of units one is looking to sell or buy.
    """

    def __init__(self, side: str, price: float, quantity: int):
        """ Initializes a new order with attributes for side, price and quantity """
        self.id = uuid.uuid4()
        self.side = side
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        """ for a string representation of an order. """
        return f"(s: {self.side}, p: {self.price}, q: {self.quantity})"


class OrderBook:
    """
    In the OrderBook class, we will store orders and modify the orderbook
    as new orders come or as orders leave the orderbook on a continous basis.
    Sellers are placed on the 'ask' side of the orderbook, and buyers on the 'bid' side.

    Attributes:
        bids (list): A max-heap to store buy orders.
        asks (list): A min-heap to store sell orders.
    """

    def __init__(self):
        """ we initialize the order book with separate heaps for buy and sell orders."""
        self.bids = []
        self.asks = []


    def add_order(self, order: Order):
        """
        we will add an (incoming) order to either bid or ask heap.

        Args:
            order (Order): The order to be added.
        """
        """heapq är per automitk en minheap. det innebär att
        minsta key'n (priset här) lagras överst.
        genom att invertera tecknet (+ -> -) kommer det största värdet att
        lagras överst för bidsidan = maxheap
        1 -> 2 -> 3     :    -1 , -2, -3   -> """
        if order.side == 'buy':
            heapq.heappush(self.bids, (-order.price, order))
        elif order.side == 'sell':
            heapq.heappush(self.asks,(order.price,order))






    def match_order(self):
        """
        We will need to match orders to one another (i.e. matching buyers and sellers)
        This will, other than accounting for price (which must be equal to match a buyer and seller)
        also utilise a FIFO approach (First-in-First-Out). The first order placed is the first to be matched, if it meets the
        matching criteria.
        """
        pass

    def query_book(self):
        """
        will retrieve current top orders from bid and ask sides of the order book


        Returns:
            (dict): The top buy and sell orders."""

        top_orders = {}

        if self.bids:
            top_bid = self.bids[0][1] #note that bids are stored like (-price, order_object), hence [0] gets us the top most row and [1] gets us the entire order instance allowing us to display both its price and quantity
            print(self.bids[0])
            #print(top_bid)




    def __repr__(self):
        """
        will represent the entire order book as a string.
        """
        return f'({self.bids}, {self.asks})'
        pass
def main():
    orderbok = OrderBook()
    a = Order('buy', 50, 1)
    b = Order('buy', 40, 1)
    c=Order('buy', 60, 1)

    orderbok.add_order(a)
    orderbok.add_order(b)
    orderbok.add_order(c)
    orderbok.query_book()
    print(orderbok)


if __name__ == '__main__':
    main()