#!/usr/bin/env python3
"""Remove the background from a still image (for compositing).

Uses rembg with an MIT-licensed model. IMPORTANT: rembg's DEFAULT model
(BRIA RMBG 2.0) is NON-COMMERCIAL — this script defaults to `u2net`
(MIT) and refuses the BRIA model unless you explicitly pass it.

Usage:
    python3 scripts/remove_bg.py portrait.jpg portrait_nobg.png
    python3 scripts/remove_bg.py portrait.jpg out.png --model u2net_human_seg
    python3 scripts/remove_bg.py frames/ nobg_frames/ --batch

The u2net model (~170 MB) downloads automatically on first use.
For video: extract frames with FFmpeg, run --batch, re-assemble.
"""
import argparse
import os
import sys


def remove_one(inp, outp, model):
    # rembg 2.x: `session` must be a Session object, not a model-name string.
    from rembg import remove, new_session
    session = new_session(model)
    with open(inp, "rb") as f:
        data = f.read()
    result = remove(data, session=session)
    with open(outp, "wb") as f:
        f.write(result)


def main():
    ap = argparse.ArgumentParser(description="Remove image background (MIT model)")
    ap.add_argument("input", help="Input image file or directory (--batch)")
    ap.add_argument("output", help="Output PNG file or directory (--batch)")
    ap.add_argument("--model", default="u2net",
                    choices=["u2net", "u2net_human_seg", "birefnet-general"],
                    help="MIT-licensed segmentation model (default u2net)")
    ap.add_argument("--batch", action="store_true",
                    help="Process every image in the input directory")
    args = ap.parse_args()

    if args.model.startswith("bria"):
        print("ERROR: the BRIA model is non-commercial; refusing.", file=sys.stderr)
        sys.exit(2)

    if args.batch:
        os.makedirs(args.output, exist_ok=True)
        names = sorted(n for n in os.listdir(args.input)
                       if n.lower().endswith((".png", ".jpg", ".jpeg", ".webp")))
        for n in names:
            outp = os.path.join(args.output, os.path.splitext(n)[0] + ".png")
            remove_one(os.path.join(args.input, n), outp, args.model)
            print(f"done {n} -> {outp}")
    else:
        remove_one(args.input, args.output, args.model)
        print(f"done {args.input} -> {args.output}")


if __name__ == "__main__":
    main()
