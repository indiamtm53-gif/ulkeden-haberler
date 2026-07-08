from datetime import datetime
import feedparser
import json
import os
import re
import html
import urllib.request
import urllib.error

SITE_URL = "https://indiamtm53-gif.github.io"

RSS_KAYNAKLARI = [
    "https://www.trthaber.com/manset_articles.rss",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml"
]


def e(deger):
    return html.escape(str(deger or ""), quote=True)


def kategori_belirle(baslik):
    baslik = baslik.lower()

    ekonomi = [
        "economy", "business", "market", "bank", "money", "inflation", "stock",
        "ekonomi", "piyasa", "borsa", "faiz", "dolar", "euro", "altın"
    ]

    teknoloji = [
        "technology", "tech", "software", "google", "apple", "microsoft", "ai",
        "teknoloji", "yapay zeka", "siber", "internet", "uygulama"
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
    if not baslik:
        baslik = "haber"
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
    tum_haberler = []

    for rss in RSS_KAYNAKLARI:
        feed = feedparser.parse(rss)

        for haber in feed.entries[:5]:
            baslik = getattr(haber, "title", "").strip()
            link = getattr(haber, "link", "").strip()
            summary = getattr(haber, "summary", "").strip()

            ozet = re.sub(r"<[^>]+>", "", summary).strip()

            gorsel = "https://picsum.photos/1000/500?random"
            eslesme = re.search(r'<img[^>]+src="([^"]+)"', summary, re.IGNORECASE)
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


def ortak_css():
    return """
<style>
:root{
--bg:#f4f6f9;
--card:#ffffff;
--text:#0f172a;
--muted:#64748b;
--primary:#2563eb;
--primary2:#1d4ed8;
--danger:#dc2626;
--green:#10b981;
--orange:#f59e0b;
--border:#e2e8f0;
--shadow:0 10px 30px rgba(15,23,42,.09);
}
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial,Helvetica,sans-serif}
body{background:var(--bg);color:var(--text);line-height:1.7}
a{text-decoration:none;color:inherit}
img{max-width:100%;display:block}
.site-header{background:#0f172a;color:white;position:sticky;top:0;z-index:1000;box-shadow:0 4px 18px rgba(0,0,0,.18)}
.header-inner{width:92%;max-width:1200px;margin:auto;display:flex;align-items:center;justify-content:space-between;gap:18px;padding:14px 0}
.brand{display:flex;align-items:center;gap:12px;font-weight:900;font-size:22px}
.brand img{height:52px;border-radius:10px}
.nav{display:flex;gap:16px;font-weight:bold;font-size:14px}
.nav a{color:#e2e8f0;padding:8px 10px;border-radius:8px}
.nav a:hover{background:rgba(255,255,255,.08);color:white}
.actions{display:flex;gap:10px}
.btn{border:none;background:var(--primary);color:white;padding:9px 12px;border-radius:10px;font-weight:bold;cursor:pointer}
.mobile-menu{display:none;background:#111827;border-top:1px solid rgba(255,255,255,.08);padding:10px 4%}
.mobile-menu.show{display:block}
.mobile-menu a{display:block;color:white;padding:12px;border-bottom:1px solid rgba(255,255,255,.08);font-weight:bold}
.hero{background:linear-gradient(135deg,rgba(15,23,42,.94),rgba(37,99,235,.74)),url("https://picsum.photos/1600/700?haber") center/cover;color:white;padding:58px 0 48px}
.hero-inner{width:92%;max-width:1200px;margin:auto;display:grid;grid-template-columns:1.45fr .85fr;gap:24px;align-items:center}
.hero h1{font-size:42px;line-height:1.15;margin-bottom:16px}
.hero p{color:#dbeafe;font-size:18px;max-width:720px}
.badges{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.badge{font-size:13px;font-weight:bold;padding:8px 12px;border-radius:999px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.18)}
.hero-panel{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);padding:22px;border-radius:20px;backdrop-filter:blur(8px)}
.hero-panel a{display:block;color:white;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.15);font-weight:bold}
.container{width:92%;max-width:1200px;margin:auto;padding:34px 0}
.section-title{font-size:28px;line-height:1.2;margin-bottom:6px}
.section-subtitle{color:var(--muted);margin-bottom:22px}
.news-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
.news-card{background:var(--card);border-radius:20px;overflow:hidden;box-shadow:var(--shadow);border:1px solid rgba(226,232,240,.8);transition:.25s ease}
.news-card:hover{transform:translateY(-5px);box-shadow:0 16px 36px rgba(15,23,42,.14)}
.news-img{height:210px;width:100%;object-fit:cover;background:#e2e8f0}
.news-body{padding:18px}
.badge-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.tag{font-size:11px;font-weight:900;letter-spacing:.3px;padding:6px 9px;border-radius:8px;color:white}
.tag.breaking{background:var(--danger)}
.tag.category{background:var(--primary)}
.news-title{font-size:20px;line-height:1.28;margin-bottom:10px}
.news-meta{display:flex;flex-wrap:wrap;gap:10px;color:var(--muted);font-size:13px;margin-bottom:12px}
.news-desc{color:#334155;font-size:15px;margin-bottom:16px}
.action-row{display:flex;flex-wrap:wrap;gap:9px}
.action{display:inline-flex;align-items:center;justify-content:center;border:none;border-radius:10px;padding:10px 12px;font-weight:bold;font-size:14px;cursor:pointer}
.read{background:var(--primary);color:white}
.source{background:var(--green);color:white}
.share{background:var(--orange);color:white}
.article-layout{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:24px;align-items:start}
.article-card{background:var(--card);border-radius:22px;box-shadow:var(--shadow);overflow:hidden;border:1px solid rgba(226,232,240,.8)}
.article-cover{height:430px;width:100%;object-fit:cover}
.article-content{padding:28px}
.article-title{font-size:38px;line-height:1.15;margin:14px 0}
.article-text{font-size:19px;color:#334155;margin:20px 0}
.source-box{background:#eff6ff;border-left:5px solid var(--primary);padding:16px;border-radius:14px;margin:18px 0}
.sidebar{display:flex;flex-direction:column;gap:18px;position:sticky;top:92px}
.side-card{background:var(--card);border:1px solid rgba(226,232,240,.8);border-radius:20px;padding:20px;box-shadow:var(--shadow)}
.side-link{display:block;padding:12px 0;border-bottom:1px solid var(--border);font-weight:bold;font-size:14px;color:var(--text)}
.side-link:last-child{border-bottom:none}
.footer{margin-top:42px;background:#0f172a;color:white;padding:40px 0}
.footer-inner{width:92%;max-width:1200px;margin:auto;display:grid;grid-template-columns:2fr 1fr 1fr;gap:24px}
.footer p,.footer a{color:#cbd5e1}
.footer h3{margin-bottom:12px}
.footer a{display:block;margin:8px 0}
body.dark{--bg:#0b1120;--card:#111827;--text:#f8fafc;--muted:#cbd5e1;--border:#334155;--shadow:0 10px 30px rgba(0,0,0,.28);background:var(--bg);color:var(--text)}
body.dark .news-desc,body.dark .article-text{color:#d1d5db}
body.dark .section-title,body.dark .news-title,body.dark .article-title,body.dark .side-link{color:#f8fafc}
body.dark .source-box{background:#172554}

.ad-box{background:linear-gradient(135deg,#f8fafc,#e2e8f0);border:2px dashed #cbd5e1;border-radius:18px;min-height:92px;display:flex;align-items:center;justify-content:center;text-align:center;color:#475569;font-weight:900;margin:22px 0;padding:18px}
.ad-box small{display:block;color:#64748b;font-weight:bold;margin-top:4px}
.ad-sidebar{min-height:260px}
body.dark .ad-box{background:linear-gradient(135deg,#111827,#1f2937);border-color:#334155;color:#e5e7eb}

@media(max-width:950px){.hero-inner,.article-layout{grid-template-columns:1fr}.sidebar{position:static}.news-grid{grid-template-columns:1fr}.article-cover{height:300px}}
@media(max-width:760px){.header-inner{flex-wrap:wrap}.nav{display:none}.brand img{height:44px}.hero{padding:42px 0}.hero h1{font-size:31px}.container{padding:26px 0}.article-title{font-size:30px}.article-content{padding:20px}.news-img{height:190px}.footer-inner{grid-template-columns:1fr}}
</style>
"""



def reklam_html(konum="genel", sidebar=False):
    sinif = "ad-box ad-sidebar" if sidebar else "ad-box"
    return f"""
<div class="{sinif}">
<div>
📢 Reklam Alanı
<small>Google AdSense için hazır bölüm - {konum}</small>
</div>
</div>
"""


def header_html():
    return """
<header class="site-header">
<div class="header-inner">
<a class="brand" href="index.html"><img src="logo.png" alt="Ülkeden Haberler Logo"><span>Ülkeden Haberler</span></a>
<nav class="nav">
<a href="index.html">Ana Sayfa</a>
<a href="otomatik-gundem.html">Otomatik Haberler</a>
<a href="gundem.html">Gündem</a>
<a href="ekonomi.html">Ekonomi</a>
<a href="teknoloji.html">Teknoloji</a>
</nav>
<div class="actions"><button class="btn" id="menuBtn">☰ Menü</button><button class="btn" id="darkBtn">🌙 Mod</button></div>
</div>
<div class="mobile-menu" id="mobileMenu">
<a href="index.html">Ana Sayfa</a>
<a href="otomatik-gundem.html">Otomatik Haberler</a>
<a href="gundem-otomatik.html">Gündem Otomatik</a>
<a href="ekonomi-otomatik.html">Ekonomi Otomatik</a>
<a href="teknoloji-otomatik.html">Teknoloji Otomatik</a>
</div>
</header>
"""


def footer_html():
    return """
<footer class="footer">
<div class="footer-inner">
<div><h3>📰 Ülkeden Haberler</h3><p>Türkiye ve dünyadan güncel haberleri otomatik sistem desteğiyle takip eden modern haber platformu.</p></div>
<div><h3>Kategoriler</h3><a href="gundem.html">Gündem</a><a href="ekonomi.html">Ekonomi</a><a href="spor.html">Spor</a><a href="teknoloji.html">Teknoloji</a></div>
<div><h3>Hızlı Linkler</h3><a href="index.html">Ana Sayfa</a><a href="hakkimizda.html">Hakkımızda</a><a href="iletisim.html">İletişim</a></div>
</div>
</footer>
<script>
const menuBtn=document.getElementById("menuBtn");
const mobileMenu=document.getElementById("mobileMenu");
const darkBtn=document.getElementById("darkBtn");
if(localStorage.getItem("theme")==="dark"){document.body.classList.add("dark");}
if(menuBtn){menuBtn.addEventListener("click",()=>mobileMenu.classList.toggle("show"));}
if(darkBtn){darkBtn.addEventListener("click",()=>{document.body.classList.toggle("dark");localStorage.setItem("theme",document.body.classList.contains("dark") ? "dark" : "light");});}
function sharePage(title,url){
const fullUrl=new URL(url,window.location.href).href;
if(navigator.share){navigator.share({title:title,url:fullUrl});}
else if(navigator.clipboard){navigator.clipboard.writeText(fullUrl);alert("Link kopyalandı.");}
else{alert(fullUrl);}
}
</script>
"""


def haber_karti(haber):
    baslik = e(haber["baslik"])
    ozet = e(haber["ozet"][:140])
    kategori = e(haber["kategori"].upper())
    kaynak = e(haber["kaynak"])
    tarih = e(haber["tarih"])
    gorsel = e(haber["gorsel"])
    dosya = e(haber["dosya"])
    link = e(haber["link"])

    return f"""
<article class="news-card">
<img class="news-img" src="{gorsel}" alt="{baslik}" loading="lazy">
<div class="news-body">
<div class="badge-row"><span class="tag breaking">SON DAKİKA</span><span class="tag category">{kategori}</span></div>
<h3 class="news-title">{baslik}</h3>
<div class="news-meta"><span>📰 {kaynak}</span><span>📅 {tarih}</span></div>
<p class="news-desc">{ozet}...</p>
<div class="action-row">
<a class="action read" href="{dosya}">Haberi Oku →</a>
<a class="action source" href="{link}" target="_blank" rel="noopener noreferrer">Kaynağa Git 🌍</a>
<button class="action share" onclick="sharePage('{baslik}', '{dosya}')">📤 Paylaş</button>
</div>
</div>
</article>
"""


def liste_sayfasi_html(baslik, aciklama, haberler, aktif_kategori=None):
    if aktif_kategori:
        liste = [h for h in haberler if h["kategori"] == aktif_kategori]
    else:
        liste = haberler

    kartlar = "\n".join(haber_karti(h) for h in liste)
    populer = "\n".join(f'<a class="side-link" href="{e(h["dosya"])}">{e(h["baslik"])}</a>' for h in liste[:5])

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(baslik)} - Ülkeden Haberler</title>
<meta name="description" content="{e(aciklama)}">
<link rel="icon" type="image/png" href="favicon.png">
{ortak_css()}
</head>
<body>
{header_html()}
<section class="hero">
<div class="hero-inner">
<div>
<h1>{e(baslik)}</h1>
<p>{e(aciklama)}</p>
<div class="badges"><span class="badge">🤖 Otomatik Sistem</span><span class="badge">📰 Güncel İçerik</span><span class="badge">🌙 Dark Mode</span><span class="badge">📱 Mobil Uyumlu</span></div>
</div>
<div class="hero-panel">
<h3>Hızlı Erişim</h3>
<a href="otomatik-gundem.html">Tüm Otomatik Haberler</a>
<a href="gundem-otomatik.html">Gündem Haberleri</a>
<a href="ekonomi-otomatik.html">Ekonomi Haberleri</a>
<a href="teknoloji-otomatik.html">Teknoloji Haberleri</a>
</div>
</div>
</section>
<main class="container">
<h2 class="section-title">{e(baslik)}</h2>
<p class="section-subtitle">Toplam haber: {len(liste)}</p>
{reklam_html("Liste üstü reklam")}
<div class="article-layout">
<section><div class="news-grid">{kartlar}</div></section>
<aside class="sidebar">
<div class="side-card"><h3>🔥 Öne Çıkanlar</h3>{populer}</div>
{reklam_html("Sidebar reklam", sidebar=True)}
<div class="side-card"><h3>↩️ Geri Dön</h3><a class="side-link" href="index.html">Ana Sayfa</a><a class="side-link" href="otomatik-gundem.html">Otomatik Haberler</a></div>
</aside>
</div>
</main>
{footer_html()}
</body>
</html>"""


def haber_sayfasi_olustur(haber):
    baslik = e(haber["baslik"])
    ozet = e(haber["ozet"])
    kategori = e(haber["kategori"].upper())
    link = e(haber["link"])
    gorsel = e(haber["gorsel"])
    kaynak = e(haber["kaynak"])
    tarih = e(haber["tarih"])
    dosya = e(haber["dosya"])
    canonical = f"{SITE_URL}/{dosya}"
    okuma_suresi = max(1, round(len(haber["ozet"].split()) / 180))

    sayfa = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{baslik} - Ülkeden Haberler</title>
<meta name="description" content="{baslik} - Ülkeden Haberler tarafından otomatik oluşturulan güncel haber.">

<meta name="keywords" content="{kategori.lower()}, haber, son dakika, {kaynak}, Türkiye, dünya">

<meta name="author" content="Ülkeden Haberler">

<meta property="og:type" content="article">
<meta property="og:title" content="{baslik}">
<meta property="og:description" content="{ozet[:150]}">
<meta property="og:image" content="{gorsel}">
<meta property="og:url" content="{SITE_URL}/{haber['dosya']}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{baslik}">
<meta name="twitter:description" content="{ozet[:150]}">
<meta name="twitter:image" content="{gorsel}">
<script type="application/ld+json">
{{
"@context":"https://schema.org",
"@type":"NewsArticle",
"headline":"{baslik}",
"image":["{gorsel}"],
"datePublished":"{tarih}",
"author":{{
"@type":"Organization",
"name":"Ülkeden Haberler"
}},
"publisher":{{
"@type":"Organization",
"name":"Ülkeden Haberler",
"logo":{{
"@type":"ImageObject",
"url":"{SITE_URL}/logo.png"
}}
}},
"mainEntityOfPage":"{SITE_URL}/{haber['dosya']}"
}}
</script>
<meta name="description" content="{baslik}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="favicon.png">
<meta property="og:title" content="{baslik}">
<meta property="og:description" content="{baslik}">
<meta property="og:type" content="article">
<meta property="og:image" content="{gorsel}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{baslik}">
<meta name="twitter:description" content="{baslik}">
<meta name="twitter:image" content="{gorsel}">
{ortak_css()}
<script type="application/ld+json">
{{
"@context":"https://schema.org",
"@type":"NewsArticle",
"headline":"{baslik}",
"image":["{gorsel}"],
"datePublished":"{datetime.now().isoformat()}",
"dateModified":"{datetime.now().isoformat()}",
"author":{{"@type":"Organization","name":"Ülkeden Haberler"}},
"publisher":{{"@type":"Organization","name":"Ülkeden Haberler","logo":{{"@type":"ImageObject","url":"{SITE_URL}/logo.png"}}}},
"mainEntityOfPage":"{canonical}"
}}
</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7206741398758511"
     crossorigin="anonymous"></script>
</head>
<body>
{header_html()}
<main class="container">
<div class="article-layout">
<article class="article-card">
<img class="article-cover" src="{gorsel}" alt="{baslik}">
<div class="article-content">
<div class="badge-row"><span class="tag breaking">SON DAKİKA</span><span class="tag category">{kategori}</span></div>
<h1 class="article-title">{baslik}</h1>
<div class="news-meta"><span>📅 {tarih}</span><span>📰 {kaynak}</span><span>⏱️ {okuma_suresi} dk okuma</span></div>
{reklam_html("Haber üstü reklam")}
<p class="article-text">{ozet}</p>
<div class="source-box">
<strong>Kaynak Bilgisi</strong><br>
Bu içerik RSS kaynağından alınan bilgilerle otomatik olarak oluşturulmuştur.
</div>
<div class="action-row">
<a class="action source" href="{link}" target="_blank" rel="noopener noreferrer">Orijinal Haberi Görüntüle 🌍</a>
<button class="action share" onclick="sharePage('{baslik}', '{dosya}')">📤 Paylaş</button>
<a class="action read" href="otomatik-gundem.html">← Otomatik Haberlere Dön</a>
</div>
{reklam_html("Haber altı reklam")}
</div>
</article>
<aside class="sidebar">
{reklam_html("Haber sidebar reklam", sidebar=True)}
<div class="side-card"><h3>📰 Haber Bilgileri</h3><a class="side-link">Kategori: {kategori}</a><a class="side-link">Kaynak: {kaynak}</a><a class="side-link">Tarih: {tarih}</a></div>
<div class="side-card"><h3>📂 Kategoriler</h3><a class="side-link" href="gundem-otomatik.html">Gündem</a><a class="side-link" href="ekonomi-otomatik.html">Ekonomi</a><a class="side-link" href="teknoloji-otomatik.html">Teknoloji</a></div>
</aside>
</div>
</main>
{footer_html()}
</body>
</html>"""

    with open(haber["dosya"], "w", encoding="utf-8") as f:
        f.write(sayfa)

    print(f"Oluşturuldu: {haber['dosya']}")


