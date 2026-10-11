# Marketing Assets: The LinkedIn Client System

| What | Where | Use |
|---|---|---|
| Book covers (1632x2112) | `images/cover-*.png` | Eden product thumbnails, mockups, Featured section |
| Product heroes (1200x630) | `images/hero-*.png` | Eden product/bundle hero and link-preview image (upload in each product's editor) |
| Single-image posts (1080x1350) | `images/post-01…09-*.png` | Paired with copy in `linkedin-image-posts.md` |
| Document carousels (9 slides) | `carousels/<name>/<name>.pdf` + `slide-NN.png` | Upload the PDF as a LinkedIn document post; PNGs for Instagram |
| Launch post copy | `linkedin-image-posts.md` | 11 posts, keyword map, fulfillment rules, 4-week schedule |
| Extracted post library | `book-post-library.md` | 24 text posts (12 per book), each with a CTA to the right book |

## Rebuild

```
python marketing/build_images.py            # all images + carousels
python the-non-salesy-dm/build/build.py all
python the-linkedin-lead-engine/build/build.py all
```

Images, covers and PDFs share `brand/brand.py` (tokens, fonts, cover layout), so a change there updates every surface.

**Headshot:** the covers and lockups currently use an "MM" monogram because the headshot couldn't be downloaded from this environment. Save a square photo as `brand/headshot.jpg` and re-run the three commands above.

## Eden

Bundle draft: **The LinkedIn Client System**, $79 (Eden shows the $98 combined price). Editor: https://app.eden.so/store/bundles/b8d46277-835b-41f7-ac34-93b88af85870
It can't be published until both $49 products are live. Upload `images/hero-linkedin-client-system-bundle.png` as its image.
