---
name: business-motion-film
description: Plan, build and quality-check a premium short commercial for a real business (roofing, property, ecommerce, B2B software) using AI-generated footage, code-built motion (HTML/GSAP), selective Three.js and an independent-critic "Gauntlet" loop. Use when asked to make a launch-style / SaaS-style video, business ad, explainer, sample reel or pitch video, or to review and improve one. Encodes motion principles distilled from 28 professional launch films, a quality bar, audio rules and a business-offer playbook.
---

# Business motion film

Make short (15–40s) commercials that look like premium SaaS launch films but sell a real business outcome: explain a service, earn a quote request, follow up on a quote, or refresh an ad. The visuals can be ambitious; the claims must be true.

Read only the reference file your current step needs:

| Step | Read |
|---|---|
| Choosing a vertical, offer, pilot scope, pricing anchors | `references/business-offers.md` |
| Storyboarding and motion design | `references/motion-grammar.md`, then `references/launch-film-notes.md` for concrete moments |
| Building 3D components | `references/three-js-patterns.md`, `templates/component-lab.html`, `templates/projected-overlays.js` |
| A 3D product hero that must move like the real thing (unfolds, closes, reveals) | `references/product-hero-realism.md` |
| Any review round | `references/gauntlet.md`, `references/critic-prompts.md`, `references/quality-bar.md` |
| Music, sound effects, mix | `references/audio.md` |
| A worked example end to end | `references/case-study-alder.md` (calm service film), `references/case-study-duo.md` (Three.js product film) |

## Non-negotiables

1. **Truth.** Never invent testimonials, ratings, completed jobs, diagnoses, savings, warranties or confirmed appointments. A concept film says it is a concept ("Fictional brand · Concept film · AI-generated imagery"). A client film uses the client's approved footage and facts.
2. **Business purpose on mute.** A first-time viewer must be able to say what the business does and what to do next, with the sound off, by the end.
3. **Independent judging.** The builder never grades its own work. Every component and every full cut goes to a fresh critic that sees only the render, the brief and the references (`references/gauntlet.md`).
4. **Deterministic motion.** Every animated state is a pure function of timeline time: no free-running `requestAnimationFrame`, `Date.now()`, unseeded randomness or physics history. Seek to any frame and get the same pixels.
5. **"No bugs" is not "good".** Clean, smooth and error-free versions still get rejected for being basic, empty or slow. Measure (`scripts/`) and judge creatively.

## Workflow

### 1. Brief (15 min)
Write `BRIEF.md`: business, buyer, the viewer's problem, the single action (CTA), what is provably true, available real assets, length, aspect ratios, brand (palette, type), and what must never be claimed. If the user has no real assets, agree it is a labelled concept.

### 2. References
Pick 3–6 moments from `references/launch-film-notes.md` whose *mechanism* fits the story, e.g. a foreground fly-through, a persistent selected object, or a layered exploded view. If the user supplies reference videos, extract frames (`scripts/contact-sheet.sh`) and cite exact timestamps. Borrow mechanisms, never layouts, logos or footage.

### 3. Storyboard before building
One table: time → what the viewer sees → business job of the beat → the transition out, including which object survives it. Rules:
- 12–15 distinct compositions for a 30s film. Vary scale: macro → wide → overhead → UI close-up → type impact.
- The lead subject fills 60–85% of the usable frame in feature beats. No small card floating in a big empty field.
- Every beat has a readable landing, then an accelerating exit. No holds without motion over ~0.6s.
- Name 3 signature transformations you can describe without effect names, e.g. "the inspection photo becomes the report's hero image".
- 3D only where it explains something physical or spatial. Typography and UI stay crisp HTML/SVG.
Get a quick critic pass on the storyboard itself (chronology, business logic, truthfulness).

### 4. Assets
- **AI stills:** generate the key frame first, then animate it with image-to-video. Prompt as a production brief: lens, light, exposure ("bright, airy, nothing crushed to black"), negative space reserved for type, "no people / no text / no logos / no watermark" when needed.
- **AI video:** short (4–5s) clips with restrained camera moves ("a steady gimbal dolly, about 25 cm of travel, preserve the exact geometry, no morphing"). Expect 720p/24fps and interpolate/upscale, which is not native detail. Reject clips whose geometry warps; regenerate rather than hide.
- Keep a generation ledger: model, prompt, seed, job id, accepted window. Never commit API keys.

### 5. Build components in isolation
Each custom component (3D scene, report UI, booking flow, logo mark) gets its own lab page (`templates/component-lab.html`), is rendered to stills plus a short motion proof, and goes through a component Gauntlet round **before** it joins the film.

### 6. Assemble
One root timeline; each scene is a sub-composition; Three.js scenes are rendered from the root seek clock; overlays such as labels, pins and leader lines are positioned from projected 3D anchors every frame (`templates/projected-overlays.js`). Hand objects across scenes at *exact* pixel coordinates, so the last frame of scene A equals the first frame of scene B for the carried object.

### 7. Full-film Gauntlet
Render the whole film. Run `scripts/frozen-time.sh` and `scripts/loudness.sh`. Send to a fresh critic with `references/critic-prompts.md` (full-film prompt). Fix the highest-impact items, re-render, and send to a *new* critic that verifies the previous list item by item. Stop at the quality bar or when gains become cosmetic (usually 3–5 rounds).

### 8. Audio last, but not an afterthought
Follow `references/audio.md`: music matched to the buyer's customer and kept well under the effects (lo-fi or warm acoustic for home services); one soft, rumble-free whoosh per real transition; clean UI sounds only on real actions; per-event levels solved in each effect's band (`scripts/solve-sfx-gains.py`); candidates screened with `scripts/sfx-candidates.py`. Always deliver a music-only fallback, and isolate complaints with it.

### 9. Deliver
Master MP4 (1080p60 for motion work), poster frame, contact sheet, editable source, generation ledger, and a Gauntlet ledger (what each critic found → what changed → measured before/after). State limits honestly: what was measured versus listened to, and sampled versus exhaustive review.

## Working style the clients in this playbook expected
- Plan visibly (storyboard), then build without stopping to ask for approval of every step.
- Report status in one line when working for a long time.
- Show the work: contact sheets, measured numbers, critic verdicts.
