# Case study: a 40 s foldable-phone spec commercial (Three.js-led)

An unofficial concept ad for a foldable phone, made in the brand's visual language. It is local only, and the end card carries an "unofficial concept, not affiliated" disclaimer. Every frame is code: six Three.js canvases on one HyperFrames seek clock, with HTML/SVG type on top. The music and effects are licensed library audio, and the wallpapers and photos are AI-generated stills.

## Structure
- **Three acts:**
  - dark, 0–17.5: the unfold, the hinge x-ray, the materials macro and the thinness shot;
  - light, 17.5–36: screen sizes, Split View, the camera, the x-ray, the colours;
  - dark, 36–40: a magnetic close into the end card.
- **Handoffs:**
  - 7.0 and 14.0: hard cuts on the downbeat, pixel-registered;
  - 17.5: the edge's glint line opens into a band of light that *is* the light stage;
  - 25.0: a mid-turn cut on a shared function;
  - 32.5: a pixel-matched pose;
  - 35.75: the next scene arrives over the previous one's close-up.
- One shared device module. A fold kinematic `pose({open, bias})` drives both halves, a spine knuckle and the displays, whose textures are built with canvas 2D.

## Process
- **Gauntlet:** every component went through lab → proof render → fresh critic → fix → re-verify → integrate on KEEP. That covered the device, UI, screens, hinge, optics, colours, finale, the type system, images, effects and music.
- **Rounds:** about 70 critic rounds in total, including 6 full-film rounds and 2 fold-specific critics comparing against the reference film.
- **The unfold:** it took 5 builder rounds after the frame-by-frame study (`product-hero-realism.md`).
- **The measured bar at ship:**
  - frozen time 0.2 s;
  - frame 0 a finished composition;
  - no text collisions and type inside title-safe;
  - no near-black frames on the light stage;
  - facts exact, and `hyperframes check` with 0 errors;
  - mix at −30 LUFS with a true peak of −12.9 dBFS.

## What the critics caught that the builders missed
- A mid-swing speed hiccup caused by blending measured keys with a smoothstep.
- The outer display sleeping too early: the director's reading of the reference was wrong.
- Three pure-black frames at an act change, caused by a brightness dip into a lens bore. The fix was to crossfade the next scene in with a small scale settle.
- A camera "jolt" on a magnetic close. Real contact is dead still.
- An end-card push that carried the disclaimer to 31 px from the edge. The fix was to counter-scale the disclaimer.
- A label clamp that fixed one safe-area bug and caused a collision two seconds later.
- Hidden causes behind symptoms: effect gains solved against near-silent music, and a sample with a 33 ms lead-in that landed every hit 2 frames late.

## What the client said, in order
1. "The opening animation, I feel like you didn't nail it… research how they did it." This led to the reference study and the measured curve.
2. "Especially nail the folding animation." This led to screen continuity, the frost, stronger motion blur, dead-still contact and the fold critics.
3. "I feel like you didn't nail the blur." This led to the sharp wallpaper, the frost veil, the frosted cards and a longer shutter.
4. "The music is a bit off… use better music and it should be syncing." This replaced the AI score with human-made library tracks edited to the cut.
5. "Some of the sound effects are not good at all," "the whoosh… too loud". This cut the effects from 14 to 9 real recordings, with quiet air passes on real transitions only.
6. "Small sound effects are missing for all the little things… music −10 %." This added micro sounds on every small mechanical move, each at or below the music's local peak.

See `audio.md` for the resulting sound rules.
