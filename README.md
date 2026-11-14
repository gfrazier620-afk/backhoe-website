# Travis Frazier Backhoe Company LLC

A modern, mobile-friendly website for a Southern California backhoe and excavation company, built by [Dry Lightning Labs](https://github.com/gfrazier620-afk) as a gift for the owner.

**Live preview:** https://gfrazier620-afk.github.io/backhoe-website/

![Home page screenshot](docs/screenshot.png)

## Pages

- **Home**: full-screen hero, services, how it works, recent work, and meet the owner
- **Services**: all six services, why choose us, and a quote form
- **Gallery**: photos of the equipment and work, with a click-to-enlarge viewer
- **Contact**: phone, email, service area, and the quote form

## Tech

Plain HTML, CSS, and JavaScript. There is no build step. Fonts (Oswald and Inter) load from Google Fonts. The quote form opens an email to the company with the details filled in.

```
index.html  services.html  gallery.html  contact.html
assets/
  css/styles.css  js/main.js  img/
```

To run it locally, open `index.html` in a browser, or serve the folder:

```bash
python -m http.server 8000
```

## Hosting

The live preview is served by GitHub Pages from the `main` branch. Pushing to `main` redeploys it.

## Status

This was my first website design project, redesigned in November 2026. A custom domain is planned.
