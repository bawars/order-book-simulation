import heapq
import uuid
import random
import time

""" Herein we define the Order and OrderBook classes used for maintaining a financial order book. An order book is used
to store buy and sell orders in a financial market, also matching said orders based on criteria such as price (among other things)
There can be different types of orders, but in this project only so-called limit orders are specified."""

class Order:
    """
    Defines what constitutes an order in our order book.

    Attributes:
        side (str): Either 'buy' or 'sell'. Indicates the side of an order. E.g. buying or selling a stock.
        price (float): The price for an order.
        quantity (int): The number of units specified in an order.
        id (UUID): Unique identifier for each order
        timestamp (int): A timestamp; time of order creation.
    """

    def __init__(self, side: str=None, price: float=None, quantity: int=None):
        """ Initializes a new order with attributes for side, price and quantity """
        self.side = side
        self.price = price
        self.quantity = quantity
        self.id = uuid.uuid1()      #unique identifier for each order
        self.timestamp = self.id.time


    def __repr__(self):
        """ for a string representation of an order. """

        return f"(s: {self.side}, p: {self.price}, qty: {self.quantity})"


class OrderBook:
    """
    Constitutes our order book which stores and processes incoming and outgoing orders.

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
        Adds (incoming) orders to either the bid or ask heap.

        Args:
            order (Order): The order to be added.
        """

        if order.side == 'buy':
            heapq.heappush(self.bids, (-order.price, order.timestamp, order))
        elif order.side == 'sell':
            heapq.heappush(self.asks,(order.price, order.timestamp, order))



    def query_book(self):
        """Method for querying the top bid and ask orders in the order book. Useful property of an order book, as it is the 'top of book' where
        the actual trading takes place.

        Returns:
            dict: A dictionary with our top of book orders"""
        top_orders = {}
        if self.bids:
            top_bid = self.bids[0][2]
            top_orders['Bid_side'] = {'side': top_bid.side, 'price': -self.bids[0][0], 'qty': top_bid.quantity}
        else:
            top_orders['Bid_side'] = {'side': None, 'price': None, 'qty': None}

        if self.asks:
            top_ask = self.asks[0][2]
            top_orders['Ask_side'] = {'side': top_ask.side, 'price': self.asks[0][0], 'qty': top_ask.quantity}
        else:
            top_orders['Ask_side'] = {'side': None, 'price': None, 'qty': None}

        return top_orders

    def match_order(self):
        """Algorithm for matching buy and sell orders in our order book. Prioritises firstly price, and secondly arrival time (FIFO approach).

        Returns:
            list: A list of matched orders with pertinent information (IDs, price, quantity, timestamp)"""

        matches = []

        while self.bids and self.asks:
            top_bid = self.bids[0][2]
            top_ask = self.asks[0][2]

            if top_bid.price >= top_ask.price:
                traded_quantity = min(top_bid.quantity, top_ask.quantity)
                top_bid.quantity -= traded_quantity
                top_ask.quantity -= traded_quantity

                match_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                matches.append((f'{top_bid.id}, {top_ask.id}', top_ask.price, traded_quantity, match_time))

                if top_bid.quantity == 0:
                    heapq.heappop(self.bids)
                else:
                    heapq.heapreplace(self.bids, (-top_bid.price, top_bid.timestamp, top_bid))

                if top_ask.quantity == 0:
                    heapq.heappop(self.asks)
                else:
                    heapq.heapreplace(self.asks, (top_ask.price, top_ask.timestamp, top_ask))
            else:
                break

        return matches

    def __repr__(self):
        """Returns a string representation of the order book."""
        bid_orders = [repr(order) for i, j, order in self.bids]
        ask_orders = [repr(order) for i, j, order in self.asks]

        if not bid_orders and not ask_orders:
            return "Order Book is empty"

        return f"Order Book\nBids: {bid_orders}\nAsks: {ask_orders}"



def generate_order(mean, std_dev, quantity_range):
    """
    Generates a random order using a mean price, standard deviation and a quantity range.

    Args:
        mean (float): Mean price of an order.
        std_dev (float): Standard deviation of the price.
        quantity_range (tuple): A tuple for allowed quantity range, in form (min,max).

    Returns:
        Order: A randomly generated order.
    """
    side = random.choice(['buy', 'sell'])
    price = round(random.normalvariate(mean, std_dev))
    quantity = random.randint(*quantity_range)

    return Order(side, price, quantity)