from yahoo_fin import stock_info

def price(ticker):
    return stock_info.get_live_price(ticker)

if __name__ == "__main__":
    print(price("AMZN"))