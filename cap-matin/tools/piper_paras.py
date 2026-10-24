"""piper_paras.py <script.txt> <outdir> <voice.onnx>
Render each paragraph (blank-line separated) of the Cap Matin script with Piper, voice fr_FR-upmc-medium,
speaker "jessica" (female; chosen by the listener). Applies cap-matin/prononciation.txt first.
Adds a short pause after each paragraph. Prints DONE at the end."""
import sys, os, re, subprocess, wave, numpy as np

script, outdir, model = sys.argv[1:4]
os.makedirs(outdir, exist_ok=True)
lex_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prononciation.txt")
pairs = []
for line in open(lex_path, encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=>" in line:
        a, b = (s.strip() for s in line.split("=>", 1))
        if a and b and a != b:
            pairs.append((a, b))
pairs.sort(key=lambda ab: -len(ab[0]))
def speakable(t):
    for a, b in pairs:
        t = re.sub(r"(?<![\w-])" + re.escape(a) + r"(?![\w-])", b, t)
    return t.replace("\n", " ")

paras = [speakable(p.strip()) for p in open(script, encoding="utf-8").read().split("\n\n") if p.strip()]
for i, p in enumerate(paras):
    f = f"{outdir}/p{i:03d}.wav"
    subprocess.run([sys.executable, "-m", "piper", "-m", model, "-s", "0", "--length-scale", "1.15",
                    "--noise-scale", "0.6", "--noise-w-scale", "0.7", "--sentence-silence", "0.3", "-f", f + ".raw.wav"],
                   input=p.encode("utf-8"), check=True, capture_output=True)
    with wave.open(f + ".raw.wav") as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
    x = np.concatenate([x, np.zeros(int(sr * 0.55), np.int16)])
    with wave.open(f, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(x.tobytes())
    os.remove(f + ".raw.wav")
    print(i + 1, len(paras), flush=True)
print("DONE", flush=True)
