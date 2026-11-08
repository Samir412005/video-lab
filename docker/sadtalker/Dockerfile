# SadTalker in a pinned environment — the radical fix for the Colab failures.
#
# Problem: SadTalker (2024, unmaintained) pins numpy==1.23.4, scipy==1.10.1,
# scikit-image==0.19.3 and basicsr==1.4.2. Colab now runs Python 3.13 +
# NumPy 2, where those pins have no wheels (numpy) or fail to build
# (basicsr). Every fix peeled one layer and exposed the next failure.
#
# Fix: stop fighting the host environment. Build SadTalker in the exact
# environment it was written for — Python 3.10, CPU torch, original pins —
# inside Docker, and run it on GitHub Actions (free, 4 vCPU, 16 GB RAM).
# No Colab, no GPU queue, no manual notebook clicks. A 6 s talking-head
# clip takes a few minutes on CPU.
#
# Build:  docker build -t sadtalker:test docker/sadtalker
# Run:    docker run --rm -v $PWD:/work -w /app sadtalker:test \
#           python inference.py --driven_audio /work/assets/vo_test.wav \
#           --source_image /work/assets/portrait.jpg --result_dir /work/out \
#           --still --preprocess full --enhancer gfpgan --size 512
FROM python:3.10-slim

# System deps: ffmpeg (video I/O), git (clone), build tools (basicsr),
# libGL/libglib (OpenCV).
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg git build-essential libgl1 libglib2.0-0 wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Torch CPU (no CUDA needed for a short test clip; much smaller than CUDA).
RUN pip install --no-cache-dir torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

# SadTalker, original pins (they have wheels and build cleanly on 3.10).
RUN git clone --depth 1 https://github.com/OpenTalker/SadTalker.git /tmp/st \
    && cp -r /tmp/st/. /app/ && rm -rf /tmp/st
RUN pip install --no-cache-dir -r requirements.txt

# Pre-trained checkpoints (~2 GB) via SadTalker's own script.
RUN bash scripts/download_models.sh

# Sanity check: the imports that kept failing on Colab.
RUN python -c "import kornia, facexlib, gfpgan, basicsr, librosa; print('deps OK')"

ENTRYPOINT ["python", "inference.py"]
