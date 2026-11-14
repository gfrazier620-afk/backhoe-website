"""Generates the site's four HTML pages plus sitemap.xml, robots.txt, the social
share image and favicons.  Run:  python tools/build_pages.py   (needs Pillow).
Change SITE_URL below when the custom domain goes live, then rebuild."""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
IMG = OUT / "assets" / "img"

# Public address of the site. Update when the domain is connected (keep trailing slash).
SITE_URL = "https://gfrazier620-afk.github.io/backhoe-website/"
# Quote form delivery (FormSubmit: no account; Travis confirms the first email once).
FORM_ENDPOINT = "https://formsubmit.co/ajax/travfraz@hotmail.com"
PHONE_TEL = "9514400647"
PHONE = "(951) 440-0647"
EMAIL = "travfraz@hotmail.com"
NAME = "Travis Frazier Backhoe Service LLC"

SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<symbol id="i-phone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></symbol>
<symbol id="i-shovel" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 22v-5l5-5 5 5-5 5z"/><path d="M9.5 14.5 16 8"/><path d="m17 2 5 5-.5.5a3.53 3.53 0 0 1-5 0 3.53 3.53 0 0 1 0-5z"/></symbol>
<symbol id="i-ruler" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.4 2.4 0 0 1 0-3.4l2.6-2.6a2.4 2.4 0 0 1 3.4 0z"/><path d="m14.5 12.5 2-2M11.5 9.5l2-2M8.5 6.5l2-2M17.5 15.5l2-2"/></symbol>
<symbol id="i-layers" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 2 10 5-10 5L2 7z"/><path d="m2 12 10 5 10-5"/><path d="m2 17 10 5 10-5"/></symbol>
<symbol id="i-cone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="8" rx="1"/><path d="M17 14v7M7 14v7M17 3v3M7 3v3M10 14 2.3 6.3M14 6l7.7 7.7M8 6l8 8"/></symbol>
<symbol id="i-hammer" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 12-8.5 8.5a2.12 2.12 0 0 1-3-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25c-.6-.6-.93-1.4-.93-2.25v-.86L16.01 4.6a5.56 5.56 0 0 0-3.94-1.64H9l.92.82A6.18 6.18 0 0 1 12 8.4v1.56l2 2h2.47l2.26 1.91"/></symbol>
<symbol id="i-truck" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></symbol>
</defs></svg>"""


COUNTIES = ["Inland Empire", "Los Angeles", "Orange County", "Desert communities", "Bay Area &amp; San Jose"]


def chips():
    return "\n".join(f"            <li>{c}</li>" for c in COUNTIES)


def dims(img):
    with Image.open(IMG / img) as im:
        return im.size


def img_attrs(img):
    w, h = dims(img)
    return f'width="{w}" height="{h}"'


PAGE_DESC = {}


def jsonld():
    areas = ["Southern California", "Inland Empire", "Los Angeles", "Orange County", "Bay Area", "San Jose"]
    data = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "name": "Travis Frazier Backhoe Service LLC",
        "legalName": "Travis Frazier Backhoe Service, LLC",
        "url": SITE_URL,
        "telephone": "+1-951-440-0647",
        "email": EMAIL,
        "image": SITE_URL + "assets/img/og-image.jpg",
        "logo": SITE_URL + "assets/img/logo-transparent.png",
        "description": "Backhoe service with operator for plumbers, electricians, fire line and pipeline contractors, and property owners across Southern California and beyond.",
        "foundingDate": "2025-05-29",
        "founder": {"@type": "Person", "name": "Travis Frazier"},
        "areaServed": [{"@type": "Place", "name": a} for a in areas],
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d}}
            for _, t, d in SERVICES
        ],
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def icon(n, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} aria-hidden="true"><use href="#i-{n}"/></svg>'


def head(title, desc, page="index.html"):
    url = SITE_URL + ("" if page == "index.html" else page)
    preload = ('    <link rel="preload" as="image" href="assets/img/backhoe-owner.jpg" fetchpriority="high">\n'
               if page == "index.html" else "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{url}">
    <meta name="theme-color" content="#0b0b0c">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{NAME}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{SITE_URL}assets/img/og-image.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{SITE_URL}assets/img/og-image.jpg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{preload}    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/styles.css">
    <link rel="icon" href="favicon.ico" sizes="any">
    <link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
    <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
    <script type="application/ld+json">
{jsonld()}
    </script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{SPRITE}
"""


