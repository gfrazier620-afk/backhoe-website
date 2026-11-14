# Travis Frazier Backhoe Company LLC

A website for a Southern California backhoe and excavation company, built by [Dry Lightning Labs](https://github.com/gfrazier620-afk) as a gift for the owner.

**Live preview:** https://gfrazier620-afk.github.io/backhoe-website/

![Home page screenshot](docs/screenshot.png)

## Pages

- **Home**: hero, featured services, and why customers choose the company
- **Services**: excavation, trenching, grading, and more
- **Gallery**: photos of the equipment and work
- **Contact**: how to reach the company and request a quote

## Tech

Plain HTML, CSS, and JavaScript. There is no build step and there are no dependencies.

```
index.html  services.html  gallery.html  contact.html
assets/
  css/  img/  js/
```

To run it locally, open `index.html` in a browser, or serve the folder:

```bash
python -m http.server 8000
```

## Hosting

The live preview is served by GitHub Pages from the `main` branch. Pushing to `main` redeploys it.

## Status

This was my first website design project. A custom domain is planned.
