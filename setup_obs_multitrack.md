# 🎙️ The "Zero-Copyright" OBS Multi-Track Audio Setup

> **The Secret:** How to listen to full copyrighted music (Spotify, Apple Music, YouTube) on your live stream while recording clips with 100% clean in-game audio.

---

## Step 1: Enable Multi-Track Recording in OBS

1. Open **OBS Studio**.
2. Go to **Settings** > **Output**.
3. At the top, change **Output Mode** from *Simple* to **Advanced**.
4. Click the **Recording** tab.
5. Under **Audio Track**, check the boxes for:
   * ✅ **Track 1**
   * ✅ **Track 2**
   * ✅ **Track 3**
6. Click **Apply**.

---

## Step 2: Route Your Audio Sources (The Audio Matrix)

1. In the main OBS window, look at the **Audio Mixer** panel.
2. Click the gear icon / three dots on any audio source and select **Advanced Audio Properties**.
3. Set your checkboxes to match this exact matrix:

| Audio Source | Track 1 (Stream Mix) | Track 2 (Game Only) | Track 3 (Mic Only) | Purpose |
| :--- | :---: | :---: | :---: | :--- |
| **Desktop Audio / Music** *(Spotify, Apple Music)* | ✅ | ❌ | ❌ | Streamers & live chat hear music; completely excluded from clips. |
| **Game Audio** *(Rocket League, Valorant, Apex)* | ✅ | ✅ | ❌ | Clean game sound effects (engines, boosts, shots, explosions). |
| **Microphone** *(Your Voice)* | ✅ | ❌ | ✅ | Live chat hears you; voice is stored on Track 3 for optional long videos. |

> [!IMPORTANT]
> **Track 1** is sent to Twitch / YouTube Live so your viewers hear everything.  
> **Track 2** contains **pure game audio**, which our rendering script pulls automatically. This makes your Shorts 100% immune to Content ID copyright claims!

---

## Step 3: Configure the 45-Second Replay Buffer

Instead of recording 4-hour video files and wasting hundreds of gigabytes of disk space, use the **Replay Buffer**:

1. In **Settings** > **Output** > **Recording**, click the **Replay Buffer** tab.
2. Check **Enable Replay Buffer**.
3. Set **Maximum Replay Time** to:
   * **`45 seconds`** *(The sweet spot for vertical Shorts).*
4. Go to **Settings** > **Hotkeys**.
5. Find **Replay Buffer: Save Replay** and bind it to a comfortable key:
   * Keyboard: **`Num 0`**
   * Controller: Map to an unused combo (or use a phone button with *OBS Blade*).
6. Click **Start Replay Buffer** in OBS when you begin playing.

Whenever you score an incredible goal or hit a clip, just tap your hotkey—OBS instantly saves only the last 45 seconds to your videos folder!
