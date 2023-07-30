# This code is heavily borrowed from: https://til.simonwillison.net/llms/python-react-pattern
import argparse
import os
import sys
import openai
import re
import httpx
from dotenv import load_dotenv
from kb import search
from portfolio import transaction_history
from price import price
load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]


class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613", messages=self.messages)
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        # print(completion.usage)
        return completion.choices[0].message.content


prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

wikipedia:
e.g. wikipedia: Django
Returns a summary from searching Wikipedia

knowledgebase:
e.g. kb: TSLA Q3 performance
Search Stock Knowledgebase 

transactions:
e.g. transactions: Get TSLA purchases in the last quarter
Returns transaction history of the user

price:
e.g. price: Stock Code
Returns the current price

Always look things up on Stock Knowledgebase if you have the opportunity to do so.

Example session:

Question: What is the capital of France?
Thought: I should look up France on Wikipedia
Action: wikipedia: France
PAUSE

You will be called again with this:

Observation: France is a country. The capital is Paris.

You then output:

Answer: The capital of France is Paris
""".strip()


action_re = re.compile('^Action: (\w+): (.*)$')


def query(question, max_turns=5, **kwargs):
    i = 0
    bot = ChatBot(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        actions = [action_re.match(a) for a in result.split(
            '\n') if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception(
                    "Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input, **kwargs)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            return


def wikipedia(q):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]


def calculate(what):
    return eval(what)


known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "knowledgebase": search,
    "transactions": transaction_history,
    "price": price
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent script")

    # Add the arguments
    parser.add_argument('--debug',
                        help='an optional debug flag', required=False)

    parser.add_argument('--question',
                        type=str,
                        help='an optional question', required=True)

    # Parse the arguments
    args = parser.parse_args()

    kwargs = {}
    kwargs['debug'] = args.debug
    question = args.question

    query(question, **kwargs)
