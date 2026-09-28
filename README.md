# Motion Video Kit

A Claude Code skill (also usable as plain context for any LLM) for making **premium, launch-style commercials for real businesses** with AI-generated footage, code-built motion (HTML/GSAP), selective Three.js, and an independent-critic quality loop.

It packages what was learned from studying 28 professional SaaS launch films and from building two full sample commercials through dozens of rounds of independent critique: a calm service film, and a 40 s Three.js product spec ad for a foldable phone in which every frame is code:

- **The Gauntlet loop:** builder ≠ judge, fresh critics on the actual render, item-by-item verification, and a ledger. Includes ready-to-use critic prompts.
- **Motion grammar:** six rules and a catalog of 16 reusable mechanisms, plus notes on all 28 reference films (links to the originals; no footage redistributed).
- **Quality bar:** measurable checks (frozen time, loudness, contrast, brand colour) and the visual and business criteria clients actually enforce.
- **Audio rules:** matching music to the buyer's customer, sparse clean sound effects, mix targets.
- **Business playbook:** verticals with buying evidence and price anchors, a pilot-offer template, honesty rules.
- **Three.js patterns:** deterministic, seekable scenes; exploded layers with projected callouts; photos pinned in 3D context; animated option patches; a realism checklist.
- **Product hero realism:** how to match a real device's motion frame by frame (measured angle keys, a monotone cubic, locked camera), screen continuity and frost, deterministic accumulation motion blur, and lights that reveal the angle without flashing.
- **Scripts and templates:** frozen-time and loudness measurement, contact sheets, sound-effect softening, an isolated component lab, and a projected-overlay module.

## Install (Claude Code)

```sh
git clone https://github.com/echris6/motion-video-kit.git
cp -r motion-video-kit/business-motion-film ~/.claude/skills/        # all projects
# or, per project:
cp -r motion-video-kit/business-motion-film <your-project>/.claude/skills/
```

Then ask for a business commercial, sample reel or explainer, or for a review of one, and the skill loads. It works best with [HyperFrames](https://hyperframes.heygen.com) for rendering, but the principles, prompts and checks are renderer-agnostic.

**Other LLMs:** paste `business-motion-film/SKILL.md` plus the reference files you need into the context.

## Requirements for the scripts

`ffmpeg`/`ffprobe` (with the `ebur128` filter). Optional: Node 22+ and HyperFrames for the lab template.

## Layout

```
business-motion-film/
  SKILL.md                      workflow + non-negotiables
  references/
    gauntlet.md                 the review loop, with real findings
    critic-prompts.md           component / full-film / verification / storyboard prompts
    motion-grammar.md           6 rules + mechanism catalog + pacing numbers
    launch-film-notes.md        notes on 28 reference films (links only)
    quality-bar.md              measured + visual + business ship criteria
    audio.md                    music, SFX, mix
    business-offers.md          verticals, evidence, price anchors, pilot offer
    three-js-patterns.md        render contract, patterns, realism checklist
    case-study-alder.md         a full worked example (calm service film)
    product-hero-realism.md     making a 3D device move like the real one
    case-study-duo.md           a Three.js product film, round by round
  scripts/                      frozen-time, loudness, contact-sheet, soften-sfx, sfx-candidates, solve-sfx-gains, offline-mix
  templates/                    component-lab.html, projected-overlays.js
```

## Notes

- Reference films belong to their owners. This repo contains only original written analysis and links. Reach numbers quoted from studio portfolios are studio claims.
- Market prices are a September 2026 snapshot of public listings; re-verify before quoting.
- Never present AI-generated imagery as a real customer, job or result. The skill enforces labelling.

## License

MIT for the text, scripts and templates in this repo.
