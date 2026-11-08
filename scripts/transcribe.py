import sys
from faster_whisper import WhisperModel

def fmt(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

audio, out = sys.argv[1], sys.argv[2]
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe(audio, language="en")
with open(out, "w", encoding="utf-8") as f:
    for i, seg in enumerate(segments, 1):
        f.write(f"{i}\n{fmt(seg.start)} --> {fmt(seg.end)}\n{seg.text.strip()}\n\n")
print("SRT written to", out)
