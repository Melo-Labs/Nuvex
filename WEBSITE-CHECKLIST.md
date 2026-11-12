# Nuvex website checklist review

Review of the static concept in this workspace. This is an implementation review, not a legal opinion, hosting audit, penetration test, or formal accessibility certification.

Status:
- **Implemented** — present in the local prototype and checked.
- **Partial** — a starting point exists, but a production condition remains.
- **Blocked** — cannot be completed without real company details or a selected service.
- **Not applicable** — the current static concept does not provide that feature.

## 1. General

- **Implemented:** Pages use consistent semantic structure, a four-link main navigation, shared styles, and a responsive layout.
- **Implemented:** All ten local page routes return HTTP 200 in the local preview. The checker verifies page titles, one H1, local links, and unique descriptions.
- **Implemented:** The site is dependency-free and does not request analytics, third-party fonts, embeds, or remote scripts.
- **Partial:** Regular content, link, security, and restore reviews still need a named owner and schedule.

## 2. Design

- **Implemented:** A single palette and component language are used across desktop and mobile layouts.
- **Implemented:** The selected text/background combinations tested are above 4.5:1 contrast.
- **Implemented:** Buttons, focus states, whitespace, and reduced-motion behavior are defined in the shared stylesheet.
- **Partial:** The current graphics are CSS geometry, not project photography. Add only owned or licensed assets with appropriate descriptions and documented rights.

## 3. Privacy and security

- **Implemented:** No optional tracking, analytics, third-party embed, cookie, or browser storage is present. No consent banner is needed for those absent features.
- **Partial / launch blocker:** Contact is a local `mailto:` handoff, not a server-submitted form. Server-side validation, mail delivery, abuse controls, and spam protection are not implemented.
- **Partial / launch blocker:** HTTPS, redirects, production security headers, hosting logs, backups, and restore testing must be configured and verified with the chosen provider.
- **Not applicable:** There are no user accounts, passwords, database, or admin UI in this static concept.

## 4. German legal requirements

- **Blocked / launch blocker:** Impressum and privacy pages contain placeholders. They are not finished legal notices; provide actual business/controller, hosting, recipient, retention, and processing details and obtain an appropriate legal review.
- **Partial:** The contact page links to the privacy notice and explains that its current form opens the visitor's email client.
- **Implemented:** Social networks and Discord are external links only; no remote content is embedded automatically.
- **Blocked:** Actual contact, Instagram, LinkedIn, and Discord URLs have not been supplied.
- **Not applicable:** There is no shop, checkout, paid promotion, affiliate placement, or user-generated video in the current concept. Reassess if any are added.

## 5. Technical

- **Implemented:** Static HTML, shared CSS, and a small progressive-enhancement script; local page and asset routes were checked.
- **Implemented:** The validator checks form labels, missing image-alt attributes, duplicate IDs, unsafe new-tab links, and selected brand contrast.
- **Not applicable:** There is no database to back up and no server form endpoint to validate.
- **Partial:** Production logging and hosting backups are provider responsibilities; test actual restore procedures before launch.

## 6. Usability

- **Implemented:** The mobile menu opens and closes, supports Escape, and returns focus to its toggle. The form has associated labels and a live status message.
- **Implemented:** At widths 320, 390, 768, 1024, and 1440 CSS pixels, the homepage did not overflow horizontally.
- **Partial:** Screen-reader review and usability testing with representative visitors have not been conducted.

## 7. Content

- **Blocked / launch blocker:** The automated review finds 51 editorial/legal placeholder matches. Replace and review every bracketed instruction before publication; do not treat these as approved marketing copy.
- **Partial:** Do not publish case studies, client marks, statements, or results without evidence and usage permission.

## 8. SEO

- **Implemented:** All ten pages have distinct titles and meta descriptions, clear page headings, readable routes, and internal links.
- **Implemented:** `scripts/generate_seo_files.py` can produce a sitemap and production robots policy after the actual public HTTPS domain is known.
- **Intentionally disabled:** The checked-in `robots.txt` disallows crawling until the placeholders and domain are resolved. Do not deploy it unchanged for a public launch.
- **Partial:** Re-check page descriptions, canonical host, sitemap, and search-console submission on the production domain.

## 9. Maintenance and administration

- **Not applicable:** No CMS, plugin, admin account, or user permissions exist in the static prototype.
- **Partial:** Versioned source provides a rollback point; hosting backup retention, restore tests, and a maintenance owner still need to be established.

## 10. Accessibility

- **Implemented:** German document language, skip link, semantic landmarks, heading hierarchy, keyboard focus indicator, labeled controls, and reduced-motion handling are present.
- **Implemented:** No raster images are currently used. CSS illustrations are labeled or marked decorative.
- **Partial:** The contrast check covers selected theme pairs, not every rendered state. Test all pages with keyboard and assistive technology; this is not a WCAG or BFSG certification.

## Release decision

**Do not publish as a finished company website yet.** The functional static prototype is ready for content and deployment work, but the contact workflow, real social/contact destinations, company-specific legal texts, all editorial placeholders, and production HTTPS/security configuration remain open.