def nav(active):
    items = [("index.html", "Home"), ("services.html", "Services"), ("gallery.html", "Gallery"), ("contact.html", "Contact")]
    li = "\n".join(
        f'                <li><a{" class=\"active\" aria-current=\"page\"" if h == active else ""} href="{h}">{t}</a></li>' for h, t in items
    )
    return f"""<header>
    <nav class="navbar" aria-label="Main">
        <a class="nav-left" href="index.html">
            <img src="assets/img/logo-transparent.png" class="nav-logo" alt="" {img_attrs("logo-transparent.png")}>
            <span class="nav-title">Travis Frazier <span>Backhoe</span> Service</span>
        </a>
        <div class="nav-right">
            <ul class="nav-links">
{li}
            </ul>
            <a class="nav-call" href="tel:{PHONE_TEL}">{icon("phone")} {PHONE}</a>
            <button class="hamburger" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button>
        </div>
    </nav>
</header>
<main id="main">
"""


FOOTER = f"""</main>

<footer>
    <div class="container">
        <div class="footer-grid">
            <div class="footer-brand">
                <img src="assets/img/logo-transparent.png" alt="{NAME} logo" loading="lazy" {img_attrs("logo-transparent.png")}>
                <p>Backhoe service with operator: excavation, trenching, grading, and site prep across Southern California and beyond.</p>
            </div>
            <div>
                <h4>Explore</h4>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="services.html">Services</a></li>
                    <li><a href="gallery.html">Gallery</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </div>
            <div>
                <h4>Get in touch</h4>
                <ul>
                    <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
                    <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
                    <li>Southern California &amp; beyond</li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; 2025 Travis Frazier Backhoe Service, LLC. All rights reserved.</span>
        </div>
    </div>
</footer>

<div class="call-bar">
    <a href="tel:{PHONE_TEL}">{icon("phone")} Call</a>
    <a href="contact.html#quote-form">Free Quote</a>
</div>
"""

LIGHTBOX = """<div id="lightbox" class="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer">
    <button class="lightbox-close" aria-label="Close">&times;</button>
    <img class="lightbox-content" id="lightbox-img" alt="">
</div>
"""

END = """
<script src="assets/js/main.js"></script>
</body>
</html>
"""

SERVICES = [
    ("shovel", "Excavation", "Full-service excavation for foundations, pools, utilities, and site development."),
    ("ruler", "Trenching", "Precision trenching for electrical, plumbing, irrigation, and drainage systems."),
    ("layers", "Grading", "Rough and finish grading to prepare your land for construction or landscaping."),
    ("cone", "Site Preparation", "Land clearing, leveling, and prep work to get your project ready to build."),
    ("hammer", "Concrete Removal", "Breaking out and removing concrete driveways, patios, slabs, and more."),
]


def service_cards(n=6):
    out = []
    for i, (ic, t, d) in enumerate(SERVICES[:n], 1):
        out.append(f"""        <article class="service-card reveal" data-delay="{(i - 1) % 3 + 1}">
            <span class="service-num">0{i}</span>
            <div class="service-icon">{icon(ic)}</div>
            <h3>{t}</h3>
            <p>{d}</p>
        </article>""")
    return "\n".join(out)


def quote_form(heading_extra=""):
    options = "\n".join(f"                        <option>{t}</option>" for _, t, _ in SERVICES)
    return f"""<section id="quote-form">
    <div class="container quote-wrap">
        <div class="quote-side reveal">
            <div class="eyebrow">Free estimates</div>
            <h2 class="section-title">Request a quote</h2>
            <p>Tell us about your project and we&rsquo;ll get back to you with a fair, accurate quote.</p>
            <ul>
                <li>{icon("check")} No-pressure, free estimates</li>
                <li>{icon("check")} Honest, upfront pricing</li>
                <li>{icon("check")} Will travel to your jobsite</li>
            </ul>
            <p style="margin-top:26px">Prefer to talk? Call <a href="tel:{PHONE_TEL}" style="color:var(--yellow);font-weight:700">{PHONE}</a>.</p>
        </div>

        <form class="quote-form reveal" data-delay="1" action="{FORM_ENDPOINT.replace('/ajax', '')}" method="POST" data-endpoint="{FORM_ENDPOINT}">
            <input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;opacity:0">
            <input type="hidden" name="_subject" value="New quote request from the website">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="_next" value="{SITE_URL}contact.html">
            <div class="form-row">
                <div class="form-group">
                    <label for="f-name">Your name</label>
                    <input id="f-name" name="name" type="text" placeholder="John Doe" autocomplete="name" required>
                </div>
                <div class="form-group">
                    <label for="f-phone">Phone number</label>
                    <input id="f-phone" name="phone" type="tel" placeholder="(555) 123-4567" autocomplete="tel" required>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="f-email">Email (optional)</label>
                    <input id="f-email" name="email" type="email" placeholder="you@example.com" autocomplete="email">
                </div>
                <div class="form-group">
                    <label for="f-service">Service needed</label>
                    <select id="f-service" name="service" required>
                        <option value="">Select a service&hellip;</option>
{options}
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label for="f-details">Project details</label>
                <textarea id="f-details" name="details" rows="5" placeholder="Where is the job, how big is it, and when do you need it done?"></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Send request</button>
            <p class="form-success" role="status" aria-live="polite">Thanks! Your request was sent. Travis will get back to you soon &mdash; or call {PHONE} for a faster answer.</p>
            <p class="form-error" role="alert">We couldn&rsquo;t send that automatically, so we opened an email with your details filled in. Just hit send, or call {PHONE}.</p>
            <p class="form-note">Your details go straight to Travis by email and are used only to answer your request.</p>
        </form>
    </div>
</section>
"""


