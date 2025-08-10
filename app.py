# videoconverter.py
import os, shutil, subprocess, tempfile, mimetypes
from pathlib import Path
import gradio as gr

VIDEO_OUTS = ["mp4", "avi", "flv", "mov", "wmv", "mkv", "webm"]
AUDIO_OUTS = ["mp3", "wav", "flac", "ogg", "m4a", "aac", "wma"]

L = {
    "id": {
        "title": "Free Video Converter",
        "subtitle": "Pilih/drag file. Format yang sama dengan input disembunyikan otomatis.",
        "choose_target": "Pilih target",
        "to_video": "ke video",
        "to_audio": "ke audio",
        "upload_label": "Unggah file video/audio",
        "status_ready": "Siap. Unggah file untuk mulai.",
        "crf": "CRF H.264 (lebih kecil = lebih bagus)",
        "preset": "Preset sangat cepat (ultrafast)",
        "convert": "Convert",
        "downlabel": "Unduh hasil",
        "detected_video": "Terdeteksi video. Format input disembunyikan otomatis.",
        "detected_audio": "Terdeteksi audio. Grup video dinonaktifkan.",
        "need_file": "Pilih file dulu.",
        "need_target": "Pilih format tujuan (klik salah satu chip).",
        "no_ffmpeg": "FFmpeg tidak ditemukan. Install ffmpeg terlebih dahulu.",
        "fmt_unsupported": "Format {fmt} belum didukung.",
        "fail_convert": "Gagal konversi: {err}",
        "error": "Error: {err}",
        "done_toast": "Selesai: {name}",
        "processing_status": "⏳ Sedang mengonversi… harap tunggu.",
        "processing_toast": "Sedang mengonversi…",
        "lang_label": "Bahasa",
        "lang_id": "🇮🇩 Indonesia",
        "lang_en": "🇺🇸 English",
        "please_wait": "Sedang mengonversi…",
      },
    "en": {
        "title": "Free Video Converter",
        "subtitle": "Pick/drag files. Input’s identical format is hidden automatically.",
        "choose_target": "Choose a target",
        "to_video": "to video",
        "to_audio": "to audio",
        "upload_label": "Upload video/audio file",
        "status_ready": "Ready. Upload a file to start.",
        "crf": "CRF H.264 (lower = better quality)",
        "preset": "Ultra fast preset (ultrafast)",
        "convert": "Convert",
        "downlabel": "Download result",
        "detected_video": "Video detected. Input format hidden automatically.",
        "detected_audio": "Audio detected. Video group disabled.",
        "need_file": "Please choose a file first.",
        "need_target": "Pick a target format (click one of the chips).",
        "no_ffmpeg": "FFmpeg not found. Please install ffmpeg.",
        "fmt_unsupported": "Format {fmt} is not supported.",
        "fail_convert": "Convert failed: {err}",
        "error": "Error: {err}",
        "done_toast": "Done: {name}",
        "processing_status": "⏳ Converting… please wait.",
        "processing_toast": "Converting…",
        "lang_label": "Language",
        "lang_id": "🇮🇩 Indonesian",
        "lang_en": "🇺🇸 English",
        "please_wait": "Converting…",
    },
}

def t(k, lang): return L.get(lang, L["id"]).get(k, k)
def _ext(n): return (Path(n).suffix or "").lower().lstrip(".")
def _is_video(n):
    mt,_ = mimetypes.guess_type(n); return (mt or "").startswith("video")
def _is_audio(n):
    mt,_ = mimetypes.guess_type(n); return (mt or "").startswith("audio")
def _ffmpeg_exists(): return shutil.which("ffmpeg") is not None

# ---------- Suggestions ----------
def suggest_targets(file, lang):
    reset_dl = gr.update(value=None, visible=False)
    if not file:
        return (gr.update(choices=[], value=None, interactive=True),
                gr.update(choices=[], value=None, interactive=True),
                None, t("status_ready", lang), reset_dl)
    name = Path(file.name).name
    same = _ext(name)
    if _is_video(name):
        v = [f for f in VIDEO_OUTS if f != same]
        a = [f for f in AUDIO_OUTS if f != same]
        default = "mp4" if "mp4" in v else (v[0] if v else (a[0] if a else None))
        return (gr.update(choices=v, value=(default if default in v else None), interactive=True),
                gr.update(choices=a, value=None, interactive=True),
                default, t("detected_video", lang), reset_dl)
    # audio
    v = [f for f in VIDEO_OUTS if f != same]
    a = [f for f in AUDIO_OUTS if f != same]
    default = "mp3" if "mp3" in a else (a[0] if a else None)
    return (gr.update(choices=v, value=None, interactive=False),
            gr.update(choices=a, value=default, interactive=True),
            default, t("detected_audio", lang), reset_dl)

