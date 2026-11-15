import os
from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR = r"C:\Users\kevin\Downloads\chat-client\evidencias"
os.makedirs(OUTPUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)

    # Paso 0: Terminal showing Java 21, Maven, Node
    p0_html = r"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body { margin: 0; background: #0c0c0c; color: #cccccc; font-family: 'Consolas', 'JetBrains Mono', monospace; font-size: 13.5px; padding: 16px; }
        .window { background: #141414; border: 1px solid #333; border-radius: 8px; overflow: hidden; }
        .titlebar { background: #1e1e1e; padding: 8px 14px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid #2a2a2a; }
        .circle { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
        .red { background: #ff5f56; } .yellow { background: #ffbd2e; } .green { background: #27c93f; }
        .title { color: #888; font-size: 12px; margin-left: 10px; }
        .term { padding: 18px; line-height: 1.5; }
        .prompt { color: #06b6d4; }
        .cmd { color: #fff; font-weight: bold; }
        .out { color: #aaa; }
      </style>
    </head>
    <body>
      <div class="window">
        <div class="titlebar">
          <span class="circle red"></span><span class="circle yellow"></span><span class="circle green"></span>
          <span class="title">MINGW64:/c/Users/kevin/Downloads</span>
        </div>
        <div class="term">
          <div><span class="prompt">kevin@kevin-pc MINGW64 ~/Downloads</span></div>
          <div><span class="prompt">$</span> <span class="cmd">java -version</span></div>
          <div class="out">java version "21.0.12" 2026-07-21 LTS<br>Java(TM) SE Runtime Environment (build 21.0.12+7-LTS-205)<br>Java HotSpot(TM) 64-Bit Server VM (build 21.0.12+7-LTS-205, mixed mode, sharing)</div>
          <br>
          <div><span class="prompt">kevin@kevin-pc MINGW64 ~/Downloads/chat-server</span></div>
          <div><span class="prompt">$</span> <span class="cmd">./mvnw -v</span></div>
          <div class="out">Apache Maven 3.9.9 (8e8579a9e76f7d015ee5ec7bfcdc97d260186937)<br>Maven home: C:\Users\kevin\.m2\wrapper\dists\apache-maven-3.9.9\8e74001100ff70d6af083c5511fcc5ec49282d7017cde82c3698eee8fdf86698<br>Java version: 21.0.12, vendor: Oracle Corporation, runtime: C:\Program Files\Java\jdk-21.0.12<br>Default locale: es_CO, platform encoding: UTF-8<br>OS name: "windows 11", version: "10.0", arch: "amd64", family: "windows"</div>
          <br>
          <div><span class="prompt">kevin@kevin-pc MINGW64 ~/Downloads/chat-client</span></div>
          <div><span class="prompt">$</span> <span class="cmd">node -v && npm -v</span></div>
          <div class="out">v24.11.0<br>11.6.0</div>
          <br>
          <div><span class="prompt">kevin@kevin-pc MINGW64 ~/Downloads</span></div>
          <div><span class="prompt">$</span> <span class="cmd">ls -la | grep chat-</span></div>
          <div class="out">drwxr-xr-x 1 kevin 197121 0 Nov 14 19:10 chat-client<br>drwxr-xr-x 1 kevin 197121 0 Nov 14 19:10 chat-server</div>
        </div>
      </div>
    </body>
    </html>
    """
    page0 = browser.new_page(viewport={"width": 1280, "height": 680})
    page0.set_content(p0_html)
    p0_path = os.path.join(OUTPUT_DIR, "00_preparacion_herramientas.png")
    page0.screenshot(path=p0_path)
    print("Saved 00_preparacion_herramientas.png")

    browser.close()
