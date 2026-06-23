import feedparser
import json

rss_url = "https://feeds.bbci.co.uk/news/world/rss.xml"

feed = feedparser.parse(rss_url)

haberler = []
def kategori_belirle(baslik):

    baslik = baslik.lower()

    ekonomi = [
        "economy",
        "market",
        "bank",
        "money",
        "inflation",
        "stock"
    ]

    teknoloji = [
        "ai",
        "technology",
        "tech",
        "software",
        "google",
        "apple",
        "microsoft"
    ]

    for kelime in ekonomi:
        if kelime in baslik:
            return "ekonomi"

    for kelime in teknoloji:
        if kelime in baslik:
            return "teknoloji"

    return "gundem"
for haber in feed.entries[:5]:
    haberler.append({
    "baslik": haber.title,
    "link": haber.link,
    "kategori": kategori_belirle(haber.title)
})

with open("otomatik-haberler.json", "w", encoding="utf-8") as f:
    json.dump(haberler, f, ensure_ascii=False, indent=4)

print("5 haber kaydedildi.")
for i, haber in enumerate(haberler, start=1):

    html = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{haber['baslik']} - Ülkeden Haberler</title>

<meta name="description" content="{haber['baslik']}">

<style>

body{{
font-family:Arial,sans-serif;
background:#f4f6f9;
margin:0;
color:#0F172A;
}}

header{{
background:#0F172A;
color:white;
padding:20px;
text-align:center;
}}

.container{{
width:90%;
max-width:900px;
margin:30px auto;
background:white;
padding:25px;
border-radius:15px;
box-shadow:0 4px 10px rgba(0,0,0,.08);
}}

h1{{
margin-bottom:20px;
}}

.meta{{
color:#64748B;
margin-bottom:20px;
}}

.back-btn{{
display:inline-block;
margin-top:25px;
padding:12px 20px;
background:#2563EB;
color:white;
text-decoration:none;
border-radius:10px;
}}

</style>

</head>

<body>

<header>
<h2>📰 Ülkeden Haberler</h2>
</header>

<div class="container">

<h1>{haber['baslik']}</h1>

<div class="meta">
📂 {haber['kategori'].upper()} |
🤖 Otomatik Haber Sistemi
</div>

<p>
Bu haber RSS kaynaklarından alınan bilgiler kullanılarak otomatik sistem tarafından oluşturulmuştur.
</p>

<p>
Kaynak bağlantısı:
</p>

<p>
<a href="{haber['link']}">
Orijinal Haberi Görüntüle
</a>
</p>

<a href="otomatik-gundem.html" class="back-btn">
← Otomatik Haberlere Dön
</a>

</div>

</body>
</html>
"""

    with open(
        f"haber-{i}.html",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)

    ilk_haber = haberler[0]

    html = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>{ilk_haber['baslik']}</title>
<meta name="description" content="{ilk_haber['baslik']}">
</head>
<body>

<h1>{ilk_haber['baslik']}</h1>

<p>
Bu haber otomatik sistem tarafından oluşturulmuştur.
</p>

<p>
Kaynak:
<a href="{ilk_haber['link']}">
Habere Git
</a>
</p>

</body>
</html>
"""

    with open(
        "otomatik-haber.html",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)
liste_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Otomatik Haberler</title>
</head>
<body>

<h1>Otomatik Haberler</h1>

<ul>
"""

for i, haber in enumerate(haberler, start=1):
    liste_html += f'''
<li>
<a href="haber-{i}.html">
{haber["baslik"]}
</a>
</li>
'''

liste_html += """
</ul>

</body>
</html>
"""

with open(
    "otomatik-gundem.html",
    "w",
    encoding="utf-8"
) as f:
    f.write(liste_html)
with open("otomatik-sitemap.txt", "w", encoding="utf-8") as f:

    for i in range(1, 6):

        f.write(
            f"https://indiamtm53-gif.github.io/ulkeden-haberler/haber-{i}.html\n"
        )
sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

for i in range(1, 6):

    sitemap += f"""
<url>
<loc>https://indiamtm53-gif.github.io/ulkeden-haberler/haber-{i}.html</loc>
<priority>0.8</priority>
</url>
"""

sitemap += """
</urlset>
"""

with open(
    "otomatik-sitemap.xml",
    "w",
    encoding="utf-8"
) as f:
    f.write(sitemap)
