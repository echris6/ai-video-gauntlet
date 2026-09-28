# Product hero realism: making a Three.js device move like the real one

This comes from building a 40 s spec commercial for a foldable phone. The client's main note was: "especially nail the folding animation… it should look realistic". Everything here is measured, not guessed.

## 1. Study the reference motion frame by frame
- Download the brand's own film for **study only**; it never goes into the output. Tile the hero motion at 10 and 30 fps (`ffmpeg -ss A -t D -i ref.mp4 -vf "fps=30,scale=400:-2,tile=7x7"`). Tile your render at the same fps and crop, and compare side by side.
- **Measure the curve.** Estimate the angle per frame from the projected width of the moving part and write keys (seconds after start → degrees). A real foldable unfold ran 0→180° in about 0.8 s, with these keys: `0→0, .08→20, .15→58, .23→82, .31→98, .39→116, .49→140, .59→159, .69→172, .80→180`. It is fastest at 30–60°, slows (dwells) near edge-on and lands softly. That is **not** a smoothstep.
- Interpolate the keys with a **monotone cubic (Fritsch–Carlson) with zero end slopes**. Blending keys with a smoothstep "to soften it" moved the dwell and created a mid-swing hiccup (7.8 → 2.6 → 5.4°/frame), which a critic caught from a per-frame CSV. Have a critic plot °/frame: it must peak once and then dwell, with no second hiccup.
- **Lock the camera** during the motion. A reframe that stops on the contact frame reads as a camera bump. Re-centre the *object* during the swing (the real footage does this), and move any camera reframe to after the landing.

## 2. The screens are half of the realism
The motion matched early on, but it still read as CG until the screen behaviour matched the reference:
- **Before the move:** the outer display shows the *home* screen, reached via a quick unlock. Stagger the unlock: the lock layer lifts and fades out, *then* the home screen scales in from 1.06. A simple crossfade gave a doubled "9:41", which counts as a text collision.
- **During the move:** the outer display **blurs but stays lit** on the moving cover and only sleeps near edge-on. Our first version slept at the lift; that made a 74 % luma drop and a black hole on a black stage.
- **Continuity:** the big display's right half shows *exactly* the layout the small display showed, pixel for pixel. Build the small display's texture as a crop of the big one, so the match holds by construction.
- **The frost:** the newly revealed half keeps a sharp, continuous wallpaper under a white frost veil (about 0.3). The new widgets arrive as frosted, whitened, translucent cards (blur about 40 px, 0.6 opacity, 0.97 scale). These resolve to sharp in about 0.35 s *after* the landing. Blurring the whole half, wallpaper included, read as a smeared photo. Pre-render about 6 blur levels and crossfade between them, so the frost is cheap per frame.

## 3. Motion blur that holds up
- Use deterministic accumulation. Render N sub-frames inside the shutter (`t + ((i+½)/N − ½)·shutter`), average them into a half-float target, and keep every frame a pure function of t.
- **Sub-frames:** 10 left a visible comb on a fast edge (a 3 px ripple of ±20 luma). 24 over the fastest 0.5 s cleaned it up.
- **Shutter:** 180° looked too crisp next to the real footage. About 300° during the fastest swing, easing back to 180°, matched it.
- **Switching:** ramp the shutter from 0 to its full angle over about 6 frames at the window edges, so it never switches on in one frame. Check that no brightness step appears where blur turns on or off.
- **Coverage:** every fast fold in the film needs it. One fold was moving 52 px/frame, another 35 px/frame, and both had no blur.

## 4. Light that tells you the angle
- **Keep ≥60 % of the glass reflections through a fold.** Our builders cut 85 % to hide one-frame flashes, and that removed the main cue that the angle was changing.
- **Fix flashes by widening the light, not dimming it.** A flat polished rail sweeps past a narrow light's mirror angle within one frame. Widen the strip (width 3 → 12 at low power) so the glint builds over about 6 frames. Find the culprit by switching lights off one at a time.
- **Build a black cover to read on a black stage.** Place a broad soft box at the mirror position of the camera about the glass, and let it travel with the angle.
- **Keep magnetic contact dead still.** The real close is pixel-identical for about 17 frames after contact. A camera "jolt" (about 22 px) and a 1.7° rebound read as fake; the fix was no jolt and a rebound of about 0.27°.

## 5. The render plumbing
- **Handoffs:** use shared functions (`applyTurn(u)`, `applyPoseP()`) so both sides of a cut compute identical poses. Check each cut with a mean frame difference against its neighbours.
- **The environment map:** three r181 `PMREMGenerator.fromScene` ignores the render target you pass and leaks a new one every call. Keep one persistent target, copy each result into it and dispose of the fresh one. Feather the soft boxes, or the reflections have hard edges.
- **Supersampling:** render at a 1.5× pixel ratio and let the browser downsample; size the depth-of-field target to the drawing buffer.
- **Fonts:** headless Chrome renders `-apple-system` as Times. Bind the family names with `@font-face` to a local font file that sits next to the CSS (lint rules may reject `../`), and don't redistribute system fonts.
- **Shared-file edits:** while several builders work in parallel, edit shared files through a `.next.js` copy, run `node --check`, then `mv` it into place. One mid-edit syntax error blanked every canvas.
- **Stage colour:** measure the stage colour through the capture→encode path. CSS `#f5f5f7` decoded as `#f3f5f5`, so author the stage colour to what should come out.

## 6. How the review loop found these
- The critic that mattered most compared the render against the reference **frame by frame** and wrote a **per-frame CSV**.
- The director's own first reading of the reference was wrong once: whether the outer display sleeps at the lift. A second, fresh fold critic caught it.
- Always verify the fixes in the next round; don't trust the builder's own numbers. One builder measured a glint at 1.11× its neighbours; the critic, measuring in the film, found 2.1×.
