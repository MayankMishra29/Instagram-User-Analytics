# The Non-Salesy DM: all editions

| Version | Purpose | Output |
|---|---|---|
| Field Guide (free) | Lead magnet on Eden, captures emails | `dist/The-Non-Salesy-DM-Field-Guide.pdf` |
| Complete Edition + Implementation System (paid) | Eden store product | `dist/The-Non-Salesy-DM-Complete-Edition.pdf`, `dist/The-Non-Salesy-DM-Field-Kit.pdf`, `system/Trust-Graph-Tracker.xlsx`, `system/AI-Thread-Debugger.md` |
| Reply Rates Lie field report (free) | Authority asset for ThriveXLabs B2B outbound | `dist/Trust-Led-Outbound-Field-Report.pdf`, `authority/linkedin-launch-posts.md` |

Sources are Markdown in `complete-edition/`, `field-guide/`, `authority/` and `system/field-kit/`.
Rebuild: `python build/build.py all` (needs markdown, qrcode, pypdf, playwright) and `python build/make_tracker.py` (openpyxl).
Every PDF has a QR code and a link to https://revops.eden.so/.
Open decisions: see `EDEN-SETUP-AND-EDITOR-NOTES.md`.
