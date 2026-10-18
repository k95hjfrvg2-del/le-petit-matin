import sys, os, numpy as np, wave
from kokoro_onnx import Kokoro
model, voices, script, outdir, voice, speed = sys.argv[1:7]
os.makedirs(outdir, exist_ok=True)
k = Kokoro(model, voices)
paras = [p.strip() for p in open(script, encoding="utf-8").read().split("\n\n") if p.strip()]
for i, p in enumerate(paras):
    f = f"{outdir}/p{i:03d}.wav"
    if os.path.exists(f): continue
    a, sr = k.create(p, voice=voice, speed=float(speed), lang="fr-fr")
    x = np.clip(np.concatenate([a.astype(np.float32), np.zeros(int(sr * 0.6), np.float32)]), -1, 1)
    with wave.open(f + ".tmp", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x * 32767).astype(np.int16).tobytes())
    os.rename(f + ".tmp", f); print(i, len(paras), flush=True)
print("DONE", flush=True)