def otomatik_liste_olustur(haberler):
    sayfa = liste_sayfasi_html(
        "Otomatik Haberler",
        "Ülkeden Haberler otomatik haber sistemi tarafından güncellenen son haberler.",
        haberler
    )
    with open("otomatik-gundem.html", "w", encoding="utf-8") as f:
        f.write(sayfa)


def kategori_sayfalari_olustur(haberler):
    ayarlar = {
        "gundem": ("Gündem Otomatik Haberleri", "Türkiye gündemine dair otomatik sistem tarafından güncellenen son haberler."),
        "ekonomi": ("Ekonomi Otomatik Haberleri", "Ekonomi, piyasa ve finans gündemine dair otomatik sistem tarafından güncellenen haberler."),
        "teknoloji": ("Teknoloji Otomatik Haberleri", "Teknoloji, yapay zeka ve dijital dünyaya dair otomatik sistem tarafından güncellenen haberler.")
    }

    for kategori, (baslik, aciklama) in ayarlar.items():
        sayfa = liste_sayfasi_html(baslik, aciklama, haberler, kategori)
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



def url_json_oku(url, timeout=15):
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Ülkeden Haberler Bot)",
                "Accept": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as hata:
        print(f"Veri alınamadı: {url} | {hata}")
        return None


def hava_durumu_json_olustur():
    sehirler = [
        {"sehir": "İstanbul", "lat": 41.0082, "lon": 28.9784},
        {"sehir": "Ankara", "lat": 39.9334, "lon": 32.8597},
        {"sehir": "İzmir", "lat": 38.4192, "lon": 27.1287},
        {"sehir": "Gaziantep", "lat": 37.0662, "lon": 37.3833}
    ]

    sonuc = []

    for s in sehirler:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={s['lat']}&longitude={s['lon']}"
            "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,apparent_temperature"
            "&timezone=auto"
        )

        data = url_json_oku(url)
        current = data.get("current", {}) if data else {}

        sonuc.append({
            "sehir": s["sehir"],
            "sicaklik": current.get("temperature_2m"),
            "hissedilen": current.get("apparent_temperature"),
            "nem": current.get("relative_humidity_2m"),
            "ruzgar": current.get("wind_speed_10m"),
            "guncelleme": datetime.now().strftime("%d.%m.%Y %H:%M")
        })

    with open("hava-durumu.json", "w", encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=4)


