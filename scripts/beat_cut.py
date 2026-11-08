#!/usr/bin/env python3
"""Beat-aligned cut points for professional montage.

Uses librosa (already in the SadTalker/Colab env; `pip install librosa`
on the Actions runner) to detect the beats of an audio track, then picks
cut points on beats so photo/video segments change on the music — the
professional-montage requirement (cuts on the audio cue, not arbitrary).

Usage:
    python3 scripts/beat_cut.py mixed.wav --segments 4
    python3 scripts/beat_cut.py music.mp3 --segments 4 --start 2.0 --end 20.0

Output (stdout): one cut time in seconds per line, plus a JSON summary
on stderr. The cut times split [start, end] into N segments whose
boundaries land on the nearest detected beat.
"""
import argparse
import json
import sys


def main():
    ap = argparse.ArgumentParser(description="Beat-aligned cut points")
    ap.add_argument("audio", help="Audio file (wav/mp3)")
    ap.add_argument("--segments", type=int, default=4,
                    help="Number of segments to cut into (default 4)")
    ap.add_argument("--start", type=float, default=0.0,
                    help="Start of the range in seconds (default 0)")
    ap.add_argument("--end", type=float, default=None,
                    help="End of the range in seconds (default: audio duration)")
    args = ap.parse_args()

    import librosa

    y, sr = librosa.load(args.audio, sr=22050, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)
    end = args.end if args.end is not None else duration
    if end > duration:
        end = duration

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units="frames")
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    # Keep only beats inside the range.
    beats = [float(t) for t in beat_times if args.start <= t <= end]
    if len(beats) < 2:
        print("WARNING: fewer than 2 beats detected; "
              "falling back to even cuts", file=sys.stderr)
        beats = None

    n = args.segments
    cuts = []
    if beats:
        # Ideal even boundaries, snapped to the nearest beat.
        for i in range(1, n):
            ideal = args.start + (end - args.start) * i / n
            nearest = min(beats, key=lambda b: abs(b - ideal))
            if not cuts or nearest > cuts[-1] + 0.3:
                cuts.append(round(nearest, 3))
    if len(cuts) < n - 1:
        # Fill any missing boundaries with even cuts.
        for i in range(1, n):
            ideal = round(args.start + (end - args.start) * i / n, 3)
            if all(abs(ideal - c) > 0.3 for c in cuts):
                cuts.append(ideal)
        cuts = sorted(cuts)[: n - 1]

    for c in cuts:
        print(c)
    # librosa >= 0.10 returns tempo as an array (possibly multi-estimate).
    import numpy as np
    tempo_val = float(np.asarray(tempo).flat[0]) if np.size(tempo) else 0.0
    print(json.dumps({"tempo_bpm": round(tempo_val, 1),
                      "duration": round(duration, 2),
                      "beats_in_range": len(beats) if beats else 0,
                      "cuts": cuts}), file=sys.stderr)


if __name__ == "__main__":
    main()
