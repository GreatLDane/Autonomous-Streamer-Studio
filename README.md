# ⚡ The Autonomous Streamer Studio
> **GPU-Accelerated Gaming Clips & Shorts Powered by Agentic AI & Local Hardware Encoding**

Turn your gaming PC into a private, hardware-accelerated post-production studio. No $30–$50/month cloud clipper subscriptions (like Opus Clip or Munch), no manual timeline dragging in Premiere, and zero copyright strikes from background stream music.

The architecture combines a **Cloud AI Brain** (Google Antigravity powered by Gemini, Cursor, or Claude Code) with **Local GPU Muscle** (NVIDIA NVENC hardware encoding + FFmpeg).

---

## 🎯 What This Solves

| Traditional Creator Nightmare | The Autonomous Studio Reality |
| :--- | :--- |
| **Hours of Manual Editing:** Dragging crop boxes & keyframing in Premiere after a 4-hour stream. | **Turnkey Automation:** Play your game, tap one hotkey (`Num 0`), and your AI agent renders 4 days of content in 20 seconds. |
| **Cloud Clipper Costs:** Paying $30–$50/mo for web apps that throttle quality and add watermarks. | **100% Free & Local:** Powered by your own NVIDIA RTX GPU using NVENC hardware acceleration. |
| **Copyright Strikes:** Background Spotify / Apple Music music getting your clips muted or claimed. | **Multi-Track Isolation:** Automatically isolates clean in-game sound (Track 2), stripping music completely. |
| **In-Game FPS Drops:** Video rendering making your games stutter or drop frames. | **Process Priority Shield:** Enforces Windows background priority (`BELOW_NORMAL`), guaranteeing smooth gameplay. |

---

## 🚀 Quick Start (Under 3 Minutes)

### 1. Requirements
* **OS:** Windows 10 / 11
* **GPU:** NVIDIA GeForce RTX / GTX (supports NVENC hardware encoding)
* **Software:**
  * [OBS Studio](https://obsproject.com/) (Free)
  * [FFmpeg](https://ffmpeg.org/) (Free)
  * Python 3.10+ (with `Pillow`)

### 2. Configure OBS Multi-Track Audio
Follow the 60-second visual checklist in [`setup_obs_multitrack.md`](./setup_obs_multitrack.md) to separate your game sound from your stream music.

### 3. Run the Studio Renderer
To render a 45-second vertical Short with instant blurred background framing and interactive debate banners:

```bash
python studio_turbo_render.py \
  --input "C:\Users\YourName\Videos\Replay.mp4" \
  --title "TOP BIN STRIKE!" \
  --question "COULD THE GOALIE SAVE THIS?!" \
  --footer "YOUR CHANNEL | DROP A COMMENT" \
  --accent cyan \
  --output "short_top_bin.mp4"
```

*Render time: ~4.5 seconds on an RTX GPU (8x to 10x realtime encoding).*

---

## 🤖 Automating With Your AI Agent

Don't want to type commands? Hand the keys over to your AI coding agent (Antigravity, Cursor, Claude Code, etc.):

1. Open [`agent_prompt_template.txt`](./agent_prompt_template.txt).
2. Paste the prompt to your agent:
   > *"Scan my recording folder, pick the best highlights from tonight's session, and render 4 days of scheduled Shorts with engaging debate questions."*
3. Sit back and watch your agent inspect video frames, generate brand-matched typography, and deliver finished MP4s ready to post.

---

## 📁 Repository Structure
```text
Autonomous-Streamer-Studio/
├── README.md                      # This overview and quick start
├── setup_obs_multitrack.md        # Step-by-step OBS audio track configuration
├── studio_turbo_render.py         # Hardware-accelerated Python rendering engine
├── agent_prompt_template.txt      # Master prompt for your AI assistant
└── bts_short_script.md            # Script & storyboard for the viral BTS Short
```