def son_depremler_json_olustur():
    sonuc = []

    # Türkiye ve çevresi - son 14 gün
    start = datetime.now().strftime("%Y-%m-%d")
    url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query"
        "?format=geojson"
        "&starttime=2020-01-01"
        "&minlatitude=35&maxlatitude=43"
        "&minlongitude=25&maxlongitude=46"
        "&minmagnitude=1.5"
        "&orderby=time"
        "&limit=8"
    )

    data = url_json_oku(url)

    if data and "features" in data:
        for eq in data["features"][:8]:
            prop = eq.get("properties", {})
            geo = eq.get("geometry", {})
            coords = geo.get("coordinates", [])

            zaman = prop.get("time")
            if zaman:
                try:
                    zaman = datetime.fromtimestamp(zaman / 1000).strftime("%d.%m.%Y %H:%M")
                except Exception:
                    zaman = ""

            sonuc.append({
                "yer": prop.get("place", "Türkiye çevresi"),
                "buyukluk": prop.get("mag", "-"),
                "zaman": zaman,
                "derinlik": coords[2] if len(coords) > 2 else "",
                "guncelleme": datetime.now().strftime("%d.%m.%Y %H:%M")
            })

    with open("son-depremler.json", "w", encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=4)


def doviz_json_olustur():
    sonuc = []

    # Güvenilir ücretsiz kur servisi
    data = url_json_oku("https://api.frankfurter.app/latest?from=TRY&to=USD,EUR,GBP")

    if data and "rates" in data:
        rates = data["rates"]

        def ters_kur(kod):
            try:
                return round(1 / float(rates[kod]), 2)
            except Exception:
                return None

        sonuc = [
            {"kod": "USD", "ad": "Amerikan Doları", "deger": ters_kur("USD"), "birim": "₺"},
            {"kod": "EUR", "ad": "Euro", "deger": ters_kur("EUR"), "birim": "₺"},
            {"kod": "GBP", "ad": "İngiliz Sterlini", "deger": ters_kur("GBP"), "birim": "₺"}
        ]

    with open("doviz.json", "w", encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=4)


def altin_json_olustur():
    # Ücretsiz ve stabil altın API'si olmadan sahte veri üretmiyoruz.
    # AdSense ve güven açısından boş/uyarı JSON üretmek daha doğru.
    sonuc = [
        {
            "kod": "ALTIN",
            "ad": "Altın verisi",
            "deger": None,
            "birim": "₺",
            "not": "Güvenilir canlı altın kaynağı bağlanınca otomatik güncellenecek."
        }
    ]

    with open("altin.json", "w", encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=4)


def canli_veriler_json_olustur():
    print("Canlı veri sistemi başladı.")
    hava_durumu_json_olustur()
    son_depremler_json_olustur()
    doviz_json_olustur()
    altin_json_olustur()
    print("Canlı veri JSON dosyaları oluşturuldu.")


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
    canli_veriler_json_olustur()
    log_yaz()

    print("Otomatik haber sistemi başarıyla tamamlandı.")


if __name__ == "__main__":
    main()
