# offline-mix.py: mix a silent picture render with a music score and per-event sound effects, levelled in each effect's own band.
# Project layout it expects (next to this script's parent, i.e. <project>/tools/offline-mix.py):
#   assets/music/<score>.mp3      assets/sfx/<name>.mp3
#   assets/sfx/plan.json          [[name, film_time_s, target_dB_over_music_in_band, note, (floor_dBFS), (peak_cap_dB)], ...]
# Usage: python3 tools/offline-mix.py renders/picture.mp4 renders/out.mp4 --score my-score.mp3 [--no-sfx] [--music-lufs -29.9]
#        [--ring-db 0] [--hf-cap 4] [--mfloor -50] [--hfloor -50] [--pkcap 6] [--pkfloor -20] [--drop-dip -2.5] [--write-events]
# The music chain (low shelf, two compressors, high shelf, loudness levelling), the post-chain dip before the drop (14.0-17.1 s:
# edit for your film) and the ring-out lift after 37.2 s are film-specific defaults; change them to your cut points.
# Needs: ffmpeg (ebur128), numpy, scipy. Writes review/mix-<out>.txt with per-event in-band lift, 150 ms body and 2-8 kHz lift.
#!/usr/bin/env python3
"""iPhone Duo audio: offline stem mix, measured per effect (the client's rule: subtle energetic bed ~-29 LUFS, each effect
set in its own band a few dB over that quiet bed, never a 2-8 kHz spike).

Usage: python3 tools/mix.py <picture.mp4> <out.mp4> [--score score-duo-a2-beat.mp3] [--no-sfx] [--music-lufs -29]
Reads assets/sfx/plan.json: [[name, film_time, target_dB_over_bed_in_band, note], ...]
Writes: out.mp4 (picture copied untouched + AAC 256k), review/mix-<stem>.txt (per-event report), assets/sfx/events.json
(the solved linear gains, relative to the music's build gain, so build.py's HTML audio matches the delivered mix closely).

Music chain (approved on AURELIN v4): -3 dB low shelf at 90 Hz, 3:1 compression, -3 dB high shelf at 5 kHz, then gain to
the target integrated loudness; 1.2 s fade at the end. Effects: each placed at its time, its gain solved so its 50 ms in-band
peak sits target dB over the music's in-band 50 ms peak in the same window; then 2-8 kHz lift capped at HF_CAP dB.
"""
import json, subprocess, sys, re, os
import numpy as np
from scipy.signal import butter, sosfilt
from pathlib import Path
P = Path(__file__).resolve().parents[1]; SR = 48000
args = sys.argv[1:]; pic, out = args[0], args[1]
opt = lambda k, d: args[args.index(k) + 1] if k in args else d
score = opt('--score', 'score-duo-a2-beat.mp3'); target_lufs = float(opt('--music-lufs', '-29.9')); HF_CAP = float(opt('--hf-cap', '4'))  # the client's rule: 2-8 kHz lift <= ~4 dB
no_sfx = '--no-sfx' in args
def load(p): return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(p), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32).reshape(-1, 2).copy()
def lufs(x):
    tmp = P / 'renders/_lufs.wav'; write(tmp, x)
    e = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(tmp), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1]), float((re.findall(r'Peak:\s+(-?[\d.]+) dBFS', e) or ['nan'])[-1]), float((re.findall(r'LRA:\s+([\d.]+) LU', e) or ['nan'])[-1])
def write(p, x): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', str(p)], input=np.clip(x, -1, 1).astype(np.float32).tobytes(), check=True)
def pk(y): h = int(.05 * SR); return max(10 * np.log10((y[i:i + h] ** 2).mean() + 1e-12) for i in range(0, max(1, len(y) - h), h // 2))
N = int(40.0 * SR)
# ---- music stem ----
raw = P / 'renders/_music_chain.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(P / 'assets/music' / score), '-af',
                'lowshelf=f=90:g=-3,acompressor=threshold=-24dB:ratio=3:attack=4:release=140:knee=6:makeup=1,highshelf=f=5000:g=-3,acompressor=threshold=-30dB:ratio=2.5:attack=1:release=90:knee=4',  # 2nd stage: music-critic-1 (A2 intro spikes 19/73 -> 0/73 windows >4.5 dB)
                '-ar', str(SR), '-ac', '2', '-t', '40', str(raw)], check=True)
