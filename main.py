from order_book import OrderBook, simulate_orders

def main():

    enbok = OrderBook()
    simulate_orders(enbok, duration=5, rate=3, mean_price=50, std_dev=2, quantity_range=(1, 20))



if __name__ == '__main__':
    main()