def page_hero(img, eyebrow, h1, p):
    return f"""<section class="page-hero" style="--hero-img:url('../img/{img}')">
    <div class="container">
        <div class="eyebrow">{eyebrow}</div>
        <h1>{h1}</h1>
        <p>{p}</p>
    </div>
</section>
<div class="hazard"></div>
"""


WHY = [
    "Licensed &amp; insured",
    "Family-owned since 2025",
    "Professional equipment",
    "Fast, reliable service",
    "Fair &amp; honest pricing",
    "Free estimates",
]


def why_grid():
    return "\n".join(f'        <div class="why-item reveal">{icon("check")} {w}</div>' for w in WHY)


def shot(img, alt, cap, sub, delay=0):
    d = f' data-delay="{delay}"' if delay else ""
    return f"""        <figure class="shot lightbox-trigger reveal"{d} tabindex="0" role="button" aria-label="Enlarge photo: {cap}">
            <img src="assets/img/{img}" alt="{alt}" loading="lazy" decoding="async" {img_attrs(img)}>
            <figcaption>{cap}<small>{sub}</small></figcaption>
        </figure>"""


# ----------------------------------------------------------------- HOME
home = head(NAME, page="index.html", desc="Backhoe service with operator for plumbers, electricians, fire line and pipeline contractors across Southern California and beyond. Will travel to the job.") + nav("index.html") + f"""
<section class="hero">
    <div class="container">
        <div class="hero-content">
            <div class="eyebrow">Southern California &bull; Since 2025</div>
            <h1>We dig it.<br><em>You build on it.</em></h1>
            <p class="lead">Backhoe service with an experienced operator for plumbers, electricians, fire line and pipeline contractors, and property owners across Southern California.</p>
            <div class="hero-actions">
                <a class="btn btn-primary" href="contact.html#quote-form">Get a free quote</a>
                <a class="btn btn-ghost" href="tel:{PHONE_TEL}">{icon("phone")} {PHONE}</a>
            </div>
        </div>
    </div>
</section>

<section class="stats" aria-label="Highlights">
    <div class="container stats-grid">
        <div class="stat"><strong>20+</strong><span>Years running heavy equipment</span></div>
        <div class="stat"><strong>SoCal+</strong><span>We go where the job is</span></div>
        <div class="stat"><strong>2018</strong><span>CASE 580 Super N</span></div>
        <div class="stat"><strong>Free</strong><span>Estimates, always</span></div>
    </div>
</section>

<section class="trades">
    <div class="container">
        <div class="section-head center reveal">
            <div class="eyebrow">Built for the trades</div>
            <h2 class="section-title">Digging for the people who build</h2>
            <p class="section-lead">Contractors call us when they need a trench, a pit, or a site opened up &mdash; done right, on schedule.</p>
        </div>
        <ul class="chips reveal">
            <li>Plumbers</li><li>Electricians</li><li>Fire line companies</li><li>Pipeline companies</li><li>General contractors</li><li>Property owners</li>
        </ul>
    </div>
</section>

<section class="services">
    <div class="container">
        <div class="section-head reveal">
            <div class="eyebrow">What we do</div>
            <h2 class="section-title">Dirt work, done right</h2>
            <p class="section-lead">From a simple trench to a full site prep, we bring the right equipment and the experience to use it.</p>
        </div>
        <div class="service-grid">
{service_cards(5)}
        </div>
        <div class="services-cta"><a class="btn btn-ghost" href="services.html">See all services</a></div>
    </div>
</section>

<section>
    <div class="container">
        <div class="section-head center reveal">
            <div class="eyebrow">How it works</div>
            <h2 class="section-title">Simple from start to finish</h2>
        </div>
        <div class="steps">
            <div class="step reveal"><h3>Tell us the job</h3><p>Call or send a quick request describing what you need dug or graded.</p></div>
            <div class="step reveal" data-delay="1"><h3>Get a fair quote</h3><p>We look at the details and give you an honest, upfront price &mdash; no surprises.</p></div>
            <div class="step reveal" data-delay="2"><h3>We get to work</h3><p>We show up with the right equipment and finish the job safely and on schedule.</p></div>
        </div>
    </div>
</section>

<section class="work">
    <div class="container">
        <div class="section-head reveal">
            <div class="eyebrow">Recent work</div>
            <h2 class="section-title">On the jobsite</h2>
        </div>
        <div class="mosaic">
{shot("crew-utility-trench.jpg", "Crew laying conduit in a deep utility trench on an active construction site", "Utility trench", "Conduit going in, crew on site")}
{shot("deep-trench-pipe.jpg", "Deep, straight trench with pipe running along the bottom", "Deep trenching", "Straight walls, clean bottom", 1)}
{shot("backhoe-on-site.jpg", "CASE backhoe beside a freshly dug trench", "On the job", "Backhoe working a trench", 2)}
        </div>
        <div class="services-cta"><a class="btn btn-ghost" href="gallery.html">View full gallery</a></div>
    </div>
</section>

<section class="machine">
    <div class="container machine-grid">
        <figure class="machine-photo reveal">
            <img src="assets/img/backhoe-owner.jpg" alt="2018 CASE 580 Super N backhoe loader at a construction site" loading="lazy" decoding="async" {img_attrs("backhoe-owner.jpg")}>
        </figure>
        <div class="reveal" data-delay="1">
            <div class="eyebrow">The equipment</div>
            <h2 class="section-title">2018 CASE 580 Super N</h2>
            <p class="section-lead">A late-model backhoe loader, run by an operator with 20+ years in the seat.</p>
            <ul class="spec-list">
                <li>{icon("check")} Backhoe service <b>with operator</b></li>
                <li>{icon("check")} Equipment rental available &mdash; <a href="contact.html#quote-form">ask for details</a></li>
                <li>{icon("check")} Trenching, pits, grading &amp; site prep</li>
            </ul>
        </div>
    </div>
</section>

<section>
    <div class="container owner-grid">
        <div class="owner-photo reveal">
            <img src="assets/img/owner.jpg" alt="Travis Frazier in front of his CASE backhoe" loading="lazy" decoding="async" {img_attrs("owner.jpg")}>
        </div>
        <div class="owner-info reveal" data-delay="1">
            <div class="eyebrow">Meet the owner</div>
            <h2 class="section-title">Hi, I&rsquo;m Travis</h2>
            <p>I&rsquo;ve been running heavy equipment for over 20 years. I started in 2006 working with my father&rsquo;s company, and in 2025 I launched my own: <strong>Travis Frazier Backhoe Service, LLC</strong>.</p>
            <p>Plumbers, electricians, fire line, and pipeline crews count on me to dig it right the first time. I bring precision, safety, and professionalism to every jobsite, and I treat every project like it&rsquo;s my own property.</p>
            <p>Family-owned, locally trusted, and committed to doing the job right &mdash; that&rsquo;s the standard this company is built on.</p>
            <div class="owner-sig">Travis Frazier<small>Owner &amp; Operator</small></div>
        </div>
    </div>
</section>

<section class="final-cta">
    <div class="container reveal">
        <h2>Ready to <em>break ground?</em></h2>
        <p>Fast, reliable, professional excavation. Get your free quote today.</p>
        <div class="hero-actions">
            <a class="btn btn-primary" href="contact.html#quote-form">Request a quote</a>
            <a class="btn btn-ghost" href="tel:{PHONE_TEL}">{icon("phone")} Call {PHONE}</a>
        </div>
    </div>
</section>
<div class="hazard"></div>

{FOOTER}
{LIGHTBOX}""" + END

