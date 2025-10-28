# ebook2audiobook v2 (Blueprint Phase 1)

Goal: resumable, faster pipeline with a queue, 2 workers, and a simple Project Manager UI — without touching the original app.

## Run locally (venv)

Open: http://localhost:7861

## Notes
- Uses SQLite (`jobs.sqlite` in repo root).
- 2 workers default (configurable).
- Phase-1.1: hook `worker.process_chapter()` to the real TTS converter.
