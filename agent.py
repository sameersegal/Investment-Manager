# This code is heavily borrowed from: https://til.simonwillison.net/llms/python-react-pattern
import argparse
import os
import sys
import openai
import re
import httpx
from dotenv import load_dotenv
from tools import (
    search,
    transaction_history,
    ratios,
    price,
    critic
)
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


action_re = re.compile('^Action: (\w+): (.*)$')


def query(prompt: str, question: str, max_turns=5, **kwargs):
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


def wikipedia(q: str, **kwargs):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]


def calculate(what: str, **kwargs):
    return eval(what)


known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "knowledgebase": search,
    "transactions": transaction_history,
    "price": price,
    "ratios": ratios,
    "critic": critic
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent script")

    # Add the arguments
    parser.add_argument('--debug',
                        action="store_true",
                        help='an optional debug flag', required=False)

    parser.add_argument('--question',
                        type=str,
                        help='user question', required=True)

    parser.add_argument('--prompt',
                        type=int,
                        help='prompt to use 1,2,3', required=True)

    # Parse the arguments
    args = parser.parse_args()

    kwargs = {}
    kwargs['debug'] = args.debug
    question = args.question
    promptid = args.prompt

    if promptid > 3 or promptid < 1:
        raise Exception("Prompt id must be 1,2,3")

    prompt = ""
    with open(f"prompts/prompt{promptid}.txt", "r") as f:
        prompt = "\n".join(f.readlines()).strip()

    query(prompt, question, **kwargs)