# ------------------------------------------------------------- SERVICES
services = head("Our Services | " + NAME, page="services.html", desc="Backhoe with operator: excavation, trenching, grading, site prep, and concrete removal across Southern California, the Inland Empire, the desert, and the Bay Area.") + nav("services.html") + page_hero(
    "home1.jpg", "What we offer", "Backhoe &amp; <em>excavation</em> services",
    "Reliable, experienced, and ready for any project &mdash; big or small."
) + f"""
<section class="services">
    <div class="container">
        <div class="service-grid">
{service_cards(5)}
        </div>
    </div>
</section>

<section>
    <div class="container">
        <div class="section-head center reveal">
            <div class="eyebrow">Why us</div>
            <h2 class="section-title">The right crew for the job</h2>
        </div>
        <div class="why-grid">
{why_grid()}
        </div>
    </div>
</section>
<div class="hazard"></div>

{quote_form()}
{FOOTER}""" + END

# -------------------------------------------------------------- GALLERY
gallery = head("Gallery | " + NAME, page="gallery.html", desc="Photos of recent excavation, trenching, grading, and backhoe work in Southern California.") + nav("gallery.html") + page_hero(
    "home3.jpg", "Our work", "Project <em>gallery</em>",
    "A look at recent excavation, trenching, grading, and backhoe work. Tap any photo to enlarge."
) + f"""
<section>
    <div class="container">
        <div class="gallery-wall">
{shot("crew-utility-trench.jpg", "Crew laying conduit in a deep utility trench on an active construction site", "Utility trench", "Conduit going in, crew on site")}
{shot("backhoe-on-site.jpg", "CASE backhoe beside a freshly dug trench", "On the job", "Backhoe working a trench", 1)}
{shot("deep-trench-pipe.jpg", "Deep, straight trench with pipe running along the bottom", "Deep trenching", "Straight walls, clean bottom", 2)}
{shot("backhoe-owner.jpg", "2018 CASE 580 Super N backhoe at a construction site", "The machine", "2018 CASE 580 Super N")}
{shot("trench-open-lot.jpg", "Straight trench dug across an open lot", "Open-lot trench", "Straight and even", 1)}
{shot("trench-with-crew.jpg", "Crew working at the bottom of a long trench", "Trench with crew", "Working to depth", 2)}
{shot("trench-long-run.jpg", "Long straight trench running along a fence line", "Long run", "Straight along the fence line")}
{shot("trench-block-wall.jpg", "Narrow trench dug between a block wall and a fence", "Tight access", "Along a block wall", 1)}
{shot("deep-cut.jpg", "Deep cut next to a concrete structure", "Deep cut", "Beside a concrete structure", 2)}
{shot("home3.jpg", "Deep excavation with utility pipe laid out beside the trench", "Deep excavation", "Utility work, tight site")}
{shot("home1.jpg", "Long straight utility trench dug with a backhoe", "Utility trenching", "Clean, straight lines", 1)}
{shot("home2.jpg", "Backhoe bucket beside a freshly cut trench with crew member working", "Trench layout", "Grade-checked and ready", 2)}
{shot("crew-hat.jpg", "Travis Frazier Backhoe hat with backhoe logo", "Crew gear", "Travis Frazier Backhoe Service LLC")}
        </div>
    </div>
</section>

<section class="final-cta">
    <div class="container reveal">
        <h2>Got a <em>project?</em></h2>
        <p>Send us the details and get a free, no-pressure quote.</p>
        <div class="hero-actions">
            <a class="btn btn-primary" href="contact.html#quote-form">Request a quote</a>
            <a class="btn btn-ghost" href="tel:{PHONE_TEL}">{icon("phone")} {PHONE}</a>
        </div>
    </div>
</section>
<div class="hazard"></div>

{FOOTER}
{LIGHTBOX}""" + END

