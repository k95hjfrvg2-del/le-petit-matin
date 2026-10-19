"""tts_paras.py <model.onnx> <voices.npz> <script.txt> <outdir> <voice> <speed>
Fallback voice (Kokoro). Applies prononciation.txt like kyutai_paras.py, and renders sentence by
sentence: Kokoro silently cuts text beyond ~500 phonemes, so whole paragraphs got truncated.
"""
import sys, os, re, numpy as np, wave
from kokoro_onnx import Kokoro
model, voices, script, outdir, voice, speed = sys.argv[1:7]
os.makedirs(outdir, exist_ok=True)

def load_lexicon():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prononciation.txt")
    pairs = []
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=>" in line:
                a, b = (s.strip() for s in line.split("=>", 1))
                if a and b and a != b:
                    pairs.append((a, b))
    return sorted(pairs, key=lambda ab: -len(ab[0]))

LEX = load_lexicon()
def speakable(text):
    for a, b in LEX:
        text = re.sub(r"(?<![\w-])" + re.escape(a) + r"(?![\w-])", b, text)
    return text

k = Kokoro(model, voices)
paras = [speakable(p.strip()) for p in open(script, encoding="utf-8").read().split("\n\n") if p.strip()]
for i, p in enumerate(paras):
    f = f"{outdir}/p{i:03d}.wav"
    if os.path.exists(f): continue
    chunks = []
    for s in re.split(r"(?<=[.!?»])\s+(?=[A-ZÀ-Ý«])", p):
        if chunks and len(chunks[-1]) + len(s) < 160: chunks[-1] += " " + s
        elif s.strip(): chunks.append(s)
    out = []
    for c in chunks:
        a, sr = k.create(c, voice=voice, speed=float(speed), lang="fr-fr")
        out += [a.astype(np.float32), np.zeros(int(sr * 0.18), np.float32)]
    x = np.clip(np.concatenate(out + [np.zeros(int(sr * 0.5), np.float32)]), -1, 1)
    with wave.open(f + ".tmp", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x * 32767).astype(np.int16).tobytes())
    os.rename(f + ".tmp", f); print(i, len(paras), flush=True)
print("DONE", flush=True)
