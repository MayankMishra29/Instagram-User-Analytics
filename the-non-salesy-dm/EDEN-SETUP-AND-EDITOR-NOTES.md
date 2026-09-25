# Eden Setup Plan + Editor Notes

## A. Decisions needed before publishing

### 1. Outbound numbers conflict (blocking)
- **In the books (from your VirtUp internal notes):** about 500 LinkedIn connection requests a week across a five-person team, reply rate around 30%. Replies-to-bookings was the bottleneck.
- **On your Eden creator page (public):** "Built VirtUp to 12.5k users in 3 months and a 46% reply rate from 11,466 cold DMs."
- Both can be true (different denominators, periods or channels), but a reader who sees 46% on the store page and 30% in the book will notice. For a book about coherence, that's a trust leak. **Tell me which figures are right and how they relate.** Swapping them is a quick find-and-replace plus a rebuild.
- Where the numbers appear: `complete-edition/00-front-matter.md`, `02-part1-ch01.md`, `08-ch08.md`, `10-part4-ch10.md`, `13-part5-ch14.md`, `15-appendices.md` (Publication Notes); `field-guide/01-field-guide.md`; `authority/01-field-report.md`; `authority/linkedin-launch-posts.md`.

### 2. Facts to verify
- Bio line "business consulting, product marketing and building education businesses" (it came from the ChatGPT draft).
- Naming **VirtUp** publicly, and describing your role as "ran outbound … as part of a 0-to-1 growth sprint." Swap for "an expert marketplace" if you'd rather not name it.
- The "no-code/AI automation niche had the worst reply rate" and "20K+ follower accounts converted poorly" claims (both from your internal VirtUp notes).
- The booking-link-in-a-post story is the "Nino" proof point. The expert isn't named in the books.
- **Automation coherence risk:** your VirtUp stack referenced tools like PhantomBuster/GetSales. The books cite LinkedIn's policy against unauthorized automation and don't describe your tooling. Make sure nothing you say publicly contradicts that.
- LinkedIn policy links in the Publication Notes: open both and confirm they still resolve.

### 3. Stripe
Your store shows **Stripe: not connected**. The paid product can't go live until you connect it at https://app.eden.so/store/storefront. That's a manual step only you can do.

## B. Proposed Eden products (all created as drafts; nothing published without your go-ahead)

| # | Product | Eden kind | Price | What buyers get |
|---|---|---|---|---|
| 1 | **The Non-Salesy DM: Field Guide** | Digital download (chat off) | Free (email captured) | `dist/The-Non-Salesy-DM-Field-Guide.pdf` |
| 2 | **The Non-Salesy DM: Complete Edition + Thread Debugger AI** | Custom AI (chat on) + files | **$49** recommended (see note) | An Eden-native AI that diagnoses any pasted thread (instructions = `system/AI-Thread-Debugger.md`), plus files: the Complete Edition PDF, the Trust Graph Tracker .xlsx, the Field Kit PDF |
| 3 | **Reply Rates Lie: Trust-Led Outbound Field Report** | Digital download (chat off) | Free (email captured) | `dist/Trust-Led-Outbound-Field-Report.pdf` |

**Why the paid tier is a real step up:** the free guide teaches diagnosis. The paid tier adds the full 16-chapter system (targeting, offers, pricing, proposals, rehydration, metrics, the 30-day sprint), a working tracker, and an AI inside Eden that runs the 13-question Debugger on the buyer's own threads. That turns the book into a tool they use daily.

**Pricing note:** $49 matches your Six Ps Offer Builder draft and keeps this as a low-friction entry offer that leads into ThriveXLabs outbound services, which is where the real revenue is. If you want the book to stand on its own as a revenue line, $79–$97 is defensible given the AI and tracker. Don't use a crossed-out "was" price unless you actually sold at that price. A fake anchor contradicts the book.

**Files must be uploaded by you.** Eden's MCP can't upload file bytes, so after I create the drafts you'll add the PDFs/xlsx in each product's Files step.

**Creator page:** products are added automatically on first publish. I'd order them: Field Guide first, the paid Complete Edition second, the Field Report third, above the existing Niche Finder and Starter Kit.

## C. Draft page copy

### 1. Field Guide (free)
- **Headline:** Stop sending the right message at the wrong moment.
- **Subheadline:** A free field guide for consultants, founders and B2B sellers: learn to read a LinkedIn conversation (the buyer's state, their trust question, the risk they're protecting) before you send the next message.
- **Tagline:** Read the buyer before you reply. Free field guide.
- **Body:** Most DMs feel salesy because they answer a trust question the buyer hasn't reached yet, not because of the words. Inside: the Six Trust Gates, the Trust Utility diagnostic, the One-Gate Rule, the Pause Test, the TRUST Loop, a 5-question Debugger Lite, and a 7-day quick start you can run on real threads this week. Built from running LinkedIn outbound at volume, where the replies came easily and the bookings didn't.
- **CTA label:** Get the free guide

### 2. Complete Edition + Thread Debugger AI (paid)
- **Headline:** The trust-led system for turning LinkedIn conversations into clients.
- **Subheadline:** The complete book plus an AI that diagnoses any DM thread: buyer state, open trust gate, weakest risk, the smallest next move, and what not to send.
- **Tagline:** The Non-Salesy DM, Complete Edition + AI Thread Debugger.
- **Body (what's inside):** 16 chapters, from choosing who to message to pricing, proposals and closing · the Six Trust Gates in depth with annotated threads · Five Trust Moves · discovery without interrogation · objections as trust signals · text → voice → Loom → call · rehydrating dormant threads · a daily operating system and honest metrics · a 30-day sprint · the Trust Graph Tracker spreadsheet · the printable Field Kit · the Thread Debugger AI.
- **Refund policy (suggested):** If it isn't useful, email within 14 days for a full refund.
- **CTA label:** Get the complete system

### 3. Field Report (free)
- **Headline:** Reply rates lie. Here's what to measure instead.
- **Subheadline:** A field report for B2B founders and revenue leaders on running LinkedIn outbound at volume, why replies didn't turn into bookings, and the trust-led model that fixes it.
- **CTA label:** Get the field report

## D. What I'll do once you say go
1. Swap in the confirmed numbers and rebuild all PDFs.
2. Create the Thread Debugger Custom AI in your workspace (chat on, memory off, 4 starter prompts) and its product draft.
3. Create the two free digital-download drafts with the page copy above.
4. Send you the editor links so you can upload the files.
5. Publish only when you explicitly say so (Stripe is needed for #2).
