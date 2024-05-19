import tkinter as tk
from tkinter import ttk
from order_book import OrderBook, generate_order
import threading
import time
import numpy as np


class OrderBookGUI:
    def __init__(self, root):

        """ Initializes our OrderBookGUI class along with setting up the main application window, creates widgets for said application
        and initializes the orderbook, matched orders list and simulation control variables.

        Args:
            root (tk.Tk): Tkinter application's root window

        Attributes: root (tk.Tk): root window for Tkinter application
        order_book (OrderBook): an instance of our OrderBook class in order_book.py
        matched_orders (list): A list used to store matched orders
        simulation_running (bool): A running flag for indicating if a simulation is running or not
        simulation_thread (threading.Thread): dedicated thread for simulation run"""

        self.root = root
        self.root.title("Order book")
        self.root.geometry("1200x600")
        self.order_book = OrderBook()
        self.matched_orders = []
        self.simulation_running = False
        self.simulation_thread = None
        self.create_widgets()

    def create_widgets(self):
        """ A method for creating the widgets of our main window application: Treeview widgets for displaying bids and asks,
        input fields for determining simulation parameters, buttons for starting/stopping the simulation and showing a matched orders log window."""
        # Create a frame to hold the two Treeview widgets
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for bids
        self.bids_tree = ttk.Treeview(self.frame, columns=("Qty", "Price"), show="headings", height=15)
        self.bids_tree.heading("Price", text="Price")
        self.bids_tree.heading("Qty", text="Qty")
        self.bids_tree.column("Price", width=100, anchor="center")
        self.bids_tree.column("Qty", width=100, anchor="center")
        self.bids_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Treeview for asks
        self.asks_tree = ttk.Treeview(self.frame, columns=("Price", "Qty"), show="headings", height=15)
        self.asks_tree.heading("Price", text="Price")
        self.asks_tree.heading("Qty", text="Qty")
        self.asks_tree.column("Price", width=100, anchor="center")
        self.asks_tree.column("Qty", width=100, anchor="center")
        self.asks_tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Control buttons for simulation
        self.start_button = ttk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = ttk.Button(self.root, text="Stop Simulation", command=self.stop_simulation)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Input fields for simulation parameters
        self.create_input_fields()

        # Button to show matched orders log
        self.log_button = ttk.Button(self.root, text="Show Matched Orders Log", command=self.show_log_window)
        self.log_button.pack(side=tk.BOTTOM, pady=10)

    def create_input_fields(self):
        """Method for creating the input fields which are user-input generated simulation parameters.
        The parameters are:
                        duration: Time duration of the simulation
                        rate: Rate parameter of the exponential distribution, used for generating time between orders. Can be any number above 0.
                        mean_price: The mean price of an order; price follows a normal distribution.
                        std_dev: The standard deviation of price; as price follows a normal dist. it must have a specified mean and standard deviation.
                        quantity_range: The quantityt range of units any order can take on; any order can generate an order for units in the span (a,b) for two integers a,b."""

        # Frame for input fields
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Duration input
        ttk.Label(self.input_frame, text="Duration:").pack(side=tk.LEFT)
        self.duration_entry = ttk.Entry(self.input_frame)
        self.duration_entry.pack(side=tk.LEFT, padx=5)

        # Rate input
        ttk.Label(self.input_frame, text="Rate:").pack(side=tk.LEFT)
        self.rate_entry = ttk.Entry(self.input_frame)
        self.rate_entry.pack(side=tk.LEFT, padx=5)

        # Mean Price input
        ttk.Label(self.input_frame, text="Mean Price:").pack(side=tk.LEFT)
        self.mean_price_entry = ttk.Entry(self.input_frame)
        self.mean_price_entry.pack(side=tk.LEFT, padx=5)

        # Std Dev input
        ttk.Label(self.input_frame, text="Std Dev:").pack(side=tk.LEFT)
        self.std_dev_entry = ttk.Entry(self.input_frame)
        self.std_dev_entry.pack(side=tk.LEFT, padx=5)

        # Quantity Range input
        ttk.Label(self.input_frame, text="Quantity Range (min,max):").pack(side=tk.LEFT)
        self.quantity_range_entry = ttk.Entry(self.input_frame)
        self.quantity_range_entry.pack(side=tk.LEFT, padx=5)

    def show_log_window(self):
        """ Application window for displaying log of matched orders. Shows order IDs for bids/asks, traded price, quantity and the time of the trade."""

        self.log_window = tk.Toplevel(self.root)
        self.log_window.title("Matched Orders Log")
        self.log_window.geometry("600x400")

        columns = ("Order IDs", "Price", "Traded Quantity", "Timestamp")

        self.log_tree = ttk.Treeview(self.log_window, columns=columns, show="headings")
        self.log_tree.heading("Order IDs", text="Order IDs")
        self.log_tree.heading("Price", text="Price")
        self.log_tree.heading("Traded Quantity", text="Traded Quantity")
        self.log_tree.heading("Timestamp", text="Timestamp")

        self.log_tree.column("Order IDs", width=200, anchor='center')
        self.log_tree.column("Price", width=100, anchor='center')
        self.log_tree.column("Traded Quantity", width=100, anchor='center')
        self.log_tree.column("Timestamp", width=150, anchor='center')

        self.log_tree.pack(fill=tk.BOTH, expand=True)


        for match in self.matched_orders:
            if isinstance(match, tuple) and len(match) == 4:
                order_ids_str, price, quantity, match_time = match
                bid_id, ask_id = order_ids_str.split(", ")
            else:
                continue

            order_ids = f"Bid ID: {bid_id}, Ask ID: {ask_id}"
            self.log_tree.insert("", "end", values=(order_ids, price, quantity, match_time))


    def start_simulation(self):
        """Starts a new simulation of the order book.
        Previous results and current states are reset, and retrieves inputs from users to run the simulation
        in a new thread.

        Raises a ValueError if invalid user inputs."""

        print("Simulation started")

        self.order_book = OrderBook()       # we reset the orderbooks state
        self.matched_orders = []            # and reset previous matches

        for i in self.bids_tree.get_children():         # we clear the entries of our bid and ask trees.
            self.bids_tree.delete(i)
        for i in self.asks_tree.get_children():
            self.asks_tree.delete(i)

        # retrieve and convert user inputs which will be the parameters for our simulation
        try:
            duration = float(self.duration_entry.get())
            rate = float(self.rate_entry.get())
            mean_price = float(self.mean_price_entry.get())
            std_dev = float(self.std_dev_entry.get())
            quantity_range = tuple(map(int, self.quantity_range_entry.get().split(',')))

            # flag that simulation is running, start simulation threading with user input variables
            self.simulation_running = True
            self.simulation_thread = threading.Thread(target = self.run_simulation, args = (duration, rate, mean_price, std_dev, quantity_range))
            self.simulation_thread.start()

        except ValueError as e:
            print(f'invalid input: {e}')



    def stop_simulation(self):
        """Stops the simulation by changing the simulation flag; waits for simulation thread to finish."""
        # signal to stop simulation
        self.simulation_running = False
        self.check_thread_finish() # let thread finish
        print("Stop simulation button pressed")

    def check_thread_finish(self):
        """Method for checking if a thread has finished. Checks if thread is alive, and resets it upon finishing"""
        if self.simulation_thread and self.simulation_thread.is_alive():
            self.root.after(10, self.check_thread_finish)
        else:
            self.simulation_thread = None

    def run_simulation(self, duration, rate, mean_price, std_dev, quantity_range):
        """Method for order arrival simulation. Works by generating orders, adding them to the orderbook
        and matching. Also updates the GUI for a dynamic experience.

        Order arrival is approximated as a Poisson distribution, hence why time between order arrivals follows the exponential distribution.
        Parameter related to order arrival is thus 'rate'.

        Prices are approximated with a normal distribution, thus have an associated 'mean' and 'standard deviation'.

        Args:
            duration (float): Time duration of simulation in seconds
            rate (float): Rate of order arrival
            mean_price (float): Mean price of orders
            std_dev (float): Standard deviation of order price
            quantity_range (tuple): Allow range of order quantities following (min, max)"""

        end_time = time.time() + duration
        while self.simulation_running and time.time() < end_time:
            time_to_next_order  = np.random.exponential(1 / rate)
            time.sleep(time_to_next_order)

            order = generate_order(mean_price, std_dev, quantity_range)
            print(order)
            self.order_book.add_order(order)
            matches = self.order_book.match_order()
            self.matched_orders.extend(matches)

            self.root.after(100, self.update_gui)


    def update_gui(self):
        """Method for updating the GUI. Clears and repopulates the bid, ask trees. If the simulation is running the GUI gets updated periodically."""
        # clear bid and ask trees
        for i in self.bids_tree.get_children():
            self.bids_tree.delete(i)
        for i in self.asks_tree.get_children():
            self.asks_tree.delete(i)

        # sort according to price
        sorted_bids = sorted(self.order_book.bids, key = lambda x: x[0])
        sorted_asks = sorted(self.order_book.asks, key = lambda x: x[0])

        # inserting bids and asks into their respective trees
        for price, timestamp, order in sorted_bids:
            self.bids_tree.insert("", "end", values = (order.quantity, -price))
        for price, timestamp, order in sorted_asks:
            self.asks_tree.insert("", "end", values = (price, order.quantity))

        # schedule GUI update
        if self.simulation_running:
            self.root.after(100, self.update_gui)


if __name__ == '__main__':
    root = tk.Tk()
    app = OrderBookGUI(root)
    root.mainloop()
