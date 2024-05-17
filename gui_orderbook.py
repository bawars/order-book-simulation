import tkinter as tk
from tkinter import ttk
from order_book import OrderBook, Order


class OrderBookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Order book")
        self.root.geometry("800x600")
        self.order_book = OrderBook()
        self.matched_orders = []  # Store matched orders here

        self.create_widgets()

        # Add some orders for testing
        self.add_test_orders()

        # Match orders and store the results
        self.matched_orders = self.order_book.match_order()


    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.bids_tree = ttk.Treeview(self.frame, columns=("Qty", "Price"), show="headings", height=15)
        self.bids_tree.heading("Price", text="Price")
        self.bids_tree.heading("Qty", text="Qty")
        self.bids_tree.column("Price", width=100, anchor="center")
        self.bids_tree.column("Qty", width=100, anchor="center")

        self.bids_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.asks_tree = ttk.Treeview(self.frame, columns=("Price", "Qty"), show="headings", height=15)
        self.asks_tree.heading("Price", text="Price")
        self.asks_tree.heading("Qty", text="Qty")
        self.asks_tree.column("Price", width=100, anchor="center")
        self.asks_tree.column("Qty", width=100, anchor="center")

        self.asks_tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.log_button = ttk.Button(self.root, text="Show Matched Orders Log", command=self.show_log_window)
        self.log_button.pack(side=tk.BOTTOM, pady=10)

    def show_log_window(self):
        self.log_window = tk.Toplevel(self.root)
        self.log_window.title("Matched Orders Log")
        self.log_window.geometry("600x400")

        columns = ("Order IDs", "Price", "Traded Quantity")

        self.log_tree = ttk.Treeview(self.log_window, columns=columns, show="headings")
        self.log_tree.heading("Order IDs", text="Order IDs")
        self.log_tree.heading("Price", text="Price")
        self.log_tree.heading("Traded Quantity", text="Traded Quantity")

        self.log_tree.column("Order IDs", width=200, anchor='center')
        self.log_tree.column("Price", width=100, anchor='center')
        self.log_tree.column("Traded Quantity", width=100, anchor='center')

        self.log_tree.pack(fill=tk.BOTH, expand=True)

        # we populate the log with matched orders
        for match in self.matched_orders:
            self.log_tree.insert("", "end", values=match)

    def add_test_orders(self):
        self.order_book.add_order(Order('buy', 100, 10))
        self.order_book.add_order(Order('sell', 100, 5))
        self.order_book.add_order(Order('sell', 100, 5))
        self.order_book.add_order(Order('buy', 90, 10))


if __name__ == '__main__':
    root = tk.Tk()
    app = OrderBookGUI(root)
    root.mainloop()