mus = load(raw)[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
L0 = lufs(mus)[0]; mg = 10 ** ((target_lufs - L0) / 20); mus *= mg
fade = np.ones(N, np.float32); f0 = int((40 - 1.2) * SR); fade[f0:] = np.linspace(1, 0, N - f0) ** 1.5; mus *= fade[:, None]
RING = float(opt('--ring-db', '7'))   # music-critic-1: the ring-out after the 37.0 resolve sat 15-25 dB under the bed; lift it (100 ms ramp)
r0 = int(37.2 * SR); ramp = np.ones(N, np.float32); ramp[r0:] = 10 ** (RING / 20); ramp[r0:r0 + int(.1 * SR)] = np.linspace(1, 10 ** (RING / 20), int(.1 * SR)); mus *= ramp[:, None]
# the build into the 17.5 drop: a post-chain dip (the compressors flattened the pre-chain one; audio-critic-3: +0.2 LU → ~+2 LU into the drop)
DIP = float(opt('--drop-dip', '-2.5'))
if DIP:
    d0, d1, rr = int(14.0 * SR), int(17.1 * SR), int(.01 * SR); dg = np.ones(N, np.float32); lv = 10 ** (DIP / 20)
    dg[d0:d1] = lv; dg[d0:d0 + rr] = np.linspace(1, lv, rr); dg[d1 - rr:d1] = np.linspace(lv, 1, rr); mus *= dg[:, None]
mono_m = mus.mean(1)
# ---- effects ----
fx = np.zeros_like(mus); rep = []; ev_out = []
plan = [] if no_sfx else json.loads((P / 'assets/sfx/plan.json').read_text())
HB = butter(4, [2000, 8000], btype='band', fs=SR, output='sos')
PKCAP = float(opt('--pkcap', '6')); PKFLOOR = float(opt('--pkfloor', '-20')); MFLOOR = float(opt('--mfloor', '-50')); HFLOOR = float(opt('--hfloor', '-50'))
build_gain = float(os.environ.get('DUO_SCORE_GAIN', '0.35'))
for ev in plan:
    name, t, target, note = ev[:4]; floor = ev[4] if len(ev) > 4 else MFLOOR   # optional per-event floor (dBFS in-band peak)
    pkc = ev[5] if len(ev) > 5 else PKCAP                                     # optional per-event peak cap (dB over the local music peak)
    s = load(P / 'assets/sfx' / f'{name}.mp3'); m1 = s.mean(1)
    F = np.abs(np.fft.rfft(m1 * np.hanning(len(m1)))) ** 2; f = np.fft.rfftfreq(len(m1), 1 / SR); c = np.cumsum(F) / F.sum()
    lo = max(f[np.searchsorted(c, .2)], 60); hi = min(max(f[np.searchsorted(c, .8)], lo * 2), SR / 2 - 500); sos = butter(4, [lo, hi], btype='band', fs=SR, output='sos')
    i = int(t * SR); W = min(len(m1), int(.4 * SR)); seg_m = mono_m[max(0, i - SR // 2):i + W + SR // 2]
    mpk = pk(sosfilt(sos, seg_m)[SR // 2:SR // 2 + W]); epk = pk(sosfilt(sos, m1)[:W])
    # floors: over near-silent music (a dead stop, a sparse intro) "+N dB over the music" would make an effect inaudible, so the
    # reference never drops below MFLOOR in-band, and the 2-8 kHz cap is measured against at least HFLOOR (Duo, lib cues)
    mpk_ref = max(mpk, floor)
    if os.environ.get("MIXDBG"): print(f"DBG {t:6.2f} mpk {mpk:.1f} hf {pk(sosfilt(HB, seg_m)[SR // 2:SR // 2 + W]):.1f}")
    g = 10 ** ((mpk_ref + target - epk) / 20)
    # 2-8 kHz cap: the lift of (music + effect) over music in the ear-sensitive band
    def hf_lift(g):
        a = seg_m.copy(); k = min(W, len(seg_m) - SR // 2); a[SR // 2:SR // 2 + k] += g * m1[:k]
        return pk(sosfilt(HB, a)[SR // 2:SR // 2 + W]) - max(pk(sosfilt(HB, seg_m)[SR // 2:SR // 2 + W]), HFLOOR)
    hl = hf_lift(g)
    while hl > HF_CAP and g > 1e-4: g *= .85; hl = hf_lift(g)
    # peak cap (Duo, client: "too loud"): the effect's sample peak may sit at most PKCAP dB over the music's local peak (floored)
    k0 = min(len(m1), len(seg_m) - SR // 2); mloc = max(20 * np.log10(np.abs(seg_m[SR // 2:SR // 2 + W]).max() + 1e-9), PKFLOOR)
    while 20 * np.log10(g * np.abs(m1[:k0]).max() + 1e-9) > mloc + pkc and g > 1e-4: g *= .9
    j = min(N, i + len(s)); fx[i:j] += g * s[:j - i]
    e = np.zeros_like(seg_m); k = min(len(m1), len(seg_m) - SR // 2); e[SR // 2:SR // 2 + k] = g * m1[:k]
    inb = pk(sosfilt(sos, seg_m + e)[SR // 2:SR // 2 + W]) - mpk
    # film-critic-3: also report BODY, the 150 ms in-band RMS of (music + effect) over music alone (what a listener hears as weight)
    b0, b1 = SR // 2, SR // 2 + int(.15 * SR); rms = lambda y: 10 * np.log10((y[b0:b1] ** 2).mean() + 1e-12)
    body = rms(sosfilt(sos, seg_m + e)) - rms(sosfilt(sos, seg_m))
    rep.append(f'{t:6.2f} {name:14s} band {int(lo):5d}-{int(hi):5d} Hz  target +{target:.0f}  in-band lift {inb:+5.1f} dB  body {body:+5.1f} dB  2-8k lift {hl:+5.1f} dB  gain {g:.4f}  {note}')
    ev_out.append([name, t, round(len(s) / SR + .05, 3), round(float(g) / mg * build_gain, 4)])
mix = mus + fx
peak = np.abs(mix).max(); lim = 10 ** (-1.5 / 20)
if peak > lim: mix *= lim / peak  # safety only; the mix is quiet by design
wav = P / f'renders/_mix-{Path(out).stem}.wav'; write(wav, mix)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', pic, '-i', str(wav), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', out], check=True)
Lm, _, _ = lufs(mus); Lx, tp, lra = lufs(mix)
hdr = f'score {score}: music-only {Lm:.1f} LUFS (chain gain {20*np.log10(mg):+.1f} dB); mix {Lx:.1f} LUFS, LRA {lra}, true peak {tp} dBFS; {len(plan)} effects'
(P / 'review').mkdir(exist_ok=True); (P / f'review/mix-{Path(out).stem}.txt').write_text(hdr + '\n' + '\n'.join(rep) + '\n')
if plan and '--write-events' in args: (P / 'assets/sfx/events.json').write_text(json.dumps(ev_out, indent=0))
print(hdr); print('\n'.join(rep))