# -------------------------------------------------------------- CONTACT
contact = head("Contact Us | " + NAME, page="contact.html", desc="Contact Travis Frazier Backhoe Service LLC for backhoe service with operator across Southern California, the Inland Empire, the desert, and the Bay Area.") + nav("contact.html") + page_hero(
    "home2.jpg", "Get in touch", "Let&rsquo;s talk <em>dirt</em>",
    "Reach out for quotes, questions, or project inquiries."
) + f"""
<section>
    <div class="container">
        <div class="contact-grid">
            <div class="contact-card reveal">
                <div class="service-icon">{icon("phone")}</div>
                <h3>Phone</h3>
                <a href="tel:{PHONE_TEL}">{PHONE}</a>
            </div>
            <div class="contact-card reveal" data-delay="1">
                <div class="service-icon">{icon("mail")}</div>
                <h3>Email</h3>
                <a href="mailto:{EMAIL}">{EMAIL}</a>
            </div>
            <div class="contact-card reveal" data-delay="2">
                <div class="service-icon">{icon("pin")}</div>
                <h3>Service area</h3>
                <p>Southern California &amp; beyond</p>
            </div>
        </div>
    </div>
</section>
<div class="hazard"></div>

{quote_form()}

<section class="area">
    <div class="container reveal">
        <div class="eyebrow">Service area</div>
        <h2 class="section-title">We go where the work is</h2>
        <ul class="chips">
{chips()}
        </ul>
        <p class="area-note">Based in Southern California, working across the Inland Empire, Los Angeles, Orange County, the desert, and as far north as San Jose. Not sure if we cover your job? Give us a call &mdash; if the work is there, we&rsquo;ll talk.</p>
    </div>
</section>

{FOOTER}""" + END

