import heapq
import uuid
import random
import numpy as np
import time

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

    def __init__(self, side: str=None, price: float=None, quantity: int=None):
        """ Initializes a new order with attributes for side, price and quantity """
        self.side = side
        self.price = price
        self.quantity = quantity
        self.id = uuid.uuid1()      #unique identifier for each order
        self.timestamp = self.id.time

        def extract_timestamp(self, uuid1):
            """
            Extracts and converts the timestamp from UUID1.
            UUID1 timestamps are the number of 100-nanosecond intervals since 00:00:00.00, 15 October 1582.
            """
            return (uuid1.time - 0x01B21DD213814000) / 1e7

    def __repr__(self):
        """ for a string representation of an order. """
        #return f"(s: {self.side}, p: {self.price}, qty: {self.quantity}, id: {self.id}, timestamp: {self.timestamp})"

        return f"(s: {self.side}, p: {self.price}, qty: {self.quantity})"


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
            heapq.heappush(self.bids, (-order.price, order.timestamp, order))
        elif order.side == 'sell':
            heapq.heappush(self.asks,(order.price, order.timestamp, order))



    def query_book(self):
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

                matches.append((f'(Bid ID: {top_bid.id}, Ask ID: {top_ask.id}, Agreed price: {top_ask.price}, Traded quantity: {traded_quantity}'))


                #if an order is fully traded out(qty = 0) it should be renmoved from the heap(s)
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


        #print(matches)
        #print(self.bids,self.asks)
        return f'matched orders: {matches}'


    # def __repr__(self):
    #     """
    #     will represent the entire order book as a string.
    #     """
    #     return f'Order Book(Bids: {self.bids}, Asks: {self.asks})'

    def __repr__(self):
        bid_orders = [repr(order) for i, j, order in self.bids]
        ask_orders = [repr(order) for i, j, order in self.asks]

        if not bid_orders and not ask_orders:
            return "Order Book is empty"

        return f"Order Book\nBids: {bid_orders}\nAsks: {ask_orders}"
    # def __repr__(self):
    #     """
    #     Will represent the entire order book as a string.
    #     """
    #     bid_orders = [f"(price: {-price}, qty: {order.quantity}, ts: {order.timestamp})" for price, _, order in
    #                   self.bids]
    #     ask_orders = [f"(price: {price}, qty: {order.quantity}, ts: {order.timestamp})" for price, _, order in
    #                   self.asks]
    #     return f"Order Book\nBids: {bid_orders}\nAsks: {ask_orders}"



def generate_order(mean, std_dev, quantity_range):
    side = random.choice(['buy', 'sell'])
    price = round(random.normalvariate(mean, std_dev))
    quantity = random.randint(*quantity_range)

    return Order(side, price, quantity)


def simulate_orders(order_book, duration, rate, mean_price, std_dev, quantity_range):

    end_time = time.time() + duration

    while time.time() < end_time:
        time_to_next_order = np.random.exponential(1 / rate)
        time.sleep(time_to_next_order)



        order = generate_order(mean_price, std_dev, quantity_range)
        order_book.add_order(order)
        #print(f'whole order book: {order_book}: ')

        print(f' top of book: {order_book.query_book()}')
        print(order_book.match_order())
        # print(f"Order Book:\n{order_book}\n")





def main():
    # tom orderbok från början
    enbok = OrderBook()

    # Test 1: Ensure the order book is initialized correctly
    assert enbok is not None, "OrderBook should be initialized."
    #
    # # a first test order 'a'
    # a = Order(side='buy', price=45, quantity=10)
    # enbok.add_order(a)
    # assert (a.side, a.price, a.quantity) == ('buy', 45, 10)
    #
    # # adding a second order 'b'
    # b = Order(side='sell', price=50, quantity=5)
    # enbok.add_order(b)
    #
    # # Top of book should return our two orders that are closest in price
    # top_orders_1 = enbok.query_book()
    # #print(top_orders)
    # assert top_orders_1['Bid_side']['side'] == 'buy'
    # assert top_orders_1['Bid_side']['price'] == 45
    #
    # assert top_orders_1['Ask_side']['side'] == 'sell'
    # assert top_orders_1['Ask_side']['price'] == 50
    #
    # # adding a third order 'c' which will replace order b in query_book() w/ sell prie of 45 to match bid side
    # c = Order(side='sell', price=45, quantity=2)
    # enbok.add_order(c)
    # top_orders_2 = enbok.query_book()
    # #print(enbok.query_book())
    # #assert top_orders['Ask_side']['quantity'] == 5
    # assert top_orders_2['Ask_side']['price'] == 45

    #print(top_orders_2)
    # eventuellt ett till ordertest men nu där vi jämför på tidsbasis och inte pris


    ##### matching orders ######
    # the two orders at price level 45 should be executed, and then min value of their qts removed from the heap
    # 1 buy order @45 for 10 units, 1 sell order @45 for 2 units --> thus 2 units should be traded,
    # and 8 units of the buy order should remain in top of book and our second sell order take top of book position

    #print(f'top of book before matching trades {enbok.query_book()}')
    #print(f'{enbok.match_order()}')
    #print(f'top of book after matching trades {enbok.query_book()}')



    # top of book ska returnera våra två ordrar som är närmast i pris, och om pris likadant -> de som ankom först i tid





    # enbok.add_order(d)
    # enbok.add_order(a)
    # enbok.add_order(b)
    # enbok.add_order(c)

    #print("Initial Order Book:", enbok)
    #print("Query Book:", enbok.query_book())
    #print("Match Orders:", enbok.match_order())
    #print("Order Book after Matching:", enbok)
    # Simulate orders
    simulate_orders(enbok, duration=5, rate=1, mean_price=50, std_dev=2, quantity_range=(1, 20))

if __name__ == '__main__':
    main()