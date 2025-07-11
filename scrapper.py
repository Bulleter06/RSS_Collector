import requests
import xml.etree.ElementTree as ET
import pandas as pd


def fetch_rss_feed(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.content


def parse_rss(xml_data):
    root = ET.fromstring(xml_data)
    channel = root.find("channel")
    items = []
    for item in channel.findall("item"):
        title = item.findtext("title", default="")
        link = item.findtext("link", default="")
        pub_date = item.findtext("pubDate", default="")
        description = item.findtext("description", default="")
        items.append({
            "title": title.strip(),
            "link": link.strip(),
            "published": pub_date.strip(),
            "summary": description.strip()
        })
    return items


def save_to_csv(entries, filename):
    df = pd.DataFrame(entries)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Saved {len(entries)} entries to {filename}")


if __name__ == "__main__":
    RSS_URL = "http://feeds.bbci.co.uk/news/rss.xml"
    xml_data = fetch_rss_feed(RSS_URL)
    entries = parse_rss(xml_data)
    save_to_csv(entries, "bbc_news.csv")
