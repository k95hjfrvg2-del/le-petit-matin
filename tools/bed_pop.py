"""Original sunny French-pop intro ("good vibes", bobo/indie): electric piano, finger bass, light
drums, tambourine, koto hook and glockenspiel, played with the GeneralUser GS soundfont.
Usage: python3 bed_pop.py <GeneralUser-GS.sf2> out.wav [seconds]
Layout at 120 BPM (one bar = 2 s): 0-2 s intro (keys + tambourine + drum fill), 2-8 s koto hook,
resolving at 8 s, then a lighter groove (no melody) to sit under the voice until the end."""
import sys, wave, numpy as np, tinysoundfont

SF, OUT = sys.argv[1], sys.argv[2]
DUR = float(sys.argv[3]) if len(sys.argv) > 3 else 34.0
SR = 44100; BPM = 120; B = 60 / BPM; BAR = 4 * B
syn = tinysoundfont.Synth(samplerate=SR, gain=-3)
sf = syn.sfload(SF)
EP, BASS, WHIS, GLOCK, GTR, KOTO, SHAKU, DR = 0, 1, 2, 3, 4, 5, 6, 9
syn.program_select(EP, sf, 0, 4)        # Electric Piano 1
syn.program_select(BASS, sf, 0, 33)     # Fingered bass
syn.program_select(WHIS, sf, 0, 78)     # Whistle
syn.program_select(GLOCK, sf, 0, 9)     # Glockenspiel
syn.program_select(GTR, sf, 0, 25)      # Steel-string guitar (muted strums)
syn.program_select(KOTO, sf, 0, 107)    # Koto
syn.program_select(SHAKU, sf, 0, 77)    # Shakuhachi
syn.program_select(DR, sf, 128, 0, is_drums=True)

ev = []  # (time, kind, chan, key, vel)
def note(t, ch, k, dur, vel):
    ev.append((t, 1, ch, k, vel)); ev.append((t + dur, 0, ch, k, 0))
def hit(t, k, vel): note(t, DR, k, 0.1, vel)

# Dmaj7 - Bm7 - Em7 - A7sus/A7  (I - vi - ii - V)
chords = [([62, 66, 69, 73], 38), ([59, 62, 66, 69], 35), ([64, 67, 71, 74], 40), ([64, 67, 69, 73], 33)]
nbars = int(DUR / BAR) + 1
for b in range(nbars):
    t0 = b * BAR
    tones, root = chords[b % 4]
    full = 1 <= b <= 3          # hook bars
    soft = b >= 4               # under the voice
    vk = 62 if not soft else 48
    # electric piano: syncopated stabs (1, 2&, 3&) bossa-pop feel
    for off, d in ((0, 0.9 * B), (1.5 * B, 0.45 * B), (2.5 * B, 0.9 * B), (3.5 * B, 0.4 * B)):
        for k in tones:
            note(t0 + off, EP, k, d, vk)
    # bass: root, octave bounce, fifth, approach
    if b >= 1:
        vb = 92 if not soft else 80
        for off, k, d in ((0, root, 0.8 * B), (1 * B, root + 12, 0.35 * B), (1.5 * B, root, 0.4 * B),
                          (2 * B, root + 7, 0.8 * B), (3 * B, root + 12, 0.4 * B), (3.5 * B, root + 10, 0.4 * B)):
            note(t0 + off, BASS, k, d, vb)
    # drums
    if b == 0:  # pickup fill on last beat
        for i, k in enumerate((38, 38, 45, 41)):
            hit(t0 + 3 * B + i * B / 4, k, 70 + i * 12)
        for i in range(8):
            hit(t0 + i * B / 2, 54, 55 + (i % 2) * 20)  # tambourine
    else:
        vd = 1.0 if not soft else 0.75
        for i in range(4):
            hit(t0 + i * B, 36, int(100 * vd))                 # four on the floor, light
            hit(t0 + i * B + B / 2, 42, int(70 * vd))           # offbeat hats
            hit(t0 + i * B + B / 4, 42, int(38 * vd))
            hit(t0 + i * B + 3 * B / 4, 42, int(38 * vd))
        hit(t0 + 1 * B, 39, int(85 * vd)); hit(t0 + 3 * B, 39, int(85 * vd))   # claps on 2 and 4
        hit(t0 + 1 * B, 37, int(60 * vd)); hit(t0 + 3 * B, 37, int(60 * vd))   # rim
        for i in range(8):
            hit(t0 + i * B / 2 + B / 4, 54, int((50 if i % 2 else 70) * vd))   # tambourine 16ths
    # muted guitar chops on offbeats under the voice (adds bounce without crowding)
    if soft:
        for i in range(4):
            for k in tones[:3]:
                note(t0 + i * B + B / 2, GTR, k - 12, 0.12, 52)

