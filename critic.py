import openai
import json
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

def critic(decision: str):
    messages = [
        {"role": "system", "content": f"""You are an expert investor of the caliber of Warren Buffet.
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
    result = critic("Given that the stock price is low, I would buy Tesla.")
    print(result)

