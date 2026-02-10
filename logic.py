import os
import feedparser
import requests
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
import streamlit as st

# --- 1. SETUP THE BRAIN ---
def get_gemini_llm(api_key):
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        verbose=True,
        temperature=0.1, # Low temperature = factual, not creative
        google_api_key=api_key
    )

# --- 2. THE TOOLS (The Eyes & Ears) ---

@tool("RSS Speed Scraper")
def scrape_rss_feeds(dummy_input: str):
    """
    Instantly pulls the latest headlines from high-speed financial RSS feeds.
    Targeting: Investing.com, CNBC, Reuters.
    """
    feeds = [
        "https://www.investing.com/rss/news.rss",
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664",
        "http://feeds.reuters.com/reuters/businessNews"
    ]
    
    news_dump = []
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]: # Top 3 from each to keep it fast
                news_dump.append(f"SOURCE: RSS | TITLE: {entry.title} | LINK: {entry.link}")
        except:
            continue
    return "\n".join(news_dump)

@tool("Social Sentiment Dragnet")
def search_social_media(query: str):
    """
    Searches Reddit and X (Twitter) for specific keywords using search operators.
    Useful for finding rumors and retail sentiment.
    """
    search = DuckDuckGoSearchRun()
    # We force the search to look at specific sites for the last 24h
    social_query = f"{query} site:reddit.com OR site:twitter.com OR site:threads.net"
    return search.run(social_query)

# --- 3. THE AGENTS (The Team) ---

def create_crew(api_key):
    llm = get_gemini_llm(api_key)

    # Agent 1: The Hunter (Finds the data)
    scanner = Agent(
        role='Financial Intelligence Officer',
        goal='Gather raw news from RSS feeds and Social Media immediately.',
        backstory='You are a high-frequency news scanner. Speed is your god.',
        tools=[scrape_rss_feeds, search_social_media],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    # Agent 2: The Analyst (Filters & Decides)
    analyst = Agent(
        role='Senior Market Strategist',
        goal='Filter noise, identify the single most important trade, and provide a signal.',
        backstory='You are a veteran trader. You ignore fluff. You only care about market-moving events.',
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    # --- 4. THE TASKS (The Mission) ---

    task_scan = Task(
        description='1. Run the "RSS Speed Scraper" to get official news. 2. Run the "Social Sentiment Dragnet" for "crypto" and "stock market". Compile the raw list.',
        expected_output='A raw text list of headlines from RSS and Social Media.',
        agent=scanner
    )

    task_analyze = Task(
        description="""
        Analyze the raw news.
        1. STRIP out duplicates and non-financial news.
        2. PICK the Top 3 stories with highest market impact.
        3. For the #1 Story, generate a TRADING SIGNAL.
        
        OUTPUT FORMAT:
        ## 🚨 MARKET ALERT
        **HEADLINE:** [The News]
        **IMPACT:** [High/Med/Low]
        **ASSET:** [e.g. BTC, TSLA, USD]
        **SIGNAL:** [BULLISH/BEARISH]
        **CONFIDENCE:** [0-100%]
        **REASONING:** [Why?]
        """,
        expected_output='A structured markdown report.',
        agent=analyst,
        context=[task_scan]
    )

    return Crew(
        agents=[scanner, analyst],
        tasks=[task_scan, task_analyze],
        process=Process.sequential,
        verbose=True
    )
