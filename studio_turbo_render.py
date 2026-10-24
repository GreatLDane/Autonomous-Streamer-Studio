#!/usr/bin/env python3
"""
Autonomous Streamer Studio - Turbo Render Engine
================================================
A standalone GPU-accelerated video rendering engine designed for game streamers.
Transforms raw 16:9 OBS Replay Buffer gameplay recordings into high-retention 9:16 Shorts
with clean multitrack audio selection, dynamic text banners, and ultra-fast NVENC encoding.

Features:
- Sub-5-second 1080x1920 60FPS renders using NVIDIA NVENC hardware acceleration.
- Automatic multitrack audio extraction (Track 2 clean game audio by default, zero copyright risk).
- Automatic Pillow-generated typography overlays with accent color palettes.
- Low-priority background processing (runs in the background while you game without dropped frames).
- Automatic CPU fallback if no NVIDIA GPU is detected.
"""

import os
import sys
import argparse
import subprocess
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Preset accent colors (RGB)
ACCENT_PALETTES = {
    "cyan": {"primary": (0, 240, 255), "name": "Cyber Cyan"},
    "red": {"primary": (255, 60, 60), "name": "Danger Red"},
    "green": {"primary": (0, 255, 120), "name": "Neon Emerald"},
    "amber": {"primary": (255, 180, 0), "name": "Solar Gold"},
    "purple": {"primary": (180, 70, 255), "name": "Electric Violet"},
}

def get_best_font(size: int, bold: bool = False):
    """Attempt to locate high-quality system sans-serif fonts; fall back gracefully."""
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "impact.ttf" if bold else "calibri.ttf",
        "segui_bl.ttf" if bold else "segoeui.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except (OSError, IOError):
            continue
    try:
        return ImageFont.load_default()
    except Exception:
        return None

def generate_overlay_card(
    width: int,
    height: int,
    title: str,
    subtitle: str,
    footer: str,
    accent_name: str,
    output_png: Path
):
    """Generates a transparent 1080x1920 PNG containing the top headline and bottom footer."""
    accent_info = ACCENT_PALETTES.get(accent_name.lower(), ACCENT_PALETTES["cyan"])
    accent_rgb = accent_info["primary"]

    card = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)

    # 1. Top Card (Title + Subtitle)
    top_y_start = 140
    top_box_height = 240
    top_box_pad = 60

    # Gradient/tinted dark background for readability
    top_box = [
        top_box_pad,
        top_y_start,
        width - top_box_pad,
        top_y_start + top_box_height
    ]
    draw.rounded_rectangle(top_box, radius=24, fill=(10, 15, 24, 215), outline=(*accent_rgb, 200), width=3)

    # Header Accent Pill
    pill_w = 260
    pill_h = 8
    pill_x0 = (width - pill_w) // 2
    draw.rounded_rectangle([pill_x0, top_y_start + 18, pill_x0 + pill_w, top_y_start + 18 + pill_h], radius=4, fill=accent_rgb)

    # Title Text
    font_title = get_best_font(54, bold=True)
    if font_title:
        title_bbox = draw.textbbox((0, 0), title, font=font_title)
        title_w = title_bbox[2] - title_bbox[0]
        title_x = (width - title_w) // 2
        draw.text((title_x, top_y_start + 45), title, font=font_title, fill=(255, 255, 255, 255))

    # Subtitle / Hook Text
    font_sub = get_best_font(34, bold=False)
    if font_sub and subtitle:
        sub_bbox = draw.textbbox((0, 0), subtitle, font=font_sub)
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_x = (width - sub_w) // 2
        draw.text((sub_x, top_y_start + 135), subtitle, font=font_sub, fill=(*accent_rgb, 240))

    # 2. Bottom Call-To-Action Card
    if footer:
        bot_y_start = height - 260
        bot_box_h = 100
        bot_box = [
            top_box_pad,
            bot_y_start,
            width - top_box_pad,
            bot_y_start + bot_box_h
        ]
        draw.rounded_rectangle(bot_box, radius=20, fill=(10, 15, 24, 210), outline=(*accent_rgb, 140), width=2)

        font_footer = get_best_font(30, bold=True)
        if font_footer:
            f_bbox = draw.textbbox((0, 0), footer, font=font_footer)
            f_w = f_bbox[2] - f_bbox[0]
            f_x = (width - f_w) // 2
            draw.text((f_x, bot_y_start + 32), footer, font=font_footer, fill=(255, 255, 255, 235))

    card.save(output_png, format="PNG")

