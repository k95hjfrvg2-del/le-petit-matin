"""kyutai_paras.py <script.txt> <outdir> [voice]
Render each paragraph (blank-line separated) of a French script with Kyutai TTS 1.6B en_fr on CPU.
Resumable: paragraphs already rendered (pNNN.wav) are skipped. Prints "i n" per paragraph and DONE.
Needs: pip install --break-system-packages torch moshi ; huggingface.co and *.hf.co reachable.
"""
import sys, os, re, wave, numpy as np, torch
from moshi.models.loaders import CheckpointInfo
from moshi.models.tts import DEFAULT_DSM_TTS_REPO, TTSModel

VOICE = "cml-tts/fr/10177_10625_000134-0003_enhanced.wav"  # chosen by the listener (sample "L")
torch.set_num_threads(os.cpu_count() or 2)
script, outdir = sys.argv[1:3]
voice = sys.argv[3] if len(sys.argv) > 3 else VOICE
os.makedirs(outdir, exist_ok=True)
def load_lexicon():
    """Pronunciation fixes from prononciation.txt at the repo root: 'Correct spelling => phonetic'."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prononciation.txt")
    pairs = []
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=>" in line:
                a, b = (s.strip() for s in line.split("=>", 1))
                if a and b and a != b:
                    pairs.append((a, b))
    return sorted(pairs, key=lambda ab: -len(ab[0]))  # longest names first

LEX = load_lexicon()
def speakable(text):
    for a, b in LEX:
        text = re.sub(r"(?<![\w-])" + re.escape(a) + r"(?![\w-])", b, text)
    return text

paras = [speakable(p.strip()) for p in open(script, encoding="utf-8").read().split("\n\n") if p.strip()]
model = TTSModel.from_checkpoint_info(CheckpointInfo.from_hf_repo(DEFAULT_DSM_TTS_REPO), n_q=32, temp=0.6,
                                      device=torch.device("cpu"), dtype=torch.bfloat16)
cond = model.make_condition_attributes([model.get_voice_path(voice)], cfg_coef=2.0)
sr = int(model.mimi.sample_rate)
for i, p in enumerate(paras):
    f = f"{outdir}/p{i:03d}.wav"
    if os.path.exists(f):
        continue
    pcms = []
    def on_frame(frame):
        if (frame != -1).all():
            pcms.append(np.clip(model.mimi.decode(frame[:, 1:, :]).cpu().float().numpy()[0, 0], -1, 1))
    entries = model.prepare_script([p], padding_between=1)
    with model.mimi.streaming(1), torch.no_grad():
        model.generate([entries], [cond], on_frame=on_frame)
    x = np.concatenate(pcms + [np.zeros(int(sr * 0.45), np.float32)])
    with wave.open(f + ".tmp", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x * 32767).astype(np.int16).tobytes())
    os.rename(f + ".tmp", f)
    print(i, len(paras), flush=True)
print("DONE", flush=True)
