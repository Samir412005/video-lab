#!/usr/bin/env python3
"""Build colab/Chatterbox_Arabic_TTS.ipynb — Chatterbox Arabic TTS test.

Chatterbox Multilingual V3 (resemble-ai/chatterbox, MIT code + MIT weights):
23 languages incl. Arabic, zero-shot voice cloning, 500M params, runs on
a free Colab T4 (and ~3x real-time on CPU). The project was retired in
Aug 2026 (frozen archive) — install from the pinned commit, falling back
to the PyPI release if the pin fails.

The notebook generates one Arabic line and saves chatterbox_ar.wav, then
prints its duration so it can be compared with the Piper kareem version
of the same line (6.13 s).
"""
import json

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Chatterbox — Arabic TTS test\n",
            "\n",
            "Tests **Chatterbox Multilingual V3** (`resemble-ai/chatterbox`, MIT) on one Arabic line, as a\n",
            "possible upgrade over Piper kareem: more natural prosody + zero-shot voice cloning.\n",
            "Runs on a free Colab **T4 GPU** (or CPU, ~3x real-time). No login, no payment.\n",
            "\n",
            "Expected output: `chatterbox_ar.wav` (Arabic voiceover) + its duration.\n",
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import torch\n",
            "print('CUDA:', torch.cuda.is_available())\n",
            "if torch.cuda.is_available():\n",
            "    print(torch.cuda.get_device_name(0), torch.cuda.get_device_properties(0).total_memory // (1024**2), 'MiB')\n",
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('Install Chatterbox (pinned commit, PyPI fallback)...')\n",
            "!pip install -q git+https://github.com/resemble-ai/chatterbox.git@5de7a54 || pip install -q chatterbox-tts\n",
            "!python -c \"import chatterbox; print('chatterbox OK')\"\n",
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import torch\n",
            "import torchaudio\n",
            "from chatterbox.mtl_tts import ChatterboxMultilingualTTS\n",
            "\n",
            "device = 'cuda' if torch.cuda.is_available() else 'cpu'\n",
            "print('device:', device)\n",
            "model = ChatterboxMultilingualTTS.from_pretrained(device=device)\n",
            "print('sample rate:', model.sr)\n",
            "\n",
            "text = 'الجزائر، أرض التاريخ والحضارة، من البحر إلى الصحراء.'\n",
            "wav = model.generate(text, language_id='ar')\n",
            "torchaudio.save('chatterbox_ar.wav', wav, model.sr)\n",
            "print('saved chatterbox_ar.wav, duration:', round(wav.shape[-1] / model.sr, 2), 's')\n",
            "print('(Piper kareem version of the same line: 6.13 s)')\n",
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from IPython.display import Audio\n",
            "Audio('chatterbox_ar.wav')\n",
        ],
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Troubleshooting\n",
            "\n",
            "- **Install fails on the git pin:** the PyPI fallback in the install cell covers it.\n",
            "- **Arabic sounds off:** try `language_id='ar'` with a shorter sentence, or pass a short\n",
            "  reference voice clip via `audio_prompt_path=` for zero-shot cloning.\n",
            "- **Out of memory on CPU:** the model is 500M params — it fits, but generation is slower;\n",
            "  keep the text to one or two sentences.\n",
            "- **Compare with Piper:** the same line with Piper kareem is 6.13 s; judge naturalness\n",
            "  by listening, not by duration.\n",
        ],
    },
]

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12.0"},
        "accelerator": "GPU",
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open("Chatterbox_Arabic_TTS.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print(f"Wrote Chatterbox_Arabic_TTS.ipynb with {len(cells)} cells")