# Japanese touch: koto glissando + shakuhachi breath in the intro, koto answers in the hook,
# soft koto arpeggios under the voice (D major pentatonic: D E F# A B)
PENTA = [62, 64, 66, 69, 71, 74, 76, 78, 81, 83, 86]
for i, k in enumerate(PENTA):
    note(0.05 + i * 0.07, KOTO, k, 1.2, 70 + i * 3)
note(0.9, SHAKU, 81, 1.0, 82)
for off, k in ((3.25, 86), (3.5, 83), (3.75, 81), (7.25, 78), (7.5, 81), (7.75, 83), (11.5, 86)):
    note(BAR + off * B, KOTO, k - 12, 0.6, 70)
for b in range(4, nbars, 2):
    t0 = b * BAR + 2 * B
    for i, k in enumerate((74, 78, 81, 83, 86)):
        note(t0 + i * B / 4, KOTO, k, 0.8, 48)
# koto hook (bars 1-3) — original melody in D major, resolving on D at 8 s
hook = [  # (beat offset from bar 1, midi, beats)
    (0, 78, .5), (.5, 81, .5), (1, 83, 1), (2, 81, .5), (2.5, 78, .5), (3, 76, 1),
    (4, 74, .5), (4.5, 76, .5), (5, 78, 1), (6, 79, .5), (6.5, 78, .5), (7, 76, .75), (7.75, 73, .25),
    (8, 74, .5), (8.5, 78, .5), (9, 81, .75), (9.75, 83, .25), (10, 81, .5), (10.5, 78, .5), (11, 76, .5), (11.5, 73, .5),
    (12, 74, 2.5)]
for off, k, d in hook:
    t = BAR + off * B
    note(t, KOTO, k, max(d * B, 0.5), 92)                 # koto carries the hook (no whistle)
# final sparkle at the resolution
for k in (86, 90, 93, 98):
    note(4 * BAR + (k - 86) * 0.02, GLOCK, k, 0.8, 58)

ev.sort(key=lambda e: (e[0], e[1]))
N = int(DUR * SR); out = np.zeros((N, 2), np.float32); pos = 0
for t, kind, ch, k, vel in ev + [(DUR, -1, 0, 0, 0)]:
    i = min(int(t * SR), N)
    if i > pos:
        buf = np.frombuffer(syn.generate(i - pos), dtype=np.float32).reshape(-1, 2)
        out[pos:i] = buf; pos = i
    if kind == 1: syn.noteon(ch, k, vel)
    elif kind == 0: syn.noteoff(ch, k)
mono = out.mean(axis=1)
# small room reverb
rev = mono.copy()
for dly, g in ((0.029, 0.22), (0.053, 0.16), (0.089, 0.11), (0.137, 0.07)):
    d = int(dly * SR); rev[d:] += mono[:-d] * g
rev = rev / (np.max(np.abs(rev)) + 1e-9) * 0.89
with wave.open(OUT, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((rev * 32767).astype(np.int16).tobytes())
print("ok")
