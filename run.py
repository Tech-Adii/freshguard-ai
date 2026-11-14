import sys
import uvicorn
import webbrowser
import threading
import time
from src.config import settings

def open_browser():
    time.sleep(1.2)
    url = f"http://localhost:{settings.PORT}"
    print(f"\n🌐 Opening FreshGuard AI Web Dashboard: {url}\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass

if __name__ == "__main__":
    print("=" * 65)
    print("🚀 STARTING FRESHGUARD AI — STALE-ANSWER DETECTOR")
    print("   Geek Room Global AI Hackathon · Problem Statement 06")
    print("   Powered by Tavily Search & Maxim AI Bifrost Gateway")
    print("=" * 65)
    print(f"👉 Local Dashboard: http://localhost:{settings.PORT}")
    print(f"👉 API Docs:        http://localhost:{settings.PORT}/docs")
    print("=" * 65)

    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("src.api.server:app", host=settings.HOST, port=settings.PORT, reload=False)
