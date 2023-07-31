# Investment Manager

Using GPT4 to democratize invesmtent management. 

## Problem Statement
A strong independent investor needs a way to brainstorm and validate investment ideas. If the investor could chat with the knowledge of their trusted analysts and feeds, they could validate their ideas and make better investment decisions. The decision needs to be personalized to the investor's risk profile and investment horizon.

## Solution
Index the investor's trusted analysts and feeds. Provide a database of transaction records and market data. Allow the investor user to chat with the system to brainstorm and validate investment ideas. The system will use GPT4 to generate responses. The system will use the investor's transaction records and market data to personalize the responses. Generate visualizations and conduct scenario analysis to augement the responses.

## Inspiration
My father-in-law is an avid reader and investor in public stocks. We aren't able to find the right advisory firm that can keep up with him. We have tried various firms and analysts but they all seem to be behind the curve.

I am finding it hard to keep up with his reading and his nuanced questions. I thought, if only there was an app for that?!

## Developer Setup

1. Install python3.10 and poetry - [https://python-poetry.org/docs/](https://python-poetry.org/docs/)
2. Run Milvus (Vector Database) in standalone mode - [https://milvus.io/docs/install_standalone-docker.md](https://milvus.io/docs/install_standalone-docker.md)
3. Insert data into Milvus. Take inspiration from my other project [https://github.com/sameersegal/investment-data](https://github.com/sameersegal/investment-data)
4. Run the following bash commands
```
$poetry shell
$poetry install
$poetry run python3 agent.py --prompt 1 --question "What are the highlights of Tesla's latest quarter earnings?" --debug
```
Look at [Demo.md](Demo.md) for more examples

## Goals
- [ ] Build the basic api & db structure for GPT4 chatbot
- [X] Scrape the web for trusted data sources
- [X] Index the fetched pages into Milvus
- [ ] Add a frontend to the chatbot
- [X] Provide portfolio transaction data and market data
- [ ] Provide visualizations using generated Python code
- [ ] Provide scenario analysis using generated Python code
