# Audit — gameformative.com as it stands

*Measured 2026-09-25 19:13 UTC with `curl`, `dig` and `whois` from Hungary. The audit slot of the
method measures the current state of the thing being rebuilt; here there is no site yet, and the
audit records that precisely.*

## The domain

| Check | Result |
|---|---|
| Registration | registered **2026-09-25** — the registry (Verisign) records `2026-09-25T18:19:23Z`, the registrar's own record `2026-09-25T13:19:23Z` (five hours apart, both labelled UTC — recorded as read, not reconciled) |
| Registrar | GoDaddy.com, LLC; expiry 2027-09-25 |
| Status | clientDelete/Renew/Transfer/UpdateProhibited — the registrar's standard locks |
| Name servers | `ns1.vercel-dns.com`, `ns2.vercel-dns.com` |
| A records | `64.29.17.130`, `216.198.79.130` (Vercel) |

## What the domain serves

| Request | Status | Time to first byte | Body |
|---|---|---|---|
| `https://gameformative.com/` | **404** | 0.219 s | 107 bytes, `text/plain` |
| `https://www.gameformative.com/` | **404** | 0.614 s | 107 bytes |
| `http://gameformative.com/` | 404 after redirect to https | 1.558 s | 107 bytes |
| `https://gameformative.com/robots.txt` | 404 | — | — |

Response headers: `server: Vercel`, `x-vercel-error: DEPLOYMENT_NOT_FOUND`, HSTS
`max-age=63072000`, edge `fra1`. The body reads "The deployment could not be found on Vercel."

## What that means

- The domain is **live on Vercel's DNS with no deployment behind it**: the hosting account is
  connected, nothing is published. There is no existing content, brand, audience, analytics or SEO
  to preserve, and no URL that has ever served a page — so no redirects are owed.
- The hosting choice is already half-made (Vercel). `11-architecture.md` ADR-01 treats it as the
  proposed host for the real build rather than an assumption.
- There is no brand to inherit: the name is the only given. The identity in `05-design.md` is new,
  derived from the research.
