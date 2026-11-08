#!/usr/bin/env bash
# Blender 4.2 LTS — official tarball install (workflow-ready snippet).
#
# WHY: the Ubuntu apt Blender (4.0.2, and 5.0.1 on newer runners) ships
# WITHOUT OpenImageDenoiser (OIDN). The official blender.org 4.2 LTS
# tarball ships OIDN + Grease Pencil 3 + newer Cycles — the single
# biggest quality upgrade for the cloud render farm (Round 7 finding).
# Free, no signup, no login.
#
# VERIFIED (Round 8, 2026-11-08):
#   URL: https://download.blender.org/release/Blender4.2/blender-4.2.23-linux-x64.tar.xz
#   HEAD: 200 OK, Content-Length: 350707672 bytes (~334 MB)
#   Latest 4.2.x patch on 2026-11-08 is 4.2.23 (index lists 4.2.0..4.2.23).
#
# USAGE (GitHub Actions step):
#   - name: Install Blender 4.2 LTS (official, with OIDN)
#     run: bash scripts/blender42_install.sh
#   After it runs, `blender` is on PATH. Scripts can then set
#   scene.cycles.use_denoising = True and scene.cycles.denoiser = 'OPENIMAGEDENOISE'.
#
# USAGE (local test): bash scripts/blender42_install.sh (needs ~700 MB free:
# 334 MB download + 334 MB extracted; installs to /opt or $BLENDER_DIR).
set -euo pipefail

BLENDER_VERSION="${BLENDER_VERSION:-4.2.23}"
BLENDER_URL="https://download.blender.org/release/Blender4.2/blender-${BLENDER_VERSION}-linux-x64.tar.xz"
INSTALL_DIR="${BLENDER_DIR:-/opt}"

echo "Installing Blender ${BLENDER_VERSION} from ${BLENDER_URL} ..."
curl -sSL -o /tmp/blender-4.2.tar.xz "${BLENDER_URL}"
echo "Downloaded: $(stat -c%s /tmp/blender-4.2.tar.xz) bytes (expected ~350707672)"

mkdir -p "${INSTALL_DIR}"
tar -xf /tmp/blender-4.2.tar.xz -C "${INSTALL_DIR}"
BLENDER_BIN="${INSTALL_DIR}/blender-${BLENDER_VERSION}-linux-x64/blender"
test -x "${BLENDER_BIN}"
export PATH="$(dirname "${BLENDER_BIN}"):$PATH"

echo "--- version ---"
blender --version | head -2

echo "--- OIDN check (must print OPENIMAGEDENOISE) ---"
blender -b --python-expr "
import bpy
scene = bpy.context.scene
scene.cycles.denoiser = 'OPENIMAGEDENOISE'
scene.cycles.use_denoising = True
print('OIDN OK:', scene.cycles.denoiser)
" 2>&1 | grep -E "OIDN OK|Error" | head -3

rm -f /tmp/blender-4.2.tar.xz
echo "Blender ${BLENDER_VERSION} ready at ${BLENDER_BIN}"
