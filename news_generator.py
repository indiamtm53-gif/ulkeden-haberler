from datetime import datetime
import feedparser
import json
import os
import re
import html
from datetime import datetime

SITE_URL = "https://indiamtm53-gif.github.io/ulkeden-haberler"

RSS_KAYNAKLARI = [
    "https://www.trthaber.com/manset_articles.rss",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml"
]

def kategori_belirle(baslik):

    baslik = baslik.lower()

    ekonomi = [
        "economy",
        "business",
        "market",
        "bank",
        "money",
        "inflation",
        "stock"
    ]

    teknoloji = [
        "technology",
        "tech",
        "software",
        "google",
        "apple",
        "microsoft",
        "ai"
    ]

    for kelime in ekonomi:
        if kelime in baslik:
            return "ekonomi"

    for kelime in teknoloji:
        if kelime in baslik:
            return "teknoloji"

    return "gundem"


def kaynak_adi(rss):

    if "trthaber" in rss:
        return "TRT Haber"

    if "technology" in rss:
        return "BBC Technology"

    if "business" in rss:
        return "BBC Business"

    return "BBC World"

def slug_olustur(baslik):
    baslik = baslik.lower()
    baslik = baslik.replace("ı", "i").replace("ğ", "g").replace("ü", "u")
    baslik = baslik.replace("ş", "s").replace("ö", "o").replace("ç", "c")
    baslik = re.sub(r"[^a-z0-9\s-]", "", baslik)
    baslik = re.sub(r"\s+", "-", baslik).strip("-")
    return "auto-" + baslik[:60]

def temizle():
    for dosya in os.listdir("."):
        if dosya.startswith("auto-") and dosya.endswith(".html"):
            os.remove(dosya)

    for i in range(1, 21):
        dosya = f"haber-{i}.html"
        if os.path.exists(dosya):
            os.remove(dosya)

def haberleri_cek():
def haberleri_cek():
    tum_haberler = []

    for rss in RSS_KAYNAKLARI:
        feed = feedparser.parse(rss)

        for haber in feed.entries[:5]:
            baslik = getattr(haber, "title", "").strip()
            link = getattr(haber, "link", "").strip()

            summary = getattr(haber, "summary", "").strip()

            # HTML etiketlerini temizle
            ozet = re.sub(r"<[^>]+>", "", summary)

            # Gerçek görseli almaya çalış
            gorsel = "https://picsum.photos/1000/500?random"

            eslesme = re.search(
                r'<img[^>]+src="([^"]+)"',
                summary,
                re.IGNORECASE
            )

            if eslesme:
                gorsel = eslesme.group(1)

            if baslik and link:
                tum_haberler.append({
                    "baslik": baslik,
                    "link": link,
                    "ozet": ozet,
                    "kategori": kategori_belirle(baslik),
                    "dosya": slug_olustur(baslik) + ".html",
                    "kaynak": kaynak_adi(rss),
                    "tarih": datetime.now().strftime("%d.%m.%Y"),
                    "gorsel": gorsel
                })

    return tum_haberler[:10]

def haber_sayfasi_olustur(haber):
    baslik = html.escape(haber["baslik"])
    ozet = html.escape(haber["ozet"])
    kategori = html.escape(haber["kategori"].upper())
    link = html.escape(haber["link"])

    sayfa = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{baslik} - Ülkeden Haberler</title>
<meta name="description" content="{baslik}">
<link rel="icon" href="favicon.png">

<style>
*{{
margin:0;
padding:0;
box-sizing:border-box;
font-family:Arial,sans-serif;
}}

body{{
background:#f4f6f9;
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
padding:30px;
border-radius:15px;
box-shadow:0 4px 10px rgba(0,0,0,.08);
}}

h1{{
font-size:32px;
margin-bottom:20px;
}}

.meta{{
color:#64748B;
margin-bottom:20px;
font-size:15px;
line-height:1.8;
}}

p{{
line-height:1.8;
font-size:18px;
margin-bottom:18px;
}}

.back-btn{{
display:inline-block;
margin-top:25px;
padding:12px 20px;
background:#2563EB;
color:white;
text-decoration:none;
border-radius:10px;
font-weight:bold;
}}

.source-link{{
color:#2563EB;
font-weight:bold;
}}
</style>
</head>

<body>

