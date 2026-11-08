import subprocess
import sys

# Synthesize the Arabic voiceover with Piper (kareem voice), one WAV
# for the single line of scripts/algeria10_vo.txt.
lines = [line.strip() for line in open("scripts/algeria10_vo.txt", encoding="utf-8")
         if line.strip()]
for i, line in enumerate(lines, 1):
    proc = subprocess.run(
        ["piper", "--model", "kareem.onnx", "--config", "kareem.onnx.json",
         "--output_file", f"vo{i}.wav"],
        input=line, text=True, encoding="utf-8", capture_output=True)
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        sys.exit(1)
    print(f"vo{i}.wav done: {line}")
