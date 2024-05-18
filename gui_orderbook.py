import tkinter as tk
from tkinter import ttk
from order_book import OrderBook, Order, generate_order
import threading
import time
import numpy as np


class OrderBookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Order book")
        self.root.geometry("1200x900")
        self.order_book = OrderBook()
        self.matched_orders = []
        self.simulation_running = False
        self.simulation_thread = None

        self.create_widgets()

    def create_widgets(self):
        # Create a frame to hold the two Treeview widgets
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for BIDS
        self.bids_tree = ttk.Treeview(self.frame, columns=("Qty", "Price"), show="headings", height=15)
        self.bids_tree.heading("Price", text="Price")
        self.bids_tree.heading("Qty", text="Qty")
        self.bids_tree.column("Price", width=100, anchor="center")
        self.bids_tree.column("Qty", width=100, anchor="center")
        self.bids_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Treeview for ASKS
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

        print("Matched Orders:", self.matched_orders)  # Debug print

        for match in self.matched_orders:
            print("Processing match:", match)
            if isinstance(match, tuple) and len(match) == 4:
                order_ids_str, price, quantity, match_time = match
                bid_id, ask_id = order_ids_str.split(", ")
            else:
                continue

            order_ids = f"Bid ID: {bid_id}, Ask ID: {ask_id}"
            self.log_tree.insert("", "end", values=(order_ids, price, quantity, match_time))


    def start_simulation(self):
        pass

    def stop_simulation(self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    app = OrderBookGUI(root)
    root.mainloop()
