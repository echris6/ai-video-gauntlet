# Audio

Audio made otherwise strong visuals feel amateur more than anything else. These rules came from direct client rejections.

## Music

- **Match the music to the buyer's customer, not to "tech launch".** An energetic SaaS-launch score was rejected for a roofing/homeowner film. For home services, warm, chill, acoustic-leaning music fits: felt piano, clean or nylon guitar, a soft steady pulse (brushed kit, shaker), ~84–88 BPM, major key.
- **Chill still needs a pulse.** Beatless ambient or very sparse tracks feel sleepy against fast cuts and need heavy gain to be heard.
- **Structure the track to the film.** With generative music (e.g. ElevenLabs composition plans), write one section per scene group with exact durations that sum to the film length. Minimum section length is often 3s, so merge short sections. Ask for "starts immediately on the first beat, no long intro" and "clear resolved final chord at the start of the last section, then natural ring-out".
- **Check the generated track's loudness over time** (short-term per second). Reject tracks with a near-silent intro, dips under key scenes, or decay seconds before the logo. Regenerate with a different seed; some styles (e.g. tremolo electric guitar + Rhodes) repeatedly produced slow intros.
- **Avoid:** vocals/humming, lo-fi vinyl crackle, ukulele/whistling corporate stock, trailer hits, EDM drops, risers, anything "epic".
- **Deliver 2–3 options** cut to the same picture at identical integrated loudness, so the client compares music, not volume.

## Sound effects

What the reference launch films do (audio analysis of 14 motion-first films): the music carries the sound design, with punchy rhythmic beds and cuts on beats. Effects are whooshes, pitched sweeps, sub hits on hard cuts, and crisp UI/product clicks. That density suits punchy tech tracks. **Copying it onto a calm score was rejected** as "too loud… not clean… annoying throughout".

What a client finally approved for a calm home-services film, after eight rounds:
- **One short, soft, rumble-free whoosh on every real transition:** scene changes, visible wipes, and the headline slam. Never long, boomy "air/wind" whooshes. Choose whooshes with little energy below 150 Hz and a gentle ~80–400 ms rise. The rejected ones had 35–83% of their energy below 150 Hz and sounded like a repeated boom.
- **Small clean UI sounds only on real actions:** clicks on cursor clicks, pops on pins/badges, light ticks on labels, a check when something seats, one soft chime on confirmation, tiny taps when a logo locks together.
- **3D reveals get a musical accent:** a clean rising three-note pluck as roof layers lift apart, and soft wooden taps as new tiles land. Pitch-shift tonal accents to the score's key.
- Music chosen: lo-fi (Rhodes + soft dusty drums), about 30% quieter than first mixed, so effects read clearly.

Rules:
1. **Clean sources.** A standard library (Mixkit Sound Effects Free License, HyperFrames' bundled SFX) with a gentle high-pass (~150–220 Hz), low-pass (~9–11 kHz) and click-free fades. Loosely prompted AI effects and synthesized sine sweeps/ticks were rejected. Targeted AI effects work when you **generate several candidates and reject by analysis** (`scripts/sfx-candidates.py`): drop anything boomy (>50% below 150 Hz), hissy or clicky (>40% above 6 kHz), or noise-like (it will read as a whoosh).
2. **Set levels per event, in each effect's own frequency band,** against a music-only render (`scripts/solve-sfx-gains.py`). Target about +3–4 dB in-band, and cap the ear-sensitive 2–8 kHz lift at ~4 dB. Full-band loudness is useless here: effects barely move it, yet ticks can spike 12–17 dB at 2–8 kHz and sound annoying.
3. **Keep repeated sounds consistent.** When the solver collapses a gain because the music is momentarily quiet, override it to match the sound's other occurrences. Soften sounds that cluster within ~0.15s (×0.6) so they don't stack.
4. **Isolate complaints with a music-only render.** When the client says "that whoosh", first check whether it's in the music (brushed snares and risers sound like whooshes). Ask them to play the music-only version at that moment, then fix the right layer.
5. **Change one thing per round and name it by timestamp.** The window between "I can't hear anything" and "I want to break my laptop" is a few dB.
6. **Always deliver a music-only fallback,** and keep previous versions in an `older versions/` folder.
7. If the music resolves on the logo, don't add a separate musical sting (key clashes), and don't cut the music out before the logo on calm pieces.

## Mix & master

- Mix and render as part of the composition (per-track volume, automation for dips under dense reading moments).
- **Loudness:** reference launch films master around −14 LUFS (some at −7 to −10). The approved calm film landed at −19 LUFS integrated once the client lowered the music 30%, with effects clearly audible on top. A dense effects layer at −14 was rejected as too loud. True peak ≤ −1 dBFS with a limiter. Copy the video stream untouched; AAC 256k.
- Measure with `scripts/loudness.sh`. State honestly whether anyone actually listened, since measurements can't judge taste.

## Energetic product films (from a 40 s Three.js product spec, 2026-09)

- **Library music beat the AI scores.** The client called two rounds of generated "brand-style" scores "a bit off". A human-made library track, **edited to picture**, landed well. Mixkit stock music is reachable at `https://assets.mixkit.co/music/<id>/<id>.mp3` (IDs come from the `data-audio-player-preview-url-value` attributes on the tag pages). Check the licence and credit the tracks.
- **Edit it like a music editor:**
  - time-stretch to a tempo where every cut falls on a beat (120 BPM puts cuts at x.0 and x.5);
  - measure the real onset at each cut and stretch ≤0.5 % between cuts (a generic beat-warp locked onto the off-beat);
  - a sparse or filtered intro, with the groove arriving on the hero moment;
  - a dead stop (about 0.4 s) and the track's own drop on the biggest cut;
  - the track's own final hit spliced on the end card, with equal-power crossfades on bar lines;
  - a 5 ms fade-in, because a full-level first sample clicks.
- **Make the drop land.** A drop that measured only +0.2 LU needed two things: a 40→300 Hz high-pass build over the 2 s before it, and a −2.5 dB dip applied **after** the bus compressors (before them, the compressors flatten it out). Result: +2.7 LU, and the bass +9 dB into the drop.
- **Brand study, for grammar only.** The reference brand film measured about 124 BPM, four-on-the-floor, with flat and confident density, a restrained 2–5 kHz, dead stops and a button ending. Don't name brands or artists in generator prompts; they get rejected.
- **Levels the client approved:**
  - music at about −30 LUFS (he asked for 10 % less than −29);
  - whooshes as a soft "air pass" at about +2–3 dB in-band, raising short-term loudness ≤0.5 LU. A bundled whoosh at +7 dB was "too loud" and unprofessional;
  - micro sounds on **every small mechanical move** (screws backing out, parts re-seating, detents, panes docking): real recordings, each peaking **at or below** the local music peak.
- **Mixer guards** (`scripts/offline-mix.py`):
  - **Level floors:** over a dead stop or a sparse intro, "+N dB over the music" makes an effect inaudible. A per-event floor on the reference level fixes it.
  - **A high-frequency floor:** the 2–8 kHz cap is measured against a floor, or a bass-only intro lets nothing through.
  - **A peak cap:** no effect may peak more than about 6 dB over the local music peak (8 dB for a signature hit). Without it, a key-press thock spiked to −2.8 dBFS in a −29 LUFS mix.
  - **Report "body" as well:** the 150 ms in-band RMS lift, verified on the decoded file against a music-only render. The 50 ms peak alone over-reported a 0.15 s thock by 8 dB.
- **Synthesised thocks were rejected** as "a pitched tom" or not professional. Layered real recordings worked, e.g. a laptop key press plus a soft body punch, about 100 ms long.
