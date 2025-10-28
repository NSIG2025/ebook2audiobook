import threading, time, os
from queue import Queue, Empty
from . import models, worker

class Orchestrator:
    def __init__(self, workers=2, out_dir="Audiobooks_v2"):
        self.q = Queue()
        self.workers = []
        self.stop_flag = False
        self.out_dir = os.path.abspath(out_dir)
        os.makedirs(self.out_dir, exist_ok=True)

        for _ in range(workers):
            t = threading.Thread(target=self._worker_loop, daemon=True)
            self.workers.append(t)

    def run(self):
        for t in self.workers:
            t.start()
        # Requeue interrupted (Phase-1 simple: noop or mark-running->queued if needed)
        # Could be extended later to recover partials
        while not self.stop_flag:
            self._fill_queue_if_needed()
            time.sleep(0.3)

    def _fill_queue_if_needed(self):
        while self.q.qsize() < len(self.workers):
            ch = models.next_queued_chapter()
            if not ch: break
            self.q.put(dict(ch))

    def _worker_loop(self):
        while not self.stop_flag:
            try:
                ch = self.q.get(timeout=0.5)
            except Empty:
                continue
            try:
                worker.process_chapter(ch, self.out_dir)
            except Exception:
                models.mark_status("chapters", ch["id"], "failed")
            finally:
                self.q.task_done()
