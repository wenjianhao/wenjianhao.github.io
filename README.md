# Wenjian Hao Website (Hugo)

This repository uses the Hugo template from:

- https://github.com/pmichaillat/hugo-website

and is configured for:

- `https://www.wenjianhao.com`

## 1. Local development

Install Hugo (extended):

```bash
brew install hugo
```

Start local server:

```bash
hugo server
```

Open: `http://localhost:1313`

## 2. Main files to edit

- `config.yml`: site title, profile text, menu, social links, base URL
- `content/research.md`: research page
- `content/projects.md`: projects page
- `static/`: static assets (favicon, files, etc.)

## 3. GitHub Pages deployment (free)

This repo includes `.github/workflows/hugo.yml`, which builds and deploys to GitHub Pages on every push to `main`.

In GitHub repo settings:

1. Enable GitHub Actions.
2. Set Pages source to **GitHub Actions**.
3. Push to `main` and wait for the workflow to complete.

## 4. Custom domain

`static/CNAME` is set to:

```txt
www.wenjianhao.com
```

At your DNS provider, set:

- `www` as `CNAME` to `<your-github-username>.github.io`

For the apex (`wenjianhao.com`), either:

- redirect to `www.wenjianhao.com`, or
- use GitHub Pages apex A records (if you prefer no redirect).

## 5. Notes

- This setup avoids paid website builders.
- You only pay for your existing domain registration.
