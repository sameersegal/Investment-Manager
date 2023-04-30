# Investment Manager

Using GPT4 to democratize invesmtent management. 

## Problem Statement
A strong independent investor needs a way to brainstorm and validate investment ideas. If the investor could chat with the knowledge of their trusted analysts and feeds, they could validate their ideas and make better investment decisions. The decision needs to be personalized to the investor's risk profile and investment horizon.

## Solution
Index the investor's trusted analysts and feeds. Provide a database of transaction records and market data. Allow the investor user to chat with the system to brainstorm and validate investment ideas. The system will use GPT4 to generate responses. The system will use the investor's transaction records and market data to personalize the responses. Generate visualizations and conduct scenario analysis to augement the responses.

## Inspiration
My father-in-law is an avid reader and investor in public stocks. We aren't able to find the right advisory firm that can keep up with him. We have tried various firms and analysts but they all seem to be behind the curve.

I am finding it hard to keep up with his reading and his nuanced questions. I thought, if only there was an app for that?!

## Goals
- [ ] Build the basic api & db structure for GPT4 chatbot
- [ ] Scrape the web for trusted data sources
- [ ] Index the fetched pages into Milvus
- [ ] Add a frontend to the chatbot
- [ ] Provide portfolio transaction data and market data
- [ ] Provide visualizations using generated Python code
- [ ] Provide scenario analysis using generated Python code