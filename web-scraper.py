#!/usr/bin/env python3
"""
Web Scraper - Fixed & Pydroid Friendly Version
==============================================
Ethical news headline scraper with improved error handling.
"""

import requests
from bs4 import BeautifulSoup
import argparse
import time
import csv
import json
from pathlib import Path
from urllib.parse import urljoin


def scrape_headlines(url: str, delay: float = 2.0):
    """Scrape headlines with better error handling."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"🌐 Fetching: {url}")
    print("⏳ Please wait...")

    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"📡 Status Code: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ Failed: Server returned status {response.status_code}")
            print("💡 Try a different website or check your internet connection.")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        seen = set()

        # More flexible headline detection
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'article', 'a']):
            title = tag.get_text(strip=True)
            if not title or len(title) < 10:
                continue
                
            link = tag.get('href')
            if link:
                if not link.startswith(('http', '/')):
                    continue
                if not link.startswith('http'):
                    link = urljoin(url, link)
                
                if title not in seen:
                    seen.add(title)
                    articles.append({"title": title, "link": link})

        time.sleep(delay)
        return articles[:25]  # Limit results

    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
        print("💡 Check your internet connection or try again later.")
        return []
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return []


def save_results(articles, filename="headlines.csv", format="csv"):
    if not articles:
        print("⚠️ No articles found to save.")
        return

    try:
        filepath = Path(filename)
        if format == "json":
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)
        else:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["title", "link"])
                writer.writeheader()
                writer.writerows(articles)
        
        print(f"✅ Success! Saved {len(articles)} headlines to {filepath}")
    except Exception as e:
        print(f"❌ Failed to save file: {e}")


def main():
    parser = argparse.ArgumentParser(description="🌐 Web Scraper (Fixed Version)")
    parser.add_argument("url", nargs="?", default="https://news.ycombinator.com",
                        help="Website URL (default: Hacker News)")
    parser.add_argument("-o", "--output", default="headlines.csv",
                        help="Output filename")
    parser.add_argument("-f", "--format", choices=["csv", "json"], default="csv")
    parser.add_argument("-d", "--delay", type=float, default=2.0)

    args = parser.parse_args()

    print("🔍 Starting Web Scraper...\n")
    
    articles = scrape_headlines(args.url, args.delay)
    
    if articles:
        print(f"\n✅ Found {len(articles)} headlines!\n")
        for i, article in enumerate(articles[:8], 1):
            print(f"{i:2d}. {article['title'][:90]}...")
        save_results(articles, args.output, args.format)
    else:
        print("\n⚠️ Could not extract headlines.")
        print("Try these sites:")
        print("   • https://news.ycombinator.com")
        print("   • https://www.bbc.com/news")


if __name__ == "__main__":
    main()