def check_nvenc_available() -> bool:
    """Test if h264_nvenc encoder is available in FFmpeg."""
    try:
        proc = subprocess.run(
            ["ffmpeg", "-encoders"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        return "h264_nvenc" in proc.stdout
    except Exception:
        return False

def render_short(
    input_file: Path,
    output_file: Path,
    title: str,
    subtitle: str,
    footer: str,
    accent: str,
    track: int,
    start_sec: float = None,
    duration_sec: float = None
):
    if not input_file.exists():
        print(f"[!] Error: Input file not found: {input_file}")
        sys.exit(1)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    temp_overlay_png = output_file.parent / f"temp_overlay_{int(time.time())}.png"

    print("=" * 60)
    print("  AUTONOMOUS STREAMER STUDIO - TURBO RENDER")
    print("=" * 60)
    print(f"[*] Input File     : {input_file.name}")
    print(f"[*] Title          : {title}")
    print(f"[*] Hook           : {subtitle}")
    print(f"[*] Audio Track    : Track {track} (1-indexed OBS track)")
    print(f"[*] Accent Theme   : {accent.upper()}")

    # 1. Generate text overlay asset
    generate_overlay_card(
        width=1080,
        height=1920,
        title=title,
        subtitle=subtitle,
        footer=footer,
        accent_name=accent,
        output_png=temp_overlay_png
    )

    # 2. Check GPU acceleration
    use_nvenc = check_nvenc_available()
    encoder = "h264_nvenc" if use_nvenc else "libx264"
    print(f"[*] Encoder        : {encoder} ({'NVIDIA GPU Acceleration' if use_nvenc else 'CPU Fallback'})")

    # 3. Construct FFmpeg command
    # Filtergraph: Center crop 16:9 into 9:16 portrait, scale to 1080x1920, force square SAR, overlay PNG card
    filtergraph = (
        "[0:v]crop=w=ih*9/16:h=ih:x=(iw-ow)/2:y=0,scale=1080:1920,setsar=1[vbg];"
        "[vbg][1:v]overlay=0:0[vout]"
    )

    # Map track: In ffmpeg, 0-indexed audio streams correspond to OBS tracks.
    # OBS Track 1 = 0:a:0, Track 2 = 0:a:1, Track 3 = 0:a:2
    ffmpeg_audio_stream = f"0:a:{track - 1}"

    cmd = ["ffmpeg", "-y"]

    if start_sec is not None:
        cmd.extend(["-ss", str(start_sec)])

    cmd.extend(["-i", str(input_file.resolve())])
    cmd.extend(["-i", str(temp_overlay_png.resolve())])

    if duration_sec is not None:
        cmd.extend(["-t", str(duration_sec)])

    cmd.extend([
        "-filter_complex", filtergraph,
        "-map", "[vout]",
        "-map", ffmpeg_audio_stream,
        "-c:v", encoder
    ])

    if use_nvenc:
        cmd.extend(["-preset", "p5", "-cq", "22"])
    else:
        cmd.extend(["-preset", "veryfast", "-crf", "22"])

    cmd.extend([
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-pix_fmt", "yuv420p",
        "-aspect", "9:16",
        str(output_file.resolve())
    ])

    # Windows process priority: BELOW_NORMAL_PRIORITY_CLASS (0x00004000)
    creation_flags = 0x00004000 if os.name == "nt" else 0

    print(f"\n[+] Rendering starting... (Target: {output_file.name})")
    start_t = time.time()

    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=creation_flags
    )

    elapsed = time.time() - start_t

    # Clean up temporary overlay PNG
    if temp_overlay_png.exists():
        try:
            temp_overlay_png.unlink()
        except Exception:
            pass

    if proc.returncode != 0:
        print("[!] Rendering failed with FFmpeg error:")
        print(proc.stderr[-1000:])
        sys.exit(1)

    file_size_mb = output_file.stat().st_size / (1024 * 1024)
    print("\n" + "=" * 60)
    print(f" [SUCCESS] Render completed in {elapsed:.2f} seconds!")
    print(f" File Size : {file_size_mb:.2f} MB")
    print(f" Output    : {output_file.resolve()}")
    print("=" * 60 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="Autonomous Streamer Studio - GPU Turbo Video Renderer"
    )
    parser.add_argument("--input", "-i", required=True, help="Path to input 16:9 gameplay recording (.mp4)")
    parser.add_argument("--output", "-o", required=True, help="Path to output 9:16 video (.mp4)")
    parser.add_argument("--title", "-t", default="STREAM HIGHLIGHT", help="Top headline text")
    parser.add_argument("--question", "-q", default="DID YOU SEE THAT?", help="Secondary hook/question text")
    parser.add_argument("--footer", "-f", default="SUBSCRIBE FOR DAILY CLIPS", help="Bottom CTA text")
    parser.add_argument("--accent", "-a", default="cyan", choices=list(ACCENT_PALETTES.keys()), help="Accent color theme")
    parser.add_argument("--track", type=int, default=2, help="OBS Audio track (1=Mix, 2=Game, 3=Mic). Default: 2")
    parser.add_argument("--start", type=float, default=None, help="Start trim offset in seconds")
    parser.add_argument("--duration", type=float, default=None, help="Duration in seconds")

    args = parser.parse_args()

    render_short(
        input_file=Path(args.input),
        output_file=Path(args.output),
        title=args.title,
        subtitle=args.question,
        footer=args.footer,
        accent=args.accent,
        track=args.track,
        start_sec=args.start,
        duration_sec=args.duration
    )

if __name__ == "__main__":
    main()
