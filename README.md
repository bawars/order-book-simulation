# Order Book Simulation


> An order book is a list which keeps track of potential buyers and sellers of a financial instrument. By keeping track of buyers and sellers one can more easily match orders to one another and thereby execute trades. A buy order is called a 'Bid', and a sell order is called an 'Ask'. The order book is thereby usually split between a Bid and Ask side.
> 
> This program implements the logic of orders, an order book, a simulation to mimic market dynamics, along with a GUI for the end user. In the GUI the user can specify the simulation's parameters and observe the order book in real-time.
> 
> NB! Other than Python's standard libraries, this program will require numpy.

## Features
- **Order Management**: Create and process buy and sell orders
- **Order Matching**: Orders wil be matched to one another according to first a price priority, secondly a time priority (FIFO)
- **GUI Interface**: An interface visualizing the marketplace dynamically as orders enter and exit the order book, and allows for stopping/starting.
  - Note that re-pressing the 'Start Simulation' button will start a *new* simulation. Thus there is no possibility of 'recommencing', only resetting the simulation.
- **Logging**: Allows to view matched orders in a window along with pertinent information for completed trades.


## Usage

1. **Getting started**:
   - Firstly, clone the repository.
   - Ensure you have Python installed.
   - Install the required package(s):
     - `pip install numpy`
   - To run the GUI:
     - `python gui_orderbook.py`
   

2. **Example usages**:

Add orders to an order book

    #We begin with an empty order book:
     order_book = OrderBook()
     
    # create orders and add them using the add_order method:
      buy_order = Order('side' = buy, price = 50, quantity = 5)
      sell_order = Order('side' = sell, price = 51, quantity = 4)

      order_book.add_order(buy_order)
      order_book.add_order(sell_order)

Knowing what constitutes 'top of book' is very important in the context of markets. These are the trades closest to matching and thereby executing.
To assess which orders are top of book, call the query method query_book().

    top_orders = order_book.query_book()

In our case, top of book would be the buy and sell order we had created, as no other orders exist and they are on opposite sides of the book.
To assess if any orders can be matched, we run the match_order() method:

      matches = order_book.match_order()

Now, if any orders had matched, they would be stored in the variable matches.

## Running Tests
To run the built-in tests and simulate the GUI, execute the `main.py` script:

    python main.py



## Simulation Parameters:

**Duration**: Time duration of the simulation in seconds.

**Rate**: Determines the rate at which orders will enter the market. It is the <br> rate parameter of the exponential distribution. I suggest  starting with a value <br> smaller than 10 then bumping it up if you so wish.

**Mean Price**: Mean price of incoming orders. Prices will follow a normal distribution. They will thus need a mean value [...and a standard deviation].

**Standard Deviation**: The standard deviation of price.

**Quantity Range**: Allowed range of quantities for orders (min, max). I.e., the number of units one may minimally or maximally order.

### GUI Controls:
   - **Start Simulation**: Begin the simulation with the specified parameters.

   - **Stop Simulation**: Stops the simulation.

   - **Show Matched Orders Log**: Display a separate window with all executed trades and relevant information.

   - **Quit**: Stop the simulation and close the application.

