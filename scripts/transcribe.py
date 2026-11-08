import subprocess
import sys
import numpy as np
from faster_whisper import WhisperModel

def fmt(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

audio, out = sys.argv[1], sys.argv[2]
# Decode with FFmpeg to 16 kHz mono float32 raw PCM first.
# (faster-whisper's own decoder uses PyAV, whose `metadata_errors`
# argument breaks with the av version pip installs on the runner,
# so we bypass it and hand Whisper a numpy array instead.)
subprocess.run(
    ["ffmpeg", "-y", "-v", "error", "-i", audio,
     "-ac", "1", "-ar", "16000", "-f", "f32le", "-acodec", "pcm_f32le", "voice.raw"],
    check=True,
)
pcm = np.fromfile("voice.raw", dtype=np.float32)
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe(pcm, language="en")
with open(out, "w", encoding="utf-8") as f:
    for i, seg in enumerate(segments, 1):
        f.write(f"{i}\n{fmt(seg.start)} --> {fmt(seg.end)}\n{seg.text.strip()}\n\n")
print("SRT written to", out)
