#!/usr/bin/env python3
"""
Apartman Assistant blog generátor.

Hogyan adj hozzá új cikket:
1. Hozz létre egy új .json fájlt a blog-content/ mappában (bármilyen néven).
   Kötelező mezők: slug, title, metaDescription, publishDate (YYYY-MM-DD),
   readingMinutes, excerpt, bodyHtml (a cikk törzse, HTML-ként: <p>, <h2>, <h3> stb.)
2. Futtasd: python3 generate_blog.py
3. Ez legyártja / frissíti:
   - blog/<slug>.html  (a cikk saját oldala, teljes SEO meta-adatokkal)
   - blog/index.html   (a bloglista, minden cikkel, legújabb elöl)
   - sitemap.xml        (minden cikk URL-jével)

Semmi mást nem kell kézzel szerkeszteni.
"""
import json
import os
import glob

SITE_URL = "https://apartmanassistant.hu"
SITE_NAME = "Apartman Assistant"
OG_IMAGE = f"{SITE_URL}/assets/og-image.jpg"

CONTENT_DIR = "blog-content"
OUTPUT_DIR = "blog"

HEADER = f"""<header class="site-header" data-block="header">
  <div class="container site-header__inner">
    <a class="logo" href="/" aria-label="{SITE_NAME} — kezdőlap">
      <span class="logo__mark"><svg viewBox="0 0 24 24"><use href="#icon-home"/></svg></span>
      {SITE_NAME}
    </a>
    <a class="btn btn-primary" href="/#cta" data-cta="header">
      Csatlakozom
    </a>
  </div>
</header>"""

FOOTER = f"""<footer class="site-footer" data-block="footer">
  <div class="container site-footer__inner">
    <div class="site-footer__brand">
      <span class="logo__mark" style="width:26px;height:26px">
        <svg viewBox="0 0 24 24" style="width:15px;height:15px"><use href="#icon-home"/></svg>
      </span>
      {SITE_NAME}
    </div>
    <ul class="site-footer__links">
      <li><a href="/blog">Blog</a></li>
      <li><a href="/kapcsolat">Kapcsolat</a></li>
      <li><a href="/aszf">ÁSZF</a></li>
      <li><a href="/adatkezelesi-tajekoztato">Adatkezelési tájékoztató</a></li>
      <li><a href="/impresszum">Impresszum</a></li>
    </ul>
    <p class="site-footer__meta">© 2026 {SITE_NAME}</p>
  </div>
</footer>"""

COOKIE_BANNER = """<div class="cookie-banner" id="cookie-banner" data-block="cookie-banner" role="dialog" aria-label="Cookie beállítások" aria-live="polite">
  <p>
    A weboldal a működéshez szükséges és — hozzájárulásod esetén — statisztikai,
    mérési sütiket használ. Bővebben az
    <a href="/adatkezelesi-tajekoztato">Adatkezelési tájékoztatóban</a>.
  </p>
  <div class="cookie-banner__actions">
    <button class="btn btn-primary" id="cookie-accept" type="button">Elfogadom</button>
    <button class="btn btn-ghost" id="cookie-reject" type="button">Csak a szükséges</button>
  </div>
</div>"""

ICON_SPRITE = """<svg style="display:none">
  <symbol id="icon-home" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 12l9-9 9 9"/><path d="M5 10v10a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1V10"/>
  </symbol>
</svg>"""

HU_MONTHS = ["", "jan.", "feb.", "márc.", "ápr.", "máj.", "jún.", "júl.", "aug.", "szept.", "okt.", "nov.", "dec."]


def hu_date(iso_date):
    y, m, d = iso_date.split("-")
    return f"{y}. {HU_MONTHS[int(m)]} {int(d)}."


def load_posts():
    posts = []
    for path in glob.glob(os.path.join(CONTENT_DIR, "*.json")):
        with open(path, encoding="utf-8") as f:
            posts.append(json.load(f))
    posts.sort(key=lambda p: p["publishDate"], reverse=True)
    return posts


