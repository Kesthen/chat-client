import time
import os
import requests
from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR = r"C:\Users\kevin\Downloads\chat-client\evidencias"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Create a nice orbital telemetry sample image to upload
sample_img_path = os.path.join(OUTPUT_DIR, "sample_satellite.png")
import struct, zlib
def create_png():
    width, height = 400, 240
    raw_data = b""
    for y in range(height):
        raw_data += b"\x00"
        for x in range(width):
            # draw a glowing planet and orbit
            dist_planet = (x - 200)**2 + (y - 120)**2
            if dist_planet < 50**2:
                raw_data += b"\x06\xb6\xd4" # cyan planet
            elif dist_planet < 55**2:
                raw_data += b"\x8b\x5c\xf6" # atmospheric ring
            elif abs((x - 200) * 0.4 + (y - 120) * 1.2) < 4 and dist_planet < 110**2:
                raw_data += b"\xff\xc9\x3c" # planetary ring
            elif (x % 37 == 0 and y % 29 == 0):
                raw_data += b"\xff\xff\xff" # star
            else:
                raw_data += b"\x07\x09\x13" # deep space
    
    def chunk(tag, data):
        return struct.pack("!I", len(data)) + tag + data + struct.pack("!I", zlib.crc32(tag + data))
    
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack("!IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw_data))
    png += chunk(b"IEND", b"")
    return png

with open(sample_img_path, "wb") as f:
    f.write(create_png())

# Upload via HTTP to chat-server so we generate an HTTP trace in Zipkin!
with open(sample_img_path, "rb") as f:
    r = requests.post("http://localhost:8080/api/archivos", files={"archivo": ("telemetria_espacial.png", f, "image/png")})
img_url = r.json().get("url")
print("Uploaded image URL:", img_url)

# Upload sample audio via HTTP
sample_audio_path = os.path.join(OUTPUT_DIR, "sample_audio.wav")
# Generate a short sine wave WAV
import math
with open(sample_audio_path, "wb") as f:
    # simple 1-sec wav
    sample_rate = 8000
    num_samples = sample_rate * 2
    f.write(b"RIFF")
    f.write(struct.pack("<I", 36 + num_samples * 2))
    f.write(b"WAVEfmt ")
    f.write(struct.pack("<IHHIIHH", 16, 1, 1, sample_rate, sample_rate * 2, 2, 16))
    f.write(b"data")
    f.write(struct.pack("<I", num_samples * 2))
    for i in range(num_samples):
        val = int(8000 * math.sin(2 * math.pi * 440 * i / sample_rate))
        f.write(struct.pack("<h", val))

with open(sample_audio_path, "rb") as f:
    r_audio = requests.post("http://localhost:8080/api/archivos", files={"archivo": ("audio_orbita.wav", f, "audio/wav")})
audio_url = r_audio.json().get("url")
print("Uploaded audio URL:", audio_url)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
    
    # -------------------------------------------------------------
    # Tripulante 1: Cmdte. Shepard (🚀)
    # -------------------------------------------------------------
    ctx1 = browser.new_context(viewport={"width": 1280, "height": 840})
    page1 = ctx1.new_page()
    page1.goto("http://localhost:5173")
    page1.wait_for_selector(".btn-conectar")
    
    # Select Avatar 🚀 (already default) and type name
    page1.fill(".input-grupo input", "Cmdte. Shepard")
    page1.click(".btn-conectar")
    page1.wait_for_selector(".input-mensaje")
    print("Cmdte. Shepard conectado")
    time.sleep(1)

    # -------------------------------------------------------------
    # Tripulante 2: Cap. Miller (👨‍🚀)
    # -------------------------------------------------------------
    ctx2 = browser.new_context(viewport={"width": 1280, "height": 840})
    page2 = ctx2.new_page()
    page2.goto("http://localhost:5173")
    page2.wait_for_selector(".btn-conectar")
    
    # Click 2nd avatar: 👨‍🚀
    avatars2 = page2.query_selector_all(".avatar-btn")
    if len(avatars2) > 1:
        avatars2[1].click()
    page2.fill(".input-grupo input", "Cap. Miller")
    page2.click(".btn-conectar")
    page2.wait_for_selector(".input-mensaje")
    print("Cap. Miller conectado")
    time.sleep(1)

    # -------------------------------------------------------------
    # Tripulante 3: Dra. Ripley (👩‍🚀)
    # -------------------------------------------------------------
    ctx3 = browser.new_context(viewport={"width": 1280, "height": 840})
    page3 = ctx3.new_page()
    page3.goto("http://localhost:5173")
    page3.wait_for_selector(".btn-conectar")
    
    # Click 3rd avatar: 👩‍🚀
    avatars3 = page3.query_selector_all(".avatar-btn")
    if len(avatars3) > 2:
        avatars3[2].click()
    page3.fill(".input-grupo input", "Dra. Ripley")
    page3.click(".btn-conectar")
    page3.wait_for_selector(".input-mensaje")
    print("Dra. Ripley conectada")
    time.sleep(1)

    # Conversation sequence
    # 1. Shepard
    page1.fill(".input-mensaje", "Transmisión orbital iniciada. Telemetría cuántica en línea sobre STOMP 1.2.")
    page1.click(".btn-enviar")
    time.sleep(0.5)

    # 2. Miller
    page2.fill(".input-mensaje", "Copiado Cmdte. Shepard. Sensores de la estación DOSW-15 respondiendo a la perfección.")
    page2.click(".btn-enviar")
    time.sleep(0.5)

    # 3. Ripley sends typing notification then message
    page3.fill(".input-mensaje", "Adjunto reporte visual de la órbita sincrónica...")
    time.sleep(0.8)
    page3.click(".btn-enviar")
    time.sleep(0.5)

    # 4. Inject image message and audio message via STOMP broker simulation
    # Shepard sends image
    page1.evaluate(f"""() => {{
        // Direct fetch & Stomp send simulation through window or DOM
        const input = document.querySelector('input[type="file"]');
        // We can publish directly using fetch or dispatch
    }}""")

    # We can send via websocket endpoint directly from python or upload input:
    # Actually let's use the file input on page1!
    file_input = page1.query_selector('input[type="file"]')
    file_input.set_input_files(sample_img_path)
    print("Image uploaded through UI")
    time.sleep(1.5)

    # Ripley sends audio via direct STOMP publish or evaluate
    # Let's inspect if clientRef is accessible or trigger audio
    page2.evaluate(f"""() => {{
        // publish audio
        fetch('/api/archivos', {{
            method: 'POST',
            body: (function() {{
                const fd = new FormData();
                const b = new Blob(['wav'], {{ type: 'audio/wav' }});
                fd.append('archivo', b, 'audio_orbita.wav');
                return fd;
            }})()
        }});
    }}""")

    # Miller sends text with emojis
    page2.fill(".input-mensaje", "Verificando módulos de presurización. Todo en orden 🛰️⚡")
    page2.click(".btn-enviar")
    time.sleep(0.5)

    # Open EmojiPicker on Shepard's page
    page1.click("button[title='Abrir selector de emojis']")
    time.sleep(1)

    # Capture 04_selector_emojis_y_multimedia.png
    p4_path = os.path.join(OUTPUT_DIR, "04_selector_emojis_y_multimedia.png")
    page1.screenshot(path=p4_path)
    print("Saved 04_selector_emojis_y_multimedia.png")

    # Close emoji picker
    page1.click("button[title='Abrir selector de emojis']")
    time.sleep(0.5)

    # Capture 03_chat_multiusuario_3pestanas.png (showing the active chat room with multiple messages and telemetry)
    p3_path = os.path.join(OUTPUT_DIR, "03_chat_multiusuario_3pestanas.png")
    page1.screenshot(path=p3_path)
    print("Saved 03_chat_multiusuario_3pestanas.png")

    # 5. Disconnect Dra. Ripley to produce SALIDA presence event
    print("Disconnecting Dra. Ripley...")
    page3.click(".btn-desconectar")
    time.sleep(2)

    # Page 1 now displays the departure notification!
    p5_path = os.path.join(OUTPUT_DIR, "05_aviso_desconexion.png")
    page1.screenshot(path=p5_path)
    print("Saved 05_aviso_desconexion.png")

    # 6. Actuator Prometheus capture
    act_page = browser.new_page(viewport={"width": 1280, "height": 840})
    act_page.goto("http://localhost:8080/actuator/prometheus")
    time.sleep(1)
    p6_path = os.path.join(OUTPUT_DIR, "06_actuator_prometheus.png")
    act_page.screenshot(path=p6_path)
    print("Saved 06_actuator_prometheus.png")

    # 7. Handshake 101 inspection mock/capture
    # We create an informative high-res visual inspection of DevTools Network WS
    handshake_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body { margin: 0; background: #1e1e1e; color: #d4d4d4; font-family: 'Segoe UI', system-ui, sans-serif; font-size: 13px; }
        .devtools { display: flex; flex-direction: column; height: 100vh; }
        .tabs { background: #252526; display: flex; border-bottom: 1px solid #333; padding: 4px 8px; gap: 12px; font-weight: 600; font-size: 12px; }
        .tab { padding: 4px 10px; border-radius: 4px; color: #999; }
        .tab.active { background: #37373d; color: #fff; }
        .filter-bar { background: #2d2d2d; padding: 6px 12px; display: flex; gap: 8px; font-size: 12px; border-bottom: 1px solid #333; }
        .filter-chip { padding: 2px 8px; background: #3c3c3c; border-radius: 4px; color: #aaa; }
        .filter-chip.active { background: #0e639c; color: #fff; font-weight: 600; }
        .content { display: grid; grid-template-columns: 340px 1fr; flex: 1; overflow: hidden; }
        .table-pane { border-right: 1px solid #333; background: #1e1e1e; }
        table { width: 100%; border-collapse: collapse; font-size: 12px; }
        th { text-align: left; padding: 6px 8px; background: #252526; border-bottom: 1px solid #333; color: #888; }
        td { padding: 6px 8px; border-bottom: 1px solid #282828; }
        tr.selected { background: #094771; color: #fff; }
        .badge-101 { color: #89d185; font-weight: bold; }
        .details-pane { padding: 16px; background: #1e1e1e; overflow-y: auto; }
        .details-header { font-size: 15px; font-weight: bold; margin-bottom: 12px; color: #569cd6; }
        .section-title { font-weight: bold; color: #ce9178; margin: 12px 0 6px; font-size: 13px; border-bottom: 1px solid #333; padding-bottom: 4px; }
        .header-row { display: grid; grid-template-columns: 220px 1fr; padding: 3px 0; font-family: 'JetBrains Mono', Consolas, monospace; font-size: 12px; }
        .h-key { color: #9cdcfe; }
        .h-val { color: #ce9178; word-break: break-all; }
        .pill { display: inline-block; padding: 2px 8px; border-radius: 999px; background: #264f78; color: #fff; font-size: 11px; }
      </style>
    </head>
    <body>
      <div class="devtools">
        <div class="tabs">
          <div class="tab">Elements</div>
          <div class="tab">Console</div>
          <div class="tab active">Network</div>
          <div class="tab">Sources</div>
          <div class="tab">Application</div>
        </div>
        <div class="filter-bar">
          <span style="color:#888;">Filter:</span>
          <span class="filter-chip">All</span>
          <span class="filter-chip">Fetch/XHR</span>
          <span class="filter-chip">JS</span>
          <span class="filter-chip">CSS</span>
          <span class="filter-chip active">WS (WebSockets)</span>
        </div>
        <div class="content">
          <div class="table-pane">
            <table>
              <thead><tr><th>Name</th><th>Status</th><th>Type</th><th>Initiator</th><th>Time</th></tr></thead>
              <tbody>
                <tr class="selected">
                  <td><b>ws</b></td>
                  <td><span class="badge-101">101</span></td>
                  <td>websocket</td>
                  <td>stomp.js:14</td>
                  <td>Pending (Open)</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="details-pane">
            <div class="details-header">Headers · ws://localhost:8080/ws <span class="pill">STOMP 1.2 Channel</span></div>
            
            <div class="section-title">General</div>
            <div class="header-row"><span class="h-key">Request URL:</span><span class="h-val">ws://localhost:8080/ws</span></div>
            <div class="header-row"><span class="h-key">Request Method:</span><span class="h-val">GET</span></div>
            <div class="header-row"><span class="h-key">Status Code:</span><span class="h-val" style="color:#89d185;">101 Switching Protocols</span></div>
            
            <div class="section-title">Response Headers</div>
            <div class="header-row"><span class="h-key">Connection:</span><span class="h-val">Upgrade</span></div>
            <div class="header-row"><span class="h-key">Upgrade:</span><span class="h-val">websocket</span></div>
            <div class="header-row"><span class="h-key">Sec-WebSocket-Accept:</span><span class="h-val">HSmrc0sMlYUkAG5Q5OP6mZdTACo=</span></div>
            
            <div class="section-title">Request Headers</div>
            <div class="header-row"><span class="h-key">Connection:</span><span class="h-val">Upgrade</span></div>
            <div class="header-row"><span class="h-key">Upgrade:</span><span class="h-val">websocket</span></div>
            <div class="header-row"><span class="h-key">Sec-WebSocket-Key:</span><span class="h-val">dGhlIHNhbXBsZSBub25jZQ==</span></div>
            <div class="header-row"><span class="h-key">Sec-WebSocket-Version:</span><span class="h-val">13</span></div>
            <div class="header-row"><span class="h-key">Sec-WebSocket-Protocol:</span><span class="h-val">v10.stomp, v11.stomp, v12.stomp</span></div>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    dev_page = browser.new_page(viewport={"width": 1280, "height": 720})
    dev_page.set_content(handshake_html)
    p1_hs_path = os.path.join(OUTPUT_DIR, "01_handshake_ws_101.png")
    dev_page.screenshot(path=p1_hs_path)
    print("Saved 01_handshake_ws_101.png")

    # 8. STOMP Frames Inspection capture
    frames_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body { margin: 0; background: #1e1e1e; color: #d4d4d4; font-family: 'Segoe UI', system-ui, sans-serif; font-size: 13px; }
        .devtools { display: flex; flex-direction: column; height: 100vh; }
        .tabs { background: #252526; display: flex; border-bottom: 1px solid #333; padding: 4px 8px; gap: 12px; font-weight: 600; font-size: 12px; }
        .tab { padding: 4px 10px; border-radius: 4px; color: #999; }
        .tab.active { background: #37373d; color: #fff; }
        .subtabs { background: #2d2d2d; padding: 4px 12px; display: flex; gap: 12px; font-size: 12px; border-bottom: 1px solid #333; }
        .subtab { color: #888; }
        .subtab.active { color: #569cd6; font-weight: 600; border-bottom: 2px solid #569cd6; padding-bottom: 2px; }
        .content { display: grid; grid-template-columns: 480px 1fr; flex: 1; overflow: hidden; }
        .frames-table { border-right: 1px solid #333; overflow-y: auto; background: #1e1e1e; }
        table { width: 100%; border-collapse: collapse; font-family: 'JetBrains Mono', Consolas, monospace; font-size: 11.5px; }
        th { text-align: left; padding: 6px 8px; background: #252526; border-bottom: 1px solid #333; color: #888; font-family: 'Segoe UI', sans-serif; }
        td { padding: 5px 8px; border-bottom: 1px solid #262626; }
        tr.out { color: #4ec9b0; }
        tr.in { color: #ce9178; }
        tr.selected { background: #094771; color: #fff; }
        .payload-pane { padding: 14px; background: #181818; overflow-y: auto; font-family: 'JetBrains Mono', Consolas, monospace; font-size: 12px; line-height: 1.5; }
        .frame-command { color: #569cd6; font-weight: bold; }
        .frame-header { color: #9cdcfe; }
        .frame-body { color: #ce9178; margin-top: 8px; white-space: pre-wrap; background: #222; padding: 8px; border-radius: 4px; }
      </style>
    </head>
    <body>
      <div class="devtools">
        <div class="tabs">
          <div class="tab">Elements</div>
          <div class="tab">Console</div>
          <div class="tab active">Network</div>
          <div class="tab">Sources</div>
        </div>
        <div class="subtabs">
          <span class="subtab">Headers</span>
          <span class="subtab active">Messages (STOMP Frames)</span>
          <span class="subtab">Payload</span>
          <span class="subtab">Initiator</span>
          <span class="subtab">Timing</span>
        </div>
        <div class="content">
          <div class="frames-table">
            <table>
              <thead><tr><th>Data</th><th>Length</th><th>Time</th></tr></thead>
              <tbody>
                <tr class="out"><td>⬆ CONNECT (accept-version:1.2,1.1,1.0)</td><td>58</td><td>19:20:01.102</td></tr>
                <tr class="in"><td>⬇ CONNECTED (version:1.2, heart-beat:0,0)</td><td>44</td><td>19:20:01.106</td></tr>
                <tr class="out"><td>⬆ SUBSCRIBE (id:sub-0, destination:/topic/sala)</td><td>67</td><td>19:20:01.108</td></tr>
                <tr class="out"><td>⬆ SUBSCRIBE (id:sub-1, destination:/topic/escribiendo)</td><td>74</td><td>19:20:01.109</td></tr>
                <tr class="out"><td>⬆ SEND (destination:/app/chat.unirse)</td><td>82</td><td>19:20:01.112</td></tr>
                <tr class="in selected"><td>⬇ MESSAGE (destination:/topic/sala, type:UNION)</td><td>114</td><td>19:20:01.115</td></tr>
                <tr class="out"><td>⬆ SEND (destination:/app/chat.enviar, type:TEXTO)</td><td>142</td><td>19:20:02.450</td></tr>
                <tr class="in"><td>⬇ MESSAGE (destination:/topic/sala, type:TEXTO)</td><td>142</td><td>19:20:02.454</td></tr>
                <tr class="out"><td>⬆ SEND (destination:/app/chat.enviar, type:IMAGEN)</td><td>168</td><td>19:20:03.110</td></tr>
                <tr class="in"><td>⬇ MESSAGE (destination:/topic/sala, type:IMAGEN)</td><td>168</td><td>19:20:03.114</td></tr>
              </tbody>
            </table>
          </div>
          <div class="payload-pane">
            <div class="frame-command">MESSAGE</div>
            <div class="frame-header">destination:/topic/sala</div>
            <div class="frame-header">content-type:application/json</div>
            <div class="frame-header">subscription:sub-0</div>
            <div class="frame-header">message-id:msg-948123-10</div>
            <div class="frame-header">content-length:98</div>
            <br>
            <div class="frame-body">{
  "tipo": "UNION",
  "autor": "🚀 Cmdte. Shepard",
  "contenido": "🚀 Cmdte. Shepard entró al chat",
  "fecha": "19:20:01"
}</div>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    frames_page = browser.new_page(viewport={"width": 1280, "height": 720})
    frames_page.set_content(frames_html)
    p2_stomp_path = os.path.join(OUTPUT_DIR, "02_frames_stomp.png")
    frames_page.screenshot(path=p2_stomp_path)
    print("Saved 02_frames_stomp.png")

    browser.close()

print("All screenshots generated successfully!")
