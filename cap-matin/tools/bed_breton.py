"""Original Breton-flavoured acoustic intro for Cap Matin: Celtic harp, bombarde (oboe), fiddle,
tin whistle, nylon guitar, accordion drone and a soft frame drum, played with GeneralUser GS.
No synths. Usage: python3 bed_breton.py <GeneralUser-GS.sf2> out.wav [seconds]
Layout at 120 BPM (one bar = 2 s): the an-dro style tune (bombarde + fiddle) starts at 0 s, no
introductory notes, resolving on D at 6 s, then a light harp/guitar accompaniment under the voice."""
import sys, wave, numpy as np, tinysoundfont

SF, OUT = sys.argv[1], sys.argv[2]
OUT_DUR = float(sys.argv[3]) if len(sys.argv) > 3 else 34.0
DUR = OUT_DUR + 2.0   # first bar is silent and gets cut: the music starts straight away
SR = 44100; B = 0.5; BAR = 4 * B
syn = tinysoundfont.Synth(samplerate=SR, gain=-3)
sf = syn.sfload(SF)
HARP, BOMB, FID, WHIS, GTR, ACC, DR = 0, 1, 2, 3, 4, 5, 9
syn.program_select(HARP, sf, 0, 46)   # Orchestral harp (Celtic harp colour)
syn.program_select(BOMB, sf, 0, 68)   # Oboe ~ bombarde
syn.program_select(FID, sf, 0, 40)    # Violin (fiddle)
syn.program_select(WHIS, sf, 0, 78)   # Tin whistle
syn.program_select(GTR, sf, 0, 24)    # Nylon guitar
syn.program_select(ACC, sf, 0, 21)    # Accordion (drone, very soft)
syn.program_select(DR, sf, 128, 0, is_drums=True)
ev = []
def note(t, ch, k, d, v): ev.append((t, 1, ch, k, v)); ev.append((t + d, 0, ch, k, 0))
def hit(t, k, v): note(t, DR, k, 0.1, v)

# D mixolydian feel: D - C - D - Am / G - D
chords = [([50, 57, 62, 66], 38), ([48, 55, 60, 64], 36), ([50, 57, 62, 66], 38), ([45, 52, 57, 60], 33)]
nbars = int(DUR / BAR) + 1
for b in range(nbars):
    t0 = b * BAR
    tones, root = chords[b % 4]
    soft = b >= 4
    if b >= 1:
        # guitar: an-dro bounce (1, 2&, 3, 4)
        vg = 58 if not soft else 46
        for off in (0, 1.5 * B, 2 * B, 3 * B):
            for j, k in enumerate(tones):
                note(t0 + off + j * 0.012, GTR, k, 0.45, vg)
        # harp bass and broken chord
        note(t0, HARP, root, 1.6, 70 if not soft else 56)
        if soft:
            for j, k in enumerate(tones[1:] + [tones[1] + 12]):
                note(t0 + (j + 1) * B, HARP, k + 12, 0.9, 44)
        # accordion drone (barely there)
        note(t0, ACC, root + 12, BAR, 30 if not soft else 22)
        # frame drum: soft heartbeat
        vd = 52 if not soft else 34
        hit(t0, 41, vd + 10); hit(t0 + 1.5 * B, 41, vd); hit(t0 + 2 * B, 45, vd + 4); hit(t0 + 3 * B, 45, vd - 6)
# tune (bars 1-3), original, D mixolydian, resolving on D at 8 s
tune = [(0, 74, .5), (.5, 76, .5), (1, 78, 1), (2, 79, .5), (2.5, 78, .5), (3, 76, 1),
        (4, 74, .5), (4.5, 72, .5), (5, 74, .75), (5.75, 76, .25), (6, 72, 1), (7, 69, 1),
        (8, 74, .5), (8.5, 78, .5), (9, 81, 1), (10, 79, .5), (10.5, 78, .5), (11, 76, .5), (11.5, 72, .5),
        (12, 74, 2.5)]
for off, k, d in tune:
    t = BAR + off * B
    note(t, BOMB, k, max(d * B * 0.95, 0.22), 88)
    note(t, FID, k - 12, max(d * B * 0.95, 0.22), 70)
# whistle ornament on the last phrase
for off, k in ((8, 86), (8.5, 90), (9, 93), (12, 86)):
    note(BAR + off * B, WHIS, k, 0.45, 52)
# under the voice: a quiet whistle echo every 8 s
for b in range(5, nbars, 4):
    for i, k in enumerate((78, 81, 79, 76)):
        note(b * BAR + i * B, WHIS, k, 0.45, 34)

ev.sort(key=lambda e: (e[0], e[1]))
N = int(DUR * SR); out = np.zeros((N, 2), np.float32); pos = 0
for t, kind, ch, k, vel in ev + [(DUR, -1, 0, 0, 0)]:
    i = min(int(t * SR), N)
    if i > pos:
        out[pos:i] = np.frombuffer(syn.generate(i - pos), dtype=np.float32).reshape(-1, 2); pos = i
    if kind == 1: syn.noteon(ch, k, vel)
    elif kind == 0: syn.noteoff(ch, k)
mono = out.mean(axis=1)[int(BAR * SR):]   # drop the empty first bar
rev = mono.copy()   # small stone-chapel reverb
for dly, g in ((0.031, 0.25), (0.057, 0.19), (0.097, 0.14), (0.151, 0.09), (0.233, 0.05)):
    d = int(dly * SR); rev[d:] += mono[:-d] * g
rev = rev / (np.max(np.abs(rev)) + 1e-9) * 0.89
with wave.open(OUT, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((rev * 32767).astype(np.int16).tobytes())
print("ok")
