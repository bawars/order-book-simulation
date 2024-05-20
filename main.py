from gui_orderbook import OrderBookGUI
from order_book import Order, OrderBook, generate_order
import tkinter as tk


def run_assertion_tests():
    """function with which we run our testing"""

    # testing our Order class
    order = Order(side='buy', price=100, quantity=10)
    assert order.side == 'buy'
    assert order.price == 100
    assert order.quantity == 10
    assert order.id is not None
    assert order.timestamp is not None
    assert repr(order) == "(s: buy, p: 100, qty: 10)"
    # print("Order class tests passed")

    # testing OrderBook class
    order_book = OrderBook()
    assert order_book is not None

    # setting up a few orders to be tested in our order book
    orders_setup = [
        ('buy', 50, 5),
        ('sell', 49, 5),
        ('buy', 45, 10)
    ]
    orders = [Order(*order) for order in orders_setup]

    ### add_order ###
    order_book.add_order(orders[0])
    assert len(order_book.bids) == 1
    assert len(order_book.asks) == 0

    order_book.add_order(orders[1])
    assert len(order_book.bids) == 1
    assert len(order_book.asks) == 1
    # print("OrderBook add_order tests passed")

    ### testing query_book ####
    top_of_book_1 = order_book.query_book()
    assert top_of_book_1['Bid_side']['price'] == 50
    assert top_of_book_1['Bid_side']['side'] == 'buy'
    assert top_of_book_1['Ask_side']['qty'] == 5
    # print("OrderBook query_book tests passed")

    ### testing match_order ###
    order_book.add_order(orders[2])

    matches = order_book.match_order()
    assert len(matches) == 1
    assert matches[0][1] == 49
    assert matches[0][2] == 5

    top_of_book = order_book.query_book()  # we now have a new 'top of book'
    assert top_of_book['Bid_side']['price'] == 45
    assert top_of_book['Ask_side']['qty'] == None  # ask side is now empty -> no matches available
    matches = order_book.match_order()
    assert len(matches) == 0
    # print("OrderBook match_order tests passed")

    ### testing generate_order function ###
    order = generate_order(100, 10, (1, 10))
    assert order.side in ['buy', 'sell']
    # assert 70 <= order.price <= 130    #--> since order.price is a normally dist. variable with std.dev > 0 there can always be some outliers
    assert 1 <= order.quantity <= 10
    # print("generate_order function tests passed")

    ### running the GUI ###
    root = tk.Tk()
    app = OrderBookGUI(root)

    def simulate_gui():
        """ we will simulate a run with user input parameters given below"""
        app.duration_entry.insert(0, '20')
        assert app.duration_entry.get() == '20'

        app.rate_entry.insert(0, '2')
        app.mean_price_entry.insert(0, '50')
        app.std_dev_entry.insert(0, '5')

        app.quantity_range_entry.insert(0, '1,10')
        assert app.quantity_range_entry.get() == ('1,10')

        app.start_simulation()

        def check_during_simulation():
            assert app.simulation_running == True


        def stop_and_check_simulation():
            app.stop_simulation()
            root.after(2000, final_checks)

        def final_checks():
            assert app.simulation_running == False
            assert app.simulation_thread is None

        #root.after schedules a function call after specified time in ms
        root.after(12500, check_during_simulation)
        root.after(15000, stop_and_check_simulation)
        root.after(20000, root.destroy)

    root.after(10, simulate_gui)
    root.mainloop()


if __name__ == '__main__':
    """ run_assertion_tests() will include a pre-made simulated run. 

    After it is completed, you can create your own simulation with your parameters of choice
    for the 'rate' parameter, I suggest starting small (<10) and then bumping it up if you want to experiment """

    run_assertion_tests()
    print("All tests passed successfully")

    root = tk.Tk()
    app = OrderBookGUI(root)
    root.mainloop()