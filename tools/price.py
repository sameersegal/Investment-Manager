# from yahoo_fin import stock_info
# def price(ticker, **kwargs):
#     return stock_info.get_live_price(ticker)
import yfinance as yf
import openai


def price(ticker, **kwargs):
    info = yf.Ticker(ticker).info

    return info['currentPrice']


def ratios(query: str, **kwargs):

    messages = [
        {"role": "system", "content": f"""Get the stock code from the user's question. Provide no other information.
         """},
        {"role": "user", "content": query},
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613", messages=messages)

    ticker = completion.choices[0].message.content

    info = yf.Ticker(ticker).info

    messages = [
        {"role": "system", "content": f"""Given the following information, answer the user's question
         {info}
         """},
        {"role": "user", "content": query},
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613", messages=messages)

    result = completion.choices[0].message.content

    return result


if __name__ == "__main__":
    # print(price("AMZN"))

    print(ratios("What is the price to earnings ratio of AMZN?"))
