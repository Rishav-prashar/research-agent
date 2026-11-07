from rich import print
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY "))

# ************* building custom tools"""""""""""


@tool
def web_search(query: str) -> str:
    """search the web for recent and reliable information on a topic . return titles,URLs and snippets"""
    results = tavily.search(query=query, max_results=5)
    out = []
    for r in results["results"]:
        out.append(
            f"""title: {r["title"]}, URL: {r["url"]}, answer: {r["content"]}""")

    return out


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={
                            "User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
