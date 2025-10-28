from .db import connect
from hashlib import sha1
import os, math

def create_job(title, input_path, voice_preset, sample_rate, bitrate_kbps):
    with connect() as c:
        cur = c.execute(
            "INSERT INTO jobs(title,input_path,voice_preset,sample_rate,bitrate_kbps) VALUES(?,?,?,?,?)",
            (title, input_path, voice_preset, sample_rate, bitrate_kbps),
        )
        c.commit()
        return cur.lastrowid

def split_text_into_chapters(text, target_chars=5000):
    parts = []
    n = max(1, math.ceil(len(text)/target_chars))
    for seq in range(n):
        start = seq*target_chars
        end = min(len(text), (seq+1)*target_chars)
        chunk = text[start:end]
        h = sha1(chunk.encode("utf-8", "ignore")).hexdigest()
        parts.append((seq, start, end, h))
    return parts

def add_chapters(job_id, text):
    chapters = split_text_into_chapters(text)
    with connect() as c:
        for (seq, start, end, h) in chapters:
            c.execute(
                "INSERT INTO chapters(job_id,seq,text_hash,start_char,end_char) VALUES(?,?,?,?,?)",
                (job_id, seq, h, start, end)
            )
        c.commit()

def list_jobs():
    with connect() as c:
        return c.execute("SELECT * FROM jobs ORDER BY id DESC").fetchall()

def list_chapters(job_id):
    with connect() as c:
        return c.execute("SELECT * FROM chapters WHERE job_id=? ORDER BY seq", (job_id,)).fetchall()

def next_queued_chapter():
    with connect() as c:
        ch = c.execute(
            "SELECT * FROM chapters WHERE status='queued' ORDER BY id LIMIT 1"
        ).fetchone()
        return ch

def mark_status(table, row_id, status):
    with connect() as c:
        c.execute(f"UPDATE {table} SET status=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (status, row_id))
        c.commit()

def update_progress(chapter_id, progress):
    with connect() as c:
        c.execute("UPDATE chapters SET progress=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (progress, chapter_id))
        c.commit()

def set_artifact(chapter_id, path):
    with connect() as c:
        c.execute("UPDATE chapters SET artifact_path=?, status='done', updated_at=CURRENT_TIMESTAMP WHERE id=?", (path, chapter_id))
        c.commit()
