import gradio as gr
import os
from . import models

def _read_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def create_project(title, input_path, voice, sample_rate, bitrate):
    if not os.path.exists(input_path):
        return "Input file not found.", gr.update()
    job_id = models.create_job(title, input_path, voice, sample_rate, bitrate)
    text = _read_text(input_path)
    models.add_chapters(job_id, text)
    return f"Queued job #{job_id} – {title}", refresh_jobs()

def refresh_jobs():
    jobs = models.list_jobs()
    rows = []
    for j in jobs:
        chapters = models.list_chapters(j["id"])
        done = sum(1 for c in chapters if c["status"] == "done")
        total = len(chapters)
        pct = (done / total * 100) if total else 0
        rows.append([j["id"], j["title"], j["status"], f"{done}/{total}", f"{pct:.1f}%"])
    return rows

def build_ui(orch):
    with gr.Blocks(title="Ebook2Audiobook v2 - Project Manager") as demo:
        gr.Markdown("## v2 Project Manager — Queue • Resume • 2 Workers (Phase-1)")
        with gr.Tab("Projects"):
            with gr.Row():
                title = gr.Textbox(label="Project Title", value="My Book")
                input_path = gr.Textbox(label="Input .txt path")
            with gr.Row():
                voice = gr.Textbox(label="Voice Preset (name)", value="Snape_Recount")
                sample_rate = gr.Number(label="Sample Rate (Hz)", value=22050, precision=0)
                bitrate = gr.Number(label="Bitrate (kbps)", value=160, precision=0)
            out = gr.Textbox(label="Status", interactive=False)
            add_btn = gr.Button("Add Project")
            jobs_tbl = gr.Dataframe(headers=["ID","Title","Status","Chapters (done/total)","Progress"], interactive=False)
            add_btn.click(create_project, [title, input_path, voice, sample_rate, bitrate], [out, jobs_tbl])
            refresh = gr.Button("Refresh")
            refresh.click(refresh_jobs, None, jobs_tbl)
    return demo
