import feedparser
import json

rss_url = "https://feeds.bbci.co.uk/news/world/rss.xml"

feed = feedparser.parse(rss_url)

haberler = []

for haber in feed.entries[:5]:
    haberler.append({
        "baslik": haber.title,
        "link": haber.link
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
<title>{haber['baslik']}</title>
<meta name="description" content="{haber['baslik']}">
</head>
<body>

<h1>{haber['baslik']}</h1>

<p>
Bu haber otomatik sistem tarafından oluşturulmuştur.
</p>

<p>
Kaynak:
<a href="{haber['link']}">
Habere Git
</a>
</p>

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
