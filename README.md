# Nuvex website concept

Static, dependency-free multi-page website concept. Serve the workspace root over HTTP so root-relative URLs work:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Before launch

- Replace every square-bracket editorial/legal placeholder with information written and approved by Nuvex. Do not publish example projects, claims, figures, portraits, customer marks, or quotations without evidence and permission.
- Complete the legal pages with the actual company, controller, hosting, recipients, retention, and processing details; have the texts reviewed for the real setup.
- Set the real contact, Instagram, LinkedIn, and Discord URLs in `assets/site.js`. Empty social values are intentionally not rendered. Social hosts are restricted to Instagram and LinkedIn; Discord must use `discord.gg`.
- The contact form is a client-side `mailto:` handoff. It does not send data to this website and cannot provide delivery guarantees, server-side validation, rate limiting, or spam protection. A real submission endpoint is a **launch blocker** if the site must collect inquiries directly. Select a provider/backend and configure server-side validation, rate limiting, spam controls, data retention, and privacy disclosures before using one.
- The default `robots.txt` blocks crawling while this concept contains placeholders. Generate production SEO files only after choosing the public HTTPS domain and approving content:

  ```sh
  python3 scripts/generate_seo_files.py --site-url https://your-real-domain.tld --indexable
  ```

  Replace the example origin with the real domain. This writes an indexable `robots.txt` and `sitemap.xml` from the HTML page routes. Do not enable indexing until legal and editorial placeholders are resolved. The non-indexable default command refuses to overwrite an existing sitemap; review/remove it explicitly before creating a preview build.
- No analytics, marketing tags, third-party fonts, embeds, or consent cookies are included. Add a consent manager only if optional storage/access or tracking is later introduced; block those services until valid consent.
- Use only licensed, locally hosted font and image assets. The concept contains no external image assets; the hero graphics are CSS shapes.

## Technical notes

- Semantic HTML, shared responsive CSS, small progressive-enhancement JavaScript, and no runtime dependencies. No database or user-account system exists, so password storage and database backups do not apply to this static concept.
- Run `python3 scripts/check_site.py` to check document language, one H1 per page, unique titles/descriptions, local links, form labels, image alt attributes, external-link safety, selected color contrast, and known release gaps.
- Deploy as static files over HTTPS on a host selected after checking processing location, subprocessors, contract terms, log retention, and backup controls. Configure HTTP-to-HTTPS redirects and security headers at the host/CDN; the local static files cannot guarantee HTTPS or production headers by themselves.
- Recommended host/CDN header baseline: `Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'`, plus `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and a restrictive `Permissions-Policy`. Confirm the policy against the final site before enforcing it. Add HSTS only after HTTPS works everywhere; enable `includeSubDomains` only if every subdomain is HTTPS-ready.
- Use versioned source and host backups for deployment rollback. Assign an owner to review broken links, content/legal changes, dependencies (if introduced), security alerts, and restore procedures on a defined schedule.
- Check navigation, the actual contact delivery path, mobile layouts, keyboard/screen-reader behavior, all relevant contrast states, current link destinations, legal texts, and the published sitemap on a staging domain before launch.
- See [`WEBSITE-CHECKLIST.md`](./WEBSITE-CHECKLIST.md) for the item-by-item implementation status and open release blockers.
