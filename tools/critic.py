import openai
import json
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

def critic(decision: str, **kwargs):
    messages = [
        {"role": "system", "content": """You are an expert investor of the caliber of Warren Buffet.
         You are a long term buy and hold investor
         Always looking for great value points.

         Evaluate the advice that user has received. 
         Give your feedback as to whether the advice is good or bad.

         Response should be in a JSON format:
         {
             "result": "good" or "bad",
            "reasons": [
                "reason1",
                "reason2"
            ]
         }
         """},
        {"role": "user", "content": decision},
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613", messages=messages)

    result = completion.choices[0].message.content

    return json.loads(result)


if "__name__" == "__main__":
    result = critic("The price to earnings ratio of TSLA is 86.5065, indicating that the stock may be overpriced.")
    print(result)