for name, content in [("index.html", home), ("services.html", services), ("gallery.html", gallery), ("contact.html", contact)]:
    (OUT / name).write_text(content, encoding="utf-8", newline="\n")
    print("wrote", name, len(content))


# ------------------------------------------------------- sitemap + robots
pages = ["", "services.html", "gallery.html", "contact.html"]
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for pg in pages:
    sitemap.append(f"  <url><loc>{SITE_URL}{pg}</loc></url>")
sitemap.append("</urlset>")
(OUT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8", newline="\n")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8", newline="\n")
print("wrote sitemap.xml, robots.txt")

# ------------------------------------------------------- social share image + favicons
YELLOW = (245, 184, 0)
BLACK = (11, 11, 12)
BOLD = "C:/Windows/Fonts/bahnschrift.ttf"


def font(size, wght=700, wdth=100):
    f = ImageFont.truetype(BOLD, size)
    try:
        f.set_variation_by_axes([wght, wdth])
    except Exception:
        pass
    return f


def og_image():
    W, H = 1200, 630
    photo = Image.open(IMG / "backhoe-owner.jpg").convert("RGB")
    scale = max(W / photo.width, H / photo.height)
    photo = photo.resize((int(photo.width * scale), int(photo.height * scale)), Image.LANCZOS)
    left = (photo.width - W) // 2 + 120
    photo = photo.crop((max(0, left), 0, max(0, left) + W, H)) if photo.width >= W + max(0, left) else photo.crop((0, 0, W, H))
    canvas = photo.convert("RGBA")
    shade = Image.new("RGBA", (W, H))
    sd = ImageDraw.Draw(shade)
    for x in range(W):
        a = int(235 * max(0.0, 1 - x / (W * 0.92)) ** 0.9) + 20
        sd.line([(x, 0), (x, H)], fill=(11, 11, 12, min(a, 240)))
    canvas.alpha_composite(shade)
    d = ImageDraw.Draw(canvas)
    logo = Image.open(IMG / "logo-transparent.png").convert("RGBA")
    lw = 330
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    canvas.alpha_composite(logo, (60, 48))
    d.text((64, 190), "WE DIG IT.", font=font(112), fill=(245, 245, 240))
    d.text((64, 305), "YOU BUILD ON IT.", font=font(112), fill=YELLOW)
    d.text((66, 460), "Backhoe service with operator  |  Southern California & beyond", font=font(31, 500), fill=(220, 220, 214))
    d.text((66, 510), "(951) 440-0647", font=font(44, 700), fill=YELLOW)
    # hazard stripe
    for x in range(-40, W + 40, 44):
        d.polygon([(x, H), (x + 22, H), (x + 44, H - 22), (x + 22, H - 22)], fill=YELLOW)
    canvas.convert("RGB").save(IMG / "og-image.jpg", quality=86, optimize=True)


def favicons():
    def tile(size):
        t = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(t)
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=size // 5, fill=YELLOW)
        f = font(int(size * 0.62), 700, 85)
        bb = d.textbbox((0, 0), "TF", font=f)
        x = (size - (bb[2] - bb[0])) / 2 - bb[0]
        y = (size - (bb[3] - bb[1])) / 2 - bb[1]
        d.text((x, y), "TF", font=f, fill=BLACK)
        return t

    tile(256).resize((32, 32), Image.LANCZOS).save(IMG / "favicon-32.png")
    tile(180).convert("RGBA").save(IMG / "apple-touch-icon.png")
    tile(256).save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])


og_image()
favicons()
print("wrote og-image.jpg and favicons")
