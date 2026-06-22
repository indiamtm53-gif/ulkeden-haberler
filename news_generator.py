import feedparser

rss_url = "https://feeds.bbci.co.uk/news/world/rss.xml"

feed = feedparser.parse(rss_url)

print("Toplam haber:", len(feed.entries))

for haber in feed.entries[:5]:
    print(haber.title)
