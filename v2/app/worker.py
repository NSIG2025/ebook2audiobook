import os, time
from . import models

# Phase-1.1: replace this stub with a call into the real converter
def render_chapter_stub(text, out_wav):
    try:
        import wave, struct
        fr = 22050
        dur = 1.0
        nframes = int(fr*dur)
        with wave.open(out_wav, 'w') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(fr)
            for _ in range(nframes):
                w.writeframes(struct.pack("<h", 0))
        time.sleep(0.5)
    except Exception:
        time.sleep(1.0)

def process_chapter(chapter, out_root):
    models.mark_status("chapters", chapter["id"], "running")
    proj_dir = os.path.join(out_root, f"job_{chapter['job_id']}")
    os.makedirs(proj_dir, exist_ok=True)
    out_wav = os.path.join(proj_dir, f"chapter_{chapter['seq']:03d}.wav")

    # Phase-1: placeholder text; Phase-1.1 will store/resolve real text
    text = f"[chapter {chapter['seq']}]"
    render_chapter_stub(text, out_wav)

    models.set_artifact(chapter["id"], out_wav)
