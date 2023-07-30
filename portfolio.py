import pandas as pd
import numpy as np
import openai
from datetime import datetime
import tabulate


def transaction_history(query: str, **kwargs):

    debug = kwargs.get("debug", False)

    df = pd.read_csv('stock_transactions.csv')
    df['Date'] = pd.to_datetime(df['Date'])

    current_date = datetime.now()

    df_head = df.head(3)

    messages = [
        {"role": "system", "content": f"""Assume you have a dataframe df of the users stock transaction history. Generate python code based on the user instruction. Do not geneate anything other than code. 
         
        df.head()
        {df_head}
         
        Current Time is {current_date}.
        If filtering by dates, define both start date and end date conditions.
        Ensure data types are set correctly before filtering.
        The last line of the code should set the result to 'df_result' dataframe.
        Do not import any packages."""},
        {"role": "user", "content": query},
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613", messages=messages)

    code = completion.choices[0].message.content
    # print(code)

    if debug:
        print(f"\033[1;32;40m{code}\n\033[0m")

    df_result = pd.DataFrame()
    result = ""
    try:
        exec(code)
        result = df_result.to_markdown()
    except Exception as e:
        print("An error occurred while executing the code:", e)

    if debug:
        print(f"\033[1;34;40m{result}\n\034[0m")

    return result


if __name__ == "__main__":
    portfolio("Get transactions in the last quarter.")
