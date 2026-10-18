"""Original, gentle 'café parisien' music bed: light waltz (3/4), musette-style reed melody,
pizzicato bass, soft brushes. Usage: python3 bed_cafe.py out.wav [seconds]"""
import sys, wave, numpy as np
SR = 44100
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 34.0
BPM = 138; beat = 60 / BPM; N = int(SR * DUR)
mix = np.zeros(N); rng = np.random.default_rng(1900)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def add(sig, start):
    i = int(start * SR)
    if i >= N: return
    j = min(N, i + len(sig)); mix[i:j] += sig[: j - i]
def adsr(n, a, d, s, r):
    a, d, r = int(a * SR), int(d * SR), int(r * SR); h = max(n - a - d - r, 0)
    e = np.concatenate([np.linspace(0, 1, max(a,1)), np.linspace(1, s, max(d,1)), np.full(h, s), np.linspace(s, 0, max(r,1))])
    return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))
def reed(m, dur):
    # musette: two slightly detuned reeds, odd-harmonic rich, gentle vibrato
    t = np.arange(int(dur * SR)) / SR
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t)
    out = np.zeros_like(t)
    for det in (-0.006, 0.0, 0.007):
        ph = 2 * np.pi * hz(m) * (1 + det) * t * vib
        out += np.sin(ph) + 0.35 * np.sin(3 * ph) + 0.15 * np.sin(5 * ph) + 0.25 * np.sin(2 * ph)
    return out / 6 * adsr(len(t), 0.03, 0.1, 0.8, 0.08)
def pluck(m, dur, bright=0.5):
    t = np.arange(int(dur * SR)) / SR
    s = np.sin(2 * np.pi * hz(m) * t) + bright * np.sin(4 * np.pi * hz(m) * t) * np.exp(-t * 8)
    return s * np.exp(-t * 4.5)
# chords (bass root, chord tones) in A minor / C major, 2 bars each of 3 beats
prog = [(45, [57, 60, 64]), (40, [56, 59, 64]), (45, [57, 60, 64]), (50, [57, 62, 65]),
        (43, [55, 59, 62]), (48, [55, 60, 64]), (40, [56, 59, 62]), (45, [57, 60, 64])]
# melody per bar: (midi, beats) — original line
mel = [[(76,1),(74,1),(72,1)], [(71,2),(68,1)], [(69,1),(72,1),(76,1)], [(77,2),(74,1)],
       [(74,1),(72,1),(71,1)], [(72,2),(76,1)], [(74,1),(71,1),(68,1)], [(69,3)]]
bar = 3 * beat; t0 = 0.4
nbars = int((DUR - t0) / bar)
for b in range(nbars):
    root, chord = prog[b % 8]; tb = t0 + b * bar
    add(pluck(root - 12, beat * 1.4, 0.3) * 0.5, tb)                  # bass on 1
    for k in (1, 2):                                                   # "pah pah" chords on 2 and 3
        for m in chord:
            add(pluck(m, beat * 0.7, 0.6) * 0.09, tb + k * beat)
    tt = tb
    for m, nb in mel[b % 8]:
        if b >= 2:  # melody enters after two bars
            add(reed(m, nb * beat * 0.95) * 0.22, tt)
        tt += nb * beat
    for k in range(3):                                                 # soft brushes
        n = int(0.09 * SR)
        add(rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 35) * (0.035 if k else 0.05), tb + k * beat)
# gentle room echo
echo = np.zeros_like(mix); dly = int(0.21 * SR); echo[dly:] = mix[:-dly] * 0.22; mix += echo
mix = mix / np.max(np.abs(mix)) * 0.89
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
