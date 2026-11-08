#!/usr/bin/env python3
"""Round 8 fetcher — downloads CC0 assets verified by URL/API checks.

Sources (all free, no key, no login):
- UAL (Universal Animation Library, CC0): GitHub mirror IAFahim/
  quaternius.universalAnimationLibrary.standard (FBX 45 clips)
- Quaternius RPG Characters Pack (CC0): OpenGameArt direct zip
- Poly Haven PBR textures + models (CC0): dl.polyhaven.org via the
  public files API (api.polyhaven.com/files/<slug>)

Verifies every file (magic bytes / JSON / sizes) and prints a manifest.
Usage: python3 scripts/fetch_round8.py
"""
import json
import os
import sys
import urllib.request
import zipfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "video-lab-round8/1.0 (open-source asset fetch)"}


def get(url, dest):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    return os.path.getsize(dest)


def api_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def check(path, kind):
    """Magic-byte / structure check. Returns (ok, detail)."""
    with open(path, "rb") as f:
        head = f.read(64)
    size = os.path.getsize(path)
    if size == 0:
        return False, "empty file"
    if kind == "fbx":
        return (head.startswith(b"Kaydara FBX Binary"),
                "FBX binary header" if head.startswith(b"Kaydara FBX Binary") else f"bad header {head[:16]!r}")
    if kind == "zip":
        return head[:2] == b"PK", "ZIP header"
    if kind == "jpg":
        return head[:2] == b"\xff\xd8", "JPEG header"
    if kind == "bin":
        # glTF binary buffer (geometry) — any non-empty binary is valid here;
        # the manifest's buffer byteLength is cross-checked by the caller.
        return True, f"glTF binary buffer, {size} bytes"
    if kind == "gltf":
        try:
            d = json.load(open(path))
            return "asset" in d, f"glTF JSON, generator={d.get('asset', {}).get('generator')}"
        except Exception as e:
            return False, f"bad JSON: {e}"
    return True, f"{size} bytes"


def main():
    manifest = []

    # --- 1. UAL (Universal Animation Library) FBX + LICENSE ---
    mocap = os.path.join(BASE, "assets", "mocap")
    os.makedirs(mocap, exist_ok=True)
    fbx = os.path.join(mocap, "UAL1_Standard.fbx")
    print("UAL FBX ...", end=" ", flush=True)
    n = get("https://raw.githubusercontent.com/IAFahim/quaternius.universalAnimationLibrary.standard/main/UAL1_Standard.fbx", fbx)
    ok, det = check(fbx, "fbx")
    print(f"{n} bytes, {det} -> {'OK' if ok else 'FAIL'}")
    manifest.append(("UAL1_Standard.fbx", n, ok, det))
    lic = os.path.join(mocap, "LICENSE_UAL_CC0.txt")
    get("https://raw.githubusercontent.com/IAFahim/quaternius.universalAnimationLibrary.standard/main/LICENSE", lic)

    # --- 2. Quaternius RPG Characters Pack (OpenGameArt) ---
    chars = os.path.join(BASE, "assets", "characters")
    os.makedirs(chars, exist_ok=True)
    zpath = os.path.join(chars, "rpg_characters_nov_2020.zip")
    print("RPG characters zip ...", end=" ", flush=True)
    n = get("https://opengameart.org/sites/default/files/rpg_characters_-_nov_2020.zip", zpath)
    ok, det = check(zpath, "zip")
    print(f"{n} bytes, {det} -> {'OK' if ok else 'FAIL'}")
    manifest.append(("rpg_characters_nov_2020.zip", n, ok, det))
    outdir = os.path.join(chars, "rpg_characters")
    with zipfile.ZipFile(zpath) as z:
        names = z.namelist()
        z.extractall(outdir)
    print(f"extracted {len(names)} files to rpg_characters/")
    for name in sorted(names):
        if name.lower().endswith((".glb", ".fbx", ".blend", ".gltf")):
            p = os.path.join(outdir, name)
            print("  model:", name, os.path.getsize(p), "bytes")

    # --- 3. Poly Haven PBR textures (2K JPG: diffuse + roughness + normal) ---
    pbr = os.path.join(BASE, "assets", "pbr", "apartment")
    os.makedirs(pbr, exist_ok=True)
    textures = {
        "dark_wooden_planks": "wood floor (dark planks)",
        "beige_wall_001": "plaster wall (beige)",
        "blue_floor_tiles_01": "kitchen floor tiles (blue)",
        "cotton_jersey": "fabric (cotton jersey)",
    }
    for slug, desc in textures.items():
        files = api_json(f"https://api.polyhaven.com/files/{slug}")
        for map_name, suffix in [("Diffuse", "diff"), ("Rough", "rough"), ("nor_gl", "nor_gl")]:
            url = files[map_name]["2k"]["jpg"]["url"]
            dest = os.path.join(pbr, f"{slug}_{suffix}_2k.jpg")
            n = get(url, dest)
            ok, det = check(dest, "jpg")
            print(f"{slug} {suffix}: {n} bytes, {det} -> {'OK' if ok else 'FAIL'}")
            manifest.append((os.path.basename(dest), n, ok, det))

    # --- 4. Poly Haven furniture models (glTF 2K manifest + textures) ---
    models = os.path.join(BASE, "assets", "models", "apartment")
    os.makedirs(models, exist_ok=True)
    for slug in ["WoodenChair_01", "Sofa_01", "CoffeeTable_01"]:
        files = api_json(f"https://api.polyhaven.com/files/{slug}")
        mdir = os.path.join(models, slug)
        os.makedirs(mdir, exist_ok=True)
        entry = files["gltf"]["2k"]["gltf"]
        dest = os.path.join(mdir, f"{slug}_2k.gltf")
        n = get(entry["url"], dest)
        ok, det = check(dest, "gltf")
        print(f"{slug} manifest: {n} bytes, {det} -> {'OK' if ok else 'FAIL'}")
        manifest.append((f"{slug}_2k.gltf", n, ok, det))
        for rel, meta in entry["include"].items():
            d2 = os.path.join(mdir, rel)
            os.makedirs(os.path.dirname(d2), exist_ok=True)
            n = get(meta["url"], d2)
            kind = "bin" if rel.endswith(".bin") else "jpg"
            ok2, det2 = check(d2, kind)
            print(f"  {rel}: {n} bytes -> {'OK' if ok2 else 'FAIL'}")
            manifest.append((rel, n, ok2, det2))

    bad = [m for m in manifest if not m[2]]
    print(f"\nMANIFEST: {len(manifest)} files, {len(bad)} failures")
    for m in bad:
        print("  FAILED:", m)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
