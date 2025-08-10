---

# 🎬 Free Video Converter (Gradio + FFmpeg)

A lightweight Gradio web app to convert **video ⇄ video** and **video/audio ⇄ audio** locally using FFmpeg.
Upload a file, pick a target format, watch the progress pop-up, then download the result—fast and simple.

[![Live Demo on Hugging Face](https://img.shields.io/badge/Live%20Demo-Hugging%20Face-orange?style=for-the-badge&logo=huggingface)](https://huggingface.co/spaces/salman555/video-converter)
![Visitor Count](https://profile-counter.glitch.me/salmanalfarisi11/count.svg)

---

## 📑 Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Running Locally](#running-locally)
6. [Usage](#usage)
7. [Settings (CRF & Preset)](#settings-crf--preset)
8. [Deploy to Hugging Face](#deploy-to-hugging-face)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)
11. [License](#license)
12. [Author & Credits](#author--credits)

---

## ✨ Features

* **Many Formats, One Click**

  * **Video targets:** `mp4`, `avi`, `flv`, `mov`, `wmv`, `mkv`, `webm`
  * **Audio targets:** `mp3`, `wav`, `flac`, `ogg`, `m4a`, `aac`, `wma`

* **Smart Targeting**
  Input format is automatically hidden from the target list; defaults to **mp4** (video) or **mp3** (audio).

* **Language Switcher (🇮🇩 / 🇺🇸)**
  Toggle Indonesian/English texts on the fly.

* **Progress Pop-up & UI Lock**
  A “Converting… please wait.” modal appears, and all controls are disabled until the job is done.

* **One-click Download**
  A green **Download result** button appears once conversion finishes.

* **CPU-friendly**
  Optimized defaults for 2 vCPU (e.g., Hugging Face Spaces), with Gradio queue limits pre-tuned.

* **Local / Offline**
  Runs entirely on your machine/Space; no third-party upload.

---

## 📁 Project Structure

```
videoconverter/
├── videoconverter.py         # Gradio app (ID/EN, progress modal, downloader)
├── requirements.txt          # Python deps (e.g., gradio)
├── apt.txt                   # System deps for Spaces (ffmpeg)
├── LICENSE                   # "All Rights Reserved"
├── README.md
└── .gitignore
```

> **Note:** The app expects `ffmpeg` to be available on the system (also installs via `apt.txt` on Spaces).

---

## ⚙️ Prerequisites

* **Python 3.10+**
* **FFmpeg** (includes `ffmpeg` and `ffprobe`)
* `git` & a terminal

Install FFmpeg locally:

**Ubuntu/Debian**

```bash
sudo apt update && sudo apt install -y ffmpeg
```

**macOS (Homebrew)**

```bash
brew install ffmpeg
```

**Windows (winget)**

```powershell
winget install Gyan.FFmpeg
```

---

## 🔧 Installation

1. Clone this repository:

```bash
git clone https://github.com/salmanalfarisi11/video-converter.git
cd video-converter
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Running Locally

Start the app:

```bash
python videoconverter.py
```

* Default URL: [http://127.0.0.1:7860](http://127.0.0.1:7860)
* Want a temporary public link? Set `share=True` in `demo.launch(...)`.

---

## 🎯 Usage

1. **Upload** a video or audio file.
2. **Choose a target** format (to video / to audio).
3. (Optional) Set **CRF** and **Ultra fast preset**.
4. Click **Convert**. A modal “Converting…” appears and the UI is locked.
5. When done, click the **Download result** button to save your file.

---

## ⚙️ Settings (CRF & Preset)

* **CRF H.264 (lower = better quality)**

  * Applies to H.264 outputs (e.g., **mp4**, **mov**).
  * Typical range: **18–28**.
  * **Lower CRF → higher quality & bigger file**, conversion a bit slower.
  * **Higher CRF → smaller file**, conversion faster.

* **Ultra fast preset (ultrafast)**

  * Uses `-preset ultrafast` for **libx264** to speed up CPU encoding at the cost of larger files.
  * Uncheck it if you prefer better compression (smaller size) with **slower** conversion.

---

## ☁️ Deploy to Hugging Face

1. Create a **New Space** → **Gradio** → (Public or Private).

2. Upload these files:

   * `videoconverter.py`
   * `requirements.txt` (e.g., `gradio==5.32.1`)
   * `apt.txt` with:

     ```
     ffmpeg
     ```
   * `README.md`, `LICENSE`, `.gitignore` (optional but recommended)

3. In **README.md**, you can add HF metadata front-matter (optional):

```yaml
---
title: Free Video Converter
emoji: 🎬
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 5.32.1
app_file: videoconverter.py
license: other   # proprietary
pinned: false
---
```

The Space will build and run automatically.

---

## 🛠️ Troubleshooting

* **“FFmpeg not found”**
  Ensure `ffmpeg` is installed and on your PATH (`ffmpeg -version`). On Spaces, keep `ffmpeg` inside `apt.txt`.

* **Conversion is slow**

  * Enable **Ultra fast preset**.
  * Use a **higher CRF** for H.264.
  * Prefer **mp4**/**mp3** which are typically faster on CPU.

* **Out of storage** (Spaces with small disks)

  * Delete large outputs frequently.
  * Reduce file sizes using higher CRF or lower bitrates.

---

## 🤝 Contributing

Bug reports, suggestions, or PRs are welcome (even though the code is proprietary, you can propose changes via issues/patches if the repo is public).

---

## 📄 License

**All Rights Reserved** — see [LICENSE](LICENSE).
You may **not** copy, modify, redistribute, or use this software without explicit permission from the copyright holder.

---

## 🖋️ Author & Credits

Developed by **[Salman Alfarisi](https://github.com/salmanalfarisi11)** © 2025

* GitHub: [salmanalfarisi11](https://github.com/salmanalfarisi11)
* LinkedIn: [salmanalfarisi11](https://linkedin.com/in/salmanalfarisi11)
* Instagram: [faris.salman111](https://instagram.com/faris.salman111)

Built with ❤️ using **Gradio** and **FFmpeg**.
If this project helps you, please ⭐ the repo!
