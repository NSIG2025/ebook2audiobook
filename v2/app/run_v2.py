import threading
import webbrowser
from . import orchestrator, ui

PORT = 7861  # keep separate from 7860

def main():
    orch = orchestrator.Orchestrator(workers=2)
    t = threading.Thread(target=orch.run, daemon=True)
    t.start()

    app = ui.build_ui(orch)
    url = f"http://127.0.0.1:{PORT}"
    webbrowser.open(url)
    # Gradio v5: queue() not needed; just launch
    app.launch(server_name="0.0.0.0", server_port=PORT)

if __name__ == "__main__":
    main()
