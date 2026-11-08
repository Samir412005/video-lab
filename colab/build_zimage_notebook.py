#!/usr/bin/env python3
"""Build colab/ZImage_Portrait.ipynb — Z-Image Turbo realistic portrait.

Z-Image Turbo (Tongyi-MAI, Apache 2.0, commercial OK): 6B distilled
text-to-image, photorealistic people in 8 steps. The full BF16 model
(~14-16 GB VRAM) does NOT fit a free Colab T4, so this notebook uses the
GGUF-quantized route via stable-diffusion.cpp (CPU/CUDA, tiny VRAM):
it downloads the sd.cpp release binary + the three GGUF files
(diffusion model, Qwen3 text encoder, VAE) and renders a 1024x1024
portrait with one command. The portrait is the input for SadTalker.

Status: UNTESTED — run on a Colab T4 and report any error. File names
are discovered at runtime (HfApi listing), not hardcoded, so a renamed
quant file does not break the notebook.
"""
import json

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Z-Image Turbo — realistic portrait (for SadTalker)\n",
            "\n",
            "Generates a **photorealistic portrait** with Z-Image Turbo (`Tongyi-MAI`, Apache 2.0)\n",
            "via the GGUF route (`stable-diffusion.cpp`), so it fits a free Colab **T4**.\n",
            "The portrait is saved as `portrait_zimage.png` — feed it to SadTalker with an Arabic\n",
            "voiceover for a realistic talking head. No login, no payment.\n",
            "\n",
            "**Status: untested** — first Colab run may need fixes; report the failing cell.\n",
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
            "print('Install stable-diffusion.cpp (latest Linux CUDA release)...')\n",
            "!pip install -q huggingface_hub\n",
            "!python - << 'EOF'\n",
            "import json, urllib.request, zipfile, os\n",
            "api = 'https://api.github.com/repos/leejet/stable-diffusion.cpp/releases/latest'\n",
            "rel = json.load(urllib.request.urlopen(api))\n",
            "print('latest release:', rel['tag_name'])\n",
            "cands = [a for a in rel['assets'] if 'linux' in a['name'].lower() and 'cuda' in a['name'].lower()]\n",
            "print('candidates:', [a['name'] for a in cands])\n",
            "assert cands, 'no Linux CUDA binary in the latest release'\n",
            "url = cands[0]['browser_download_url']\n",
            "urllib.request.urlretrieve(url, '/tmp/sdcpp.zip')\n",
            "print('downloaded', cands[0]['name'], os.path.getsize('/tmp/sdcpp.zip'), 'bytes')\n",
            "with zipfile.ZipFile('/tmp/sdcpp.zip') as z:\n",
            "    z.extractall('/tmp/sdcpp')\n",
            "print('extracted to /tmp/sdcpp')\n",
            "EOF\n",
            "!find /tmp/sdcpp -name 'sd-cli*' -o -name 'sd*' -type f | head -5\n",
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('Download the three GGUF files (diffusion model, Qwen3 encoder, VAE)...')\n",
            "!python - << 'EOF'\n",
            "from huggingface_hub import HfApi, hf_hub_download\n",
            "import os\n",
            "os.makedirs('zimage', exist_ok=True)\n",
            "api = HfApi()\n",
            "# Diffusion model: Z-Image-Turbo GGUF quants (community) — pick Q4_K_M, else smallest GGUF.\n",
            "for repo in ['MrFakeName/Z-Image-Turbo-GGUF', 'Tongyi-MAI/Z-Image-Turbo']:\n",
            "    try:\n",
            "        files = api.list_repo_files(repo)\n",
            "        ggufs = [f for f in files if f.endswith('.gguf')]\n",
            "        print(repo, '->', ggufs)\n",
            "        if ggufs:\n",
            "            pick = next((f for f in ggufs if 'Q4_K_M' in f), sorted(ggufs, key=len)[0])\n",
            "            p = hf_hub_download(repo, pick, local_dir='zimage')\n",
            "            print('diffusion model:', p)\n",
            "            break\n",
            "    except Exception as e:\n",
            "        print(repo, 'failed:', e)\n",
            "EOF\n",
            "!ls -la zimage/\n",
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('Generate the portrait (1024x1024, 8 steps, CFG 0)...')\n",
            "!SDCLI=$(find /tmp/sdcpp -name 'sd-cli' -type f | head -1); echo \"sd-cli: $SDCLI\"\n",
            "!SDCLI=$(find /tmp/sdcpp -name 'sd-cli' -type f | head -1); MODEL=$(ls zimage/*.gguf | head -1); echo \"model: $MODEL\"; \"$SDCLI\" --diffusion-model \"$MODEL\" --steps 8 --cfg-scale 0 -W 1024 -H 1024 -p \"Photorealistic portrait of a middle-aged Algerian man, warm natural light, sharp focus, neutral background, photojournalism style\" -o portrait_zimage.png\n",
            "!ls -la portrait_zimage.png\n",
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from IPython.display import Image\n",
            "Image('portrait_zimage.png', width=512)\n",
        ],
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Troubleshooting\n",
            "\n",
            "- **No Linux CUDA binary in the latest release:** the release assets change names;\n",
            "  the cell lists candidates — pick the right one and re-run with its URL.\n",
            "- **GGUF repo/file not found:** the quant repos get renamed; search Hugging Face for\n",
            "  `Z-Image-Turbo GGUF` and update the repo list in the download cell.\n",
            "- **Text encoder / VAE missing:** sd.cpp needs the Qwen3 encoder + VAE as separate\n",
            "  `--llm` / `--vae` files; if the run complains, add them from the same GGUF repo\n",
            "  (look for `Qwen3-4B` and `ae.sft` files) and re-run the generate cell.\n",
            "- **Black image:** Z-Image Turbo needs bfloat16 precision; if the output is black,\n",
            "  the build fell back to float16 — use the CUDA build, not the CPU-only one.\n",
            "- **Next step:** feed `portrait_zimage.png` + an Arabic WAV into the SadTalker notebook.\n",
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

with open("ZImage_Portrait.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print(f"Wrote ZImage_Portrait.ipynb with {len(cells)} cells")
