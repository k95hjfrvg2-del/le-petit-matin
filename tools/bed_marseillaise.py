"""Peppy brass-band intro on the opening phrase of La Marseillaise (Rouget de Lisle, 1792,
public domain melody; this arrangement and synthesis are original, no recording used).
Brass melody + harmony, snare roll, timpani, cymbal crash, then a light march groove to sit
under the voice.  Usage: python3 bed_marseillaise.py out.wav [seconds]"""
import sys, wave, numpy as np
SR = 44100
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 34.0
BPM = 116; beat = 60 / BPM; N = int(SR * DUR)
mix = np.zeros(N); rng = np.random.default_rng(1792)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def add(sig, start, gain=1.0):
    i = int(start * SR)
    if i >= N or i < 0: return
    j = min(N, i + len(sig)); mix[i:j] += sig[: j - i] * gain
def lowpass_var(x, cut):
    y = np.zeros_like(x); prev = 0.0
    a = np.exp(-2 * np.pi * np.asarray(cut) / SR)
    a = np.broadcast_to(a, x.shape)
    for k in range(len(x)):
        prev = (1 - a[k]) * x[k] + a[k] * prev; y[k] = prev
    return y
def brass(m, dur, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    vib = 1 + 0.003 * np.sin(2 * np.pi * 5.2 * t) * np.clip(t / 0.25, 0, 1)
    ph = np.cumsum(2 * np.pi * hz(m) * vib / SR)
    saw = sum(np.sin(k * ph) / k for k in range(1, 12))
    att = np.clip(t / 0.04, 0, 1); rel = np.clip((dur - t) / 0.06, 0, 1)
    cut = 500 + 3800 * bright * (0.55 + 0.45 * np.exp(-t * 6)) * att
    return lowpass_var(saw, cut) * att * rel * 0.5
def snare(gain=1.0, length=0.16):
    n = int(length * SR); t = np.arange(n) / SR
    return (rng.standard_normal(n) * 0.8 + np.sin(2 * np.pi * 185 * t) * 0.5) * np.exp(-t * 22) * gain
def timp(m, gain=1.0):
    n = int(1.2 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * hz(m) * t * (1 + 0.02 * np.exp(-t * 8))) * np.exp(-t * 3) * gain
def crash(gain=1.0):
    n = int(2.5 * SR); t = np.arange(n) / SR
    x = np.diff(rng.standard_normal(n + 1)) * np.exp(-t * 1.6)
    return x * gain

t0 = 0.5
# snare roll crescendo into the pickup
roll_start = t0 - 0.0
for k in range(int(1.0 / 0.045)):
    add(snare(0.08 + 0.25 * k / 22, 0.08), t0 + k * 0.045 - 1.0 + 1.0)
t_mel = t0 + 1.0
# melody in G major: (midi, beats)
mel = [(62, .375), (62, .125), (62, .5),
       (67, 1), (67, 1), (69, 1), (69, 1),
       (74, 1.5), (71, .375), (67, .125),
       (67, .375), (71, .125), (67, .375), (64, .125), (72, 1), (69, .75), (66, .25),
       (67, 2.5)]
harm = {67: 59, 69: 66, 74: 71, 71: 67, 64: 60, 72: 69, 66: 62, 62: 59}  # thirds/sixths below
t = t_mel
for m, b in mel:
    d = b * beat
    add(brass(m, d * 0.97), t, 0.55)
    add(brass(m + 12, d * 0.97, 0.7), t, 0.12)           # trumpet octave sparkle
    add(brass(harm[m], d * 0.97, 0.8), t, 0.30)           # horn harmony
    t += d
mel_end = t
# bass / timpani on strong beats: G D G D ... and final G
bar = 4 * beat
chords = [(43, t_mel + 1 * beat), (50, t_mel + 3 * beat), (43, t_mel + 5 * beat), (50, t_mel + 7 * beat),
          (48, t_mel + 9 * beat), (50, t_mel + 10.5 * beat)]
for m, tt in chords:
    add(brass(m, beat * 1.4, 0.5), tt, 0.35); add(timp(m + 12, 0.35), tt)
# march snare during melody: on beats with a flam
k = 0
tt = t_mel + beat
while tt < mel_end - beat * 0.5:
    add(snare(0.18 if k % 2 else 0.28), tt)
    tt += beat / 2; k += 1
# final hit
add(crash(0.22), mel_end - 2.5 * beat)
add(timp(43, 0.7), mel_end - 2.5 * beat); add(timp(55, 0.4), mel_end - 2.5 * beat)
for m in (55, 59, 62, 67):
    add(brass(m, 1.4, 0.9), mel_end - 2.5 * beat, 0.25)
# light march groove under the voice (bass + soft snare + cymbal ticks), until the end
tt = mel_end + 0.2; k = 0
prog = [43, 50, 48, 50]
while tt < DUR - 0.5:
    if k % 4 == 0:
        add(brass(prog[(k // 4) % 4], beat * 0.9, 0.35), tt, 0.25)
    if k % 2 == 1:
        add(snare(0.10, 0.10), tt)
    n = int(0.05 * SR)
    add(np.diff(rng.standard_normal(n + 1)) * np.exp(-np.arange(n) / SR * 70) * 0.04, tt)
    tt += beat; k += 1
# hall reverb (simple multi-tap)
out = mix.copy()
for dly, g in ((0.031, 0.25), (0.067, 0.18), (0.113, 0.12), (0.171, 0.08)):
    d = int(dly * SR); out[d:] += mix[:-d] * g
out = out / np.max(np.abs(out)) * 0.89
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
print("melody ends at", round(mel_end, 2), "s")
