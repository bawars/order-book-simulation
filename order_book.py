import heapq
import uuid
from datetime import datetime
import time
import numpy as np

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

    def __init__(self, side: str=None, price: float=None, quantity: int=None, seq=None):
        """ Initializes a new order with attributes for side, price and quantity """
        self.side = side
        self.price = price
        self.quantity = quantity
        self.id = uuid.uuid4()      #unique identifier for each order
        self.seq = seq

    def __repr__(self):
        """ for a string representation of an order. """
        return f"(s: {self.side}, p: {self.price}, qty: {self.quantity}, id: {self.id}, seq: {self.seq}))"


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
        self.sequence_number = 0  # initialise a sequence number


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

        self.sequence_number += 1  # we incrementr the seq number for each added order
        order.seq = self.sequence_number

        if order.side == 'buy':
            heapq.heappush(self.bids, (-order.price, order.seq, order))
        elif order.side == 'sell':
            heapq.heappush(self.asks,(order.price, order.seq, order))



    def query_book(self):
        top_orders = {}
        if self.bids:
            top_bid = self.bids[0][2]
            top_orders['top_bid'] = {'side': top_bid.side, 'price': -self.bids[0][0], 'qty': top_bid.quantity, 'seq': top_bid.seq}
        else:
            top_orders['top_bid'] = {'side': None, 'price': None, 'qty': None, 'seq': None}

        if self.asks:
            top_ask = self.asks[0][2]
            top_orders['top_ask'] = {'side': top_ask.side, 'price': self.asks[0][0], 'qty': top_ask.quantity, 'seq': top_ask.seq}
        else:
            top_orders['top_ask'] = {'side': None, 'price': None, 'qty': None, 'seq': None}

        return top_orders


    def match_order(self):
        """
        We will need to match orders to one another (i.e. matching buyers and sellers)
        This will, other than accounting for price (which must be equal to match a buyer and seller)
        also utilise a FIFO approach (First-in-First-Out). The first order placed is the first to be matched, if it meets the
        matching criteria.
        """

        # vi vill kolla om top of book har matchande priser:

        matches = []

        while self.bids and self.asks:
            #top_of_book = (self.bids[0][1], self.asks[0][1])
            top_bid = self.bids[0][2]
            top_ask = self.asks[0][2]



            if top_bid.price >= top_ask.price:
                # we trade out the quantities of the smaller order
                traded_quantity = min(top_bid.quantity, top_ask.quantity)
                top_bid.quantity -= traded_quantity
                top_ask.quantity -= traded_quantity

                matches.append((top_bid.id, top_ask.id, traded_quantity, top_ask.price))


                #if an order is fully traded out(qty = 0) it should be renmoved from the heap(s)
                if top_bid.quantity == 0:
                    heapq.heappop(self.bids)
                else:
                    heapq.heapreplace(self.bids, (-top_bid.price, top_bid.seq, top_bid))


                if top_ask.quantity == 0:
                    heapq.heappop(self.asks)
                else:
                    heapq.heapreplace(self.asks, (-top_ask.price, top_ask.seq, top_ask))

            else:
                break


        #print(matches)
        #print(self.bids,self.asks)
        return f'matched orders: {matches}'




    def __repr__(self):
        """
        will represent the entire order book as a string.
        """
        return f'({self.bids}, {self.asks})'

def main():
    enbok = OrderBook()
    a = Order(side='buy', price=50, quantity=10)
    b=Order('sell', 50, 5)
    #time.sleep(0.0000001)

    c = Order('sell', 50, 2)

    enbok.add_order(a)
    enbok.add_order(b)
    enbok.add_order(c)

    print(enbok)
    print(enbok.query_book())
    #print(enbok.match_order())



if __name__ == '__main__':
    main()