<header>
<h2>📰 Ülkeden Haberler</h2>
</header>

<div class="container">

<h1>{baslik}</h1>
<img src="{haber['gorsel']}" alt="{baslik}"
<div class="meta">
📂 {kategori}
<br>
📅 {datetime.now().strftime("%d.%m.%Y")}
<br>
🤖 Ülkeden Haberler Otomasyon Sistemi
</div> 
<br>
📰 Kaynak: {haber['kaynak']}
<p>{ozet}</p>

<p>
Bu içerik RSS kaynağından alınan bilgiler kullanılarak otomatik sistem tarafından oluşturulmuştur.
</p>

<p>
Kaynak:
<a class="source-link" href="{link}">Orijinal Haberi Görüntüle</a>
</p>

<a href="otomatik-gundem.html" class="back-btn">← Otomatik Haberlere Dön</a>

</div>

</body>
</html>
"""

    with open(haber["dosya"], "w", encoding="utf-8") as f:
        f.write(sayfa)

def otomatik_liste_olustur(haberler):
    liste = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Otomatik Haberler - Ülkeden Haberler</title>
<link rel="icon" href="favicon.png">
</head>
<body>

<h1>Otomatik Haberler</h1>

<ul>
"""

    for haber in haberler:
        liste += f'<li><a href="{haber["dosya"]}">{html.escape(haber["baslik"])}</a></li>\n'

    liste += """
</ul>

<a href="index.html">Ana Sayfaya Dön</a>

</body>
</html>
"""

    with open("otomatik-gundem.html", "w", encoding="utf-8") as f:
        f.write(liste)

def kategori_sayfalari_olustur(haberler):
    kategoriler = {
        "gundem": [],
        "ekonomi": [],
        "teknoloji": []
    }

    for haber in haberler:
        kategoriler[haber["kategori"]].append(haber)

    for kategori, liste in kategoriler.items():
        sayfa = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{kategori.title()} Otomatik Haberleri - Ülkeden Haberler</title>
<link rel="icon" href="favicon.png">
</head>
<body>

<h1>{kategori.title()} Otomatik Haberleri</h1>

<ul>
"""

        for haber in liste:
            sayfa += f'<li><a href="{haber["dosya"]}">{html.escape(haber["baslik"])}</a></li>\n'

        sayfa += """
</ul>

<a href="otomatik-gundem.html">Ana Listeye Dön</a>

</body>
</html>
"""

        with open(f"{kategori}-otomatik.html", "w", encoding="utf-8") as f:
            f.write(sayfa)

def sitemap_olustur(haberler):
    sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

    for haber in haberler:
        sitemap += f"""
<url>
<loc>{SITE_URL}/{haber["dosya"]}</loc>
<priority>0.8</priority>
</url>
"""

    sitemap += """
</urlset>
"""

    with open("otomatik-sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)

def ana_sayfa_kutusu_olustur(haberler):
    kutu = """
<div class="auto-news-box">

<p>Toplam Otomatik Haber: 10</p>

<h2>🤖 Son Otomatik Haberler</h2>

<ul>
"""

    for haber in haberler:
        kutu += f'<li><a href="{haber["dosya"]}">{html.escape(haber["baslik"])}</a></li>\n'

    kutu += """
</ul>

</div>
"""

    with open("ana-sayfa-haberleri.html", "w", encoding="utf-8") as f:
        f.write(kutu)

def json_olustur(haberler):
    with open("otomatik-haberler.json", "w", encoding="utf-8") as f:
        json.dump(haberler, f, ensure_ascii=False, indent=4)

def log_yaz():
    with open("otomasyon-log.txt", "a", encoding="utf-8") as f:
        f.write(f"Sistem çalıştı: {datetime.now()}\n")

def main():
    print("Ülkeden Haberler otomasyon sistemi başladı.")

    temizle()

    haberler = haberleri_cek()

    if not haberler:
        print("Haber bulunamadı.")
        return

    json_olustur(haberler)

    for haber in haberler:
        haber_sayfasi_olustur(haber)

    otomatik_liste_olustur(haberler)
    kategori_sayfalari_olustur(haberler)
    sitemap_olustur(haberler)
    ana_sayfa_kutusu_olustur(haberler)
    log_yaz()

    print("Otomatik haber sistemi başarıyla tamamlandı.")

if __name__ == "__main__":
    main()
