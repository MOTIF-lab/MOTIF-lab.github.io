#!/usr/bin/env python3
"""normalize_images.py — one-off: turn the raw photos in static/img/{gallery,team} and the home banner into clean sRGB JPEGs
under assets/img/ (Hugo image processing source), max edge 2000 px, quality 85, progressive, NO EXIF/ICC (strips GPS and
device metadata). Prints before/after sizes and the GPS tags found. Originals are removed from static/."""
import os, sys, glob
from PIL import Image, ImageOps, ImageCms
LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOBS = [("static/img/gallery", "assets/img/gallery"), ("static/img/team", "assets/img/team")]
BANNER = ("static/img/homepage-banner.png", "assets/img/brand/homepage-banner.jpg")

def to_srgb(im):
    icc = im.info.get("icc_profile")
    if im.mode == "CMYK":
        try:
            if icc:
                import io
                src = ImageCms.ImageCmsProfile(io.BytesIO(icc)); dst = ImageCms.createProfile("sRGB")
                return ImageCms.profileToProfile(im, src, dst, outputMode="RGB")
        except Exception: pass
        return im.convert("RGB")
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); bg = Image.new("RGB", im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[-1]); return bg
    return im.convert("RGB")

def process(src, dst, max_edge=2000, quality=85):
    im = Image.open(src); gps = len(im.getexif().get_ifd(0x8825)) if hasattr(im, "getexif") else 0
    fmt, mode, size0 = im.format, im.mode, im.size
    im = ImageOps.exif_transpose(im); im = to_srgb(im)
    if max(im.size) > max_edge:
        r = max_edge / max(im.size); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, "JPEG", quality=quality, optimize=True, progressive=True)   # no exif=, no icc_profile= → metadata dropped
    chk = Image.open(dst); assert not chk.getexif().get_ifd(0x8825), "GPS survived"
    print(f"{os.path.relpath(src, LAB):44s} {fmt:5s} {mode:5s} {size0[0]}x{size0[1]} {os.path.getsize(src)/1e6:5.2f} MB gps={gps}  →  {os.path.relpath(dst, LAB)} {im.width}x{im.height} {os.path.getsize(dst)/1e6:4.2f} MB")

def main():
    for sdir, ddir in JOBS:
        for src in sorted(glob.glob(os.path.join(LAB, sdir, "*.*"))):
            base = os.path.splitext(os.path.basename(src))[0]
            if base == ".gitkeep" or src.endswith(".gitkeep"): continue
            process(src, os.path.join(LAB, ddir, base + ".jpg"))
            os.remove(src)
    process(os.path.join(LAB, *BANNER[0].split("/")), os.path.join(LAB, *BANNER[1].split("/")), max_edge=2000, quality=88)
    os.remove(os.path.join(LAB, *BANNER[0].split("/")))

if __name__ == "__main__": main()