def render_article_page(post):
    url = f"{SITE_URL}/blog/{post['slug']}"
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["metaDescription"],
        "datePublished": post["publishDate"],
        "author": {"@type": "Organization", "name": SITE_NAME},
        "publisher": {"@type": "Organization", "name": SITE_NAME},
        "mainEntityOfPage": url,
        "image": OG_IMAGE,
    }
    return f"""<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />

<title>{post['title']} — {SITE_NAME} Blog</title>
<meta name="description" content="{post['metaDescription']}" />
<link rel="canonical" href="{url}" />
<meta name="robots" content="index, follow" />
<meta name="theme-color" content="#10161a" />
<link rel="icon" href="/favicon.png" type="image/png" sizes="192x192" />
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />

<meta property="og:type" content="article" />
<meta property="og:site_name" content="{SITE_NAME}" />
<meta property="og:title" content="{post['title']}" />
<meta property="og:description" content="{post['metaDescription']}" />
<meta property="og:url" content="{url}" />
<meta property="og:locale" content="hu_HU" />
<meta property="og:image" content="{OG_IMAGE}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{post['title']}" />
<meta name="twitter:description" content="{post['metaDescription']}" />
<meta name="twitter:image" content="{OG_IMAGE}" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/style.css" />

<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
{ICON_SPRITE}
{HEADER}

<main id="main">
<article class="section blog-article">
  <div class="container container--narrow">
    <a class="blog-back" href="/blog">← Vissza a bloghoz</a>
    <p class="blog-meta">{hu_date(post['publishDate'])} · {post['readingMinutes']} perc olvasás</p>
    <h1>{post['title']}</h1>
    <div class="blog-prose">
{post['bodyHtml']}
    </div>
    <div class="blog-article__cta card">
      <h3>Készen állsz kipróbálni?</h3>
      <p>Az Apartman Assistant automatikusan összefésüli a foglalásaidat — bevezető időszakban díjmentesen.</p>
      <a class="btn btn-primary" href="/#cta">Csatlakozom a bevezető időszakhoz</a>
    </div>
  </div>
</article>
</main>

{FOOTER}
{COOKIE_BANNER}
<script src="/script.js" defer></script>
</body>
</html>
"""


def render_index_page(posts):
    cards = []
    for post in posts:
        cards.append(f"""      <a class="blog-card" href="/blog/{post['slug']}">
        <p class="blog-card__meta">{hu_date(post['publishDate'])} · {post['readingMinutes']} perc</p>
        <h2 class="blog-card__title">{post['title']}</h2>
        <p class="blog-card__excerpt">{post['excerpt']}</p>
        <span class="blog-card__link">Elolvasom →</span>
      </a>""")
    cards_html = "\n".join(cards)

    return f"""<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />

<title>Blog — {SITE_NAME}</title>
<meta name="description" content="Cikkek apartmankiadásról, Airbnb és Szállás.hu kezelésről, vendégkommunikációról és adminisztrációról." />
<link rel="canonical" href="{SITE_URL}/blog" />
<meta name="robots" content="index, follow" />
<meta name="theme-color" content="#10161a" />
<link rel="icon" href="/favicon.png" type="image/png" sizes="192x192" />
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />

<meta property="og:type" content="website" />
<meta property="og:site_name" content="{SITE_NAME}" />
<meta property="og:title" content="Blog — {SITE_NAME}" />
<meta property="og:description" content="Cikkek apartmankiadásról, Airbnb és Szállás.hu kezelésről, vendégkommunikációról és adminisztrációról." />
<meta property="og:url" content="{SITE_URL}/blog" />
<meta property="og:locale" content="hu_HU" />
<meta property="og:image" content="{OG_IMAGE}" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/style.css" />
</head>
<body>
{ICON_SPRITE}
{HEADER}

<main id="main">
<section class="section">
  <div class="container">
    <div class="section-head section-head--center">
      <p class="eyebrow">Blog</p>
      <h1>Cikkek apartmankiadóknak</h1>
      <p class="lead">Gyakorlati tippek Airbnb, Szállás.hu és Booking.com kezeléséről, vendégadminisztrációról és időmegtakarításról.</p>
    </div>
    <div class="blog-grid">
{cards_html}
    </div>
  </div>
</section>
</main>

{FOOTER}
{COOKIE_BANNER}
<script src="/script.js" defer></script>
</body>
</html>
"""


def render_sitemap(posts):
    urls = [
        ("", "1.0", "monthly"),
        ("blog", "0.8", "weekly"),
    ]
    for post in posts:
        urls.append((f"blog/{post['slug']}", "0.7", "monthly"))

    entries = []
    for path, priority, freq in urls:
        loc = f"{SITE_URL}/{path}" if path else f"{SITE_URL}/"
        lastmod = posts[0]["publishDate"] if posts and path == "blog" else "2026-07-13"
        entries.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(entries)}
</urlset>
"""


def main():
    posts = load_posts()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for post in posts:
        with open(os.path.join(OUTPUT_DIR, f"{post['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(render_article_page(post))

    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_index_page(posts))

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(render_sitemap(posts))

    print(f"Kész: {len(posts)} cikk legenerálva.")
    for post in posts:
        print(f"  - /blog/{post['slug']}")


if __name__ == "__main__":
    main()