def pick_video(fmt): return fmt, gr.update(value=None), gr.update(value=None, visible=False)
def pick_audio(fmt): return fmt, gr.update(value=None), gr.update(value=None, visible=False)

# ---------- Convert ----------
def convert(file, target_fmt, crf, super_fast, lang):
    if not file:        return gr.update(value=None, visible=False), t("need_file", lang)
    if not target_fmt:  return gr.update(value=None, visible=False), t("need_target", lang)
    if not _ffmpeg_exists(): return gr.update(value=None, visible=False), t("no_ffmpeg", lang)

    in_path = Path(file.name)
    work = Path(tempfile.mkdtemp(prefix="vc_"))
    src = work / in_path.name
    shutil.copyfile(in_path, src)

    out_name = f"{in_path.stem}.{target_fmt}"
    dst = work / out_name
    args = ["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(src)]

    if target_fmt in ("mp4","mov"):
        args += ["-c:v","libx264","-preset",("ultrafast" if super_fast else "veryfast"),
                 "-pix_fmt","yuv420p","-crf",str(crf),"-c:a","aac","-b:a","192k"]
    elif target_fmt in ("webm","mkv"):
        args += ["-c:v","libvpx-vp9","-b:v","1200k","-c:a","libopus","-b:a","128k"]
    elif target_fmt=="avi":
        args += ["-c:v","mpeg4","-qscale:v","6","-c:a","mp2","-b:a","192k"]
    elif target_fmt=="flv":
        args += ["-c:v","flv","-b:v","1M","-c:a","libmp3lame","-b:a","160k"]
    elif target_fmt=="wmv":
        args += ["-c:v","wmv2","-b:v","1M","-c:a","wmav2","-b:a","160k"]
    elif target_fmt=="mp3":
        args += ["-vn","-c:a","libmp3lame","-b:a","192k"]
    elif target_fmt=="wav":
        args += ["-vn","-c:a","pcm_s16le","-ar","44100","-ac","2"]
    elif target_fmt=="flac":
        args += ["-vn","-c:a","flac"]
    elif target_fmt=="ogg":
        args += ["-vn","-c:a","libopus","-b:a","128k","-f","ogg"]
    elif target_fmt=="m4a":
        args += ["-vn","-c:a","aac","-b:a","192k"]
    elif target_fmt=="aac":
        args += ["-vn","-c:a","aac","-b:a","192k","-f","adts"]
    elif target_fmt=="wma":
        args += ["-vn","-c:a","wmav2","-b:a","160k"]
    else:
        shutil.rmtree(work, ignore_errors=True)
        return gr.update(value=None, visible=False), t("fmt_unsupported", lang).format(fmt=target_fmt)

    args += [str(dst)]
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        shutil.rmtree(work, ignore_errors=True)
        return gr.update(value=None, visible=False), t("fail_convert", lang).format(err=e)
    except Exception as e:
        shutil.rmtree(work, ignore_errors=True)
        return gr.update(value=None, visible=False), t("error", lang).format(err=e)

    gr.Info(t("done_toast", lang).format(name=out_name))
    return gr.update(value=str(dst), visible=True, label=t("downlabel", lang)), t("done_toast", lang).format(name=out_name)

# ---------- Lock / Unlock + MODAL “please wait” ----------
def begin_processing(lang):
    gr.Info(t("processing_toast", lang))
    return (
        gr.update(interactive=False),  # file_in
        gr.update(interactive=False),  # video_radio
        gr.update(interactive=False),  # audio_radio
        gr.update(interactive=False),  # crf
        gr.update(interactive=False),  # super_fast
        gr.update(interactive=False),  # btn convert
        gr.update(value=None, visible=False),  # download button
        t("processing_status", lang),          # status text
        gr.update(visible=True),               # SHOW modal
    )

def end_processing():
    return (
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(visible=False),              # HIDE modal
    )

def switch_lang(choice, lang_state):
    code = "id" if "🇮🇩" in (choice or "") else "en"
    return (
        code,
        gr.update(value=f"<h2>{t('title', code)}</h2><p style='color:#64748b'>{t('subtitle', code)}</p>"),
        gr.update(label=t("upload_label", code)),
        gr.update(value="### " + t("choose_target", code)),
        gr.update(label=t("to_video", code)),
        gr.update(label=t("to_audio", code)),
        gr.update(label=t("crf", code)),
        gr.update(label=t("preset", code)),
        gr.update(value=t("convert", code)),
        gr.update(label=t("downlabel", code)),
        t("status_ready", code),
        # modal content will change language too
        gr.update(value=wait_html(code)),
    )

# ---------- UI ----------
def wait_html(lang):
    return f"""
<div class="wait-overlay">
  <div class="wait-card">
    <div class="spinner"></div>
    <div class="msg">{t('please_wait', lang)}</div>
  </div>
</div>
"""

CSS = """
.wrap {max-width:1200px;margin:24px auto;}
.card {background:#fff;border:1px solid #e5e7eb;border-radius:18px;box-shadow:0 12px 40px rgba(2,6,23,.08);padding:18px}
.g-row {display:grid;grid-template-columns:1fr 420px;gap:24px}
@media (max-width:980px){.g-row{grid-template-columns:1fr}}
.targets {background:#eef2f7;border:1px solid #cdd5df;border-radius:14px;padding:14px}
.lang {display:flex;gap:10px;align-items:center;justify-content:flex-end;margin:0 0 8px}
.dl .gr-button {background:linear-gradient(90deg,#10b981,#22c55e)!important;color:#fff!important;border:none!important;
                box-shadow:0 10px 22px rgba(16,185,129,.25)}
.dl .gr-button:disabled{opacity:.5}

/* ===== Modal “please wait” ===== */
.wait-overlay{position:fixed;inset:0;background:rgba(9,9,11,.55);
  display:flex;align-items:center;justify-content:center;z-index:9999}
.wait-card{background:#111827;color:#e5e7eb;border:1px solid #334155;border-radius:14px;
  box-shadow:0 20px 60px rgba(0,0,0,.35);padding:20px 24px;min-width:260px;display:flex;gap:12px;align-items:center}
.spinner{width:22px;height:22px;border:3px solid #475569;border-top-color:#22c55e;border-radius:50%;animation:spin .9s linear infinite}
.msg{font-weight:700}
@keyframes spin{to{transform:rotate(360deg)}}
"""

with gr.Blocks(css=CSS, title="Free Video Converter") as demo:
    lang = gr.State(value="id")

    with gr.Row(elem_classes="wrap lang"):
        lang_dd = gr.Dropdown(
            choices=[L["id"]["lang_id"], L["en"]["lang_en"]],
            value=L["id"]["lang_id"],
            label=L["id"]["lang_label"],
            allow_custom_value=False,
        )

    header_md = gr.Markdown(
        f"<div class='wrap'><div class='card'>"
        f"<h2>{t('title','id')}</h2>"
        f"<p style='color:#64748b'>{t('subtitle','id')}</p></div></div>"
    )

    with gr.Row(elem_classes="wrap g-row"):
        with gr.Column():
            file_in = gr.File(label=t("upload_label","id"), file_count="single", type="filepath")
            status = gr.Markdown(t("status_ready","id"))
        with gr.Column(elem_classes="targets"):
            target_title = gr.Markdown("### " + t("choose_target","id"))
            video_radio = gr.Radio(choices=[], label=t("to_video","id"), interactive=True)
            audio_radio = gr.Radio(choices=[], label=t("to_audio","id"), interactive=True)
            target = gr.State(value=None)

    with gr.Row(elem_classes="wrap"):
        crf = gr.Slider(1, 35, value=24, step=1, label=t("crf","id"))
        super_fast = gr.Checkbox(value=True, label=t("preset","id"))

    with gr.Column(elem_classes="wrap"):
        btn = gr.Button(value=t("convert","id"), variant="primary")
        download_btn = gr.DownloadButton(label=t("downlabel","id"), value=None, visible=False, elem_classes="dl")

    # MODAL (HTML) — awalnya hidden; isinya ikut bahasa
    wait_modal = gr.HTML(wait_html("id"), visible=False)

    # language change (update teks + modal content)
    lang_dd.change(
        switch_lang,
        inputs=[lang_dd, lang],
        outputs=[lang, header_md, file_in, target_title, video_radio, audio_radio, crf, super_fast, btn, download_btn, status, wait_modal],
    )

    file_in.change(
        suggest_targets,
        inputs=[file_in, lang],
        outputs=[video_radio, audio_radio, target, status, download_btn],
    )
    video_radio.change(pick_video, inputs=[video_radio], outputs=[target, audio_radio, download_btn])
    audio_radio.change(pick_audio, inputs=[audio_radio], outputs=[target, video_radio, download_btn])

    # lock → show modal → convert → hide modal + unlock
    (btn.click(
        begin_processing,
        inputs=[lang],
        outputs=[file_in, video_radio, audio_radio, crf, super_fast, btn, download_btn, status, wait_modal],
        queue=False
     ).then(
        convert,
        inputs=[file_in, target, crf, super_fast, lang],
        outputs=[download_btn, status],
        show_progress="full"
     ).then(
        end_processing,
        inputs=None,
        outputs=[file_in, video_radio, audio_radio, crf, super_fast, btn, wait_modal],
        queue=False
     ))

demo.queue(max_size=12, default_concurrency_limit=2)
if __name__ == "__main__":
    demo.launch(share=False)
