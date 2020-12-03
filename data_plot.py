import cbpro

public_client = cbpro.PublicClient()

def twent_four_hr_info(coin):
    daily_stats = public_client.get_product_24hr_stats(coin)
    return daily_stats

def order_book_info(coin):
    order_book = public_client.get_product_order_book(coin, level=1)
    return order_book

def ticker_info(coin):
    ticker = public_client.get_product_ticker(product_id=coin)
    return ticker

def get_historic_info(coin, from_date, to_date, gran):
    history = public_client.get_product_historic_rates(coin, from_date, to_date, granularity=gran)
    return history