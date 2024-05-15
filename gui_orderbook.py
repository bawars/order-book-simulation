import tkinter as tk
from tkinter import ttk


class OrderBookGUI:
    def __init__(self, root):
        self.root = root            #initializes the main window
        self.root.title("Order book")       #window title
        self.root.geometry("800x600")       # window size

        self.create_widgets()

    def create_widgets(self):
        #we create a Treeview for the Order book display

        self.tree = ttk.Treeview(self.root, columns=("Price", "Qty", "Side"), show="headings")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Qty", text="Qty")
        self.tree.heading("Side", text="Side")
        self.tree.pack(fill=tk.BOTH, expand=True)



if __name__ == '__main__':
    root = tk.Tk()
    app = OrderBookGUI(root)
    root.mainloop()