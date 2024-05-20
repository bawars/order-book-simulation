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

1. **Running the Simulation**:
   - Clone the repository.
   - Ensure you have Python installed.
   - Run the `gui_orderbook.py` file to start the GUI. This will allow you to make your own simulation <br> with your own parameters of choice.


2. **Simulation Parameters**:
    - **Duration**: Time duration of the simulation in seconds.
   - **Rate**: Determines the rate at which orders will enter the market. It is the <br> rate parameter of the exponential distribution. I suggest  starting with a value <br> smaller than 10 then bumping it up if you so wish.
   - **Mean Price**: Mean price of incoming orders. 
     - Prices will follow a normal distribution. They will thus need a mean value [...and a standard deviation].
   - **Standard Deviation**: The standard deviation of price.
   - **Quantity Range**: Allowed range of quantities for orders (min, max). I.e., the number of units one may minimally or maximally order. 


3. **Controls**:
   - **Start Simulation**: Begin the simulation with the specified parameters.
   - **Stop Simulation**: Stops the simulation.
   - **Show Matched Orders Log**: Display a separate window with all executed trades and relevant information.
   - **Quit**: Stop the simulation and close the application.

