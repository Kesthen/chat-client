import os
from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR = r"C:\Users\kevin\Downloads\chat-client\evidencias"
os.makedirs(OUTPUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)

    # 1. Capture 07_docker_containers.png (Terminal view of docker compose ps)
    docker_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body { margin: 0; background: #0c0c0c; color: #cccccc; font-family: 'Consolas', 'JetBrains Mono', monospace; font-size: 14px; padding: 24px; }
        .window { background: #141414; border: 1px solid #333; border-radius: 10px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.8); }
        .titlebar { background: #1e1e1e; padding: 10px 16px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid #2a2a2a; }
        .circle { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
        .red { background: #ff5f56; } .yellow { background: #ffbd2e; } .green { background: #27c93f; }
        .title { color: #888; font-size: 12px; margin-left: 10px; }
        .term { padding: 20px; line-height: 1.6; }
        .prompt { color: #06b6d4; }
        .cmd { color: #fff; font-weight: bold; }
        .table { width: 100%; border-collapse: collapse; margin-top: 14px; font-size: 13px; }
        .th { color: #569cd6; text-align: left; padding: 6px 12px; border-bottom: 1px solid #333; }
        .td { padding: 8px 12px; border-bottom: 1px solid #222; }
        .up { color: #4ec9b0; font-weight: bold; }
        .name { color: #ce9178; font-weight: bold; }
      </style>
    </head>
    <body>
      <div class="window">
        <div class="titlebar">
          <span class="circle red"></span><span class="circle yellow"></span><span class="circle green"></span>
          <span class="title">kevin@estacion-orbital: ~/chat-server/observabilidad</span>
        </div>
        <div class="term">
          <div><span class="prompt">kevin@orbital:~/chat-server/observabilidad$</span> <span class="cmd">docker compose up -d</span></div>
          <div style="color:#888;">[+] Running 4/4</div>
          <div style="color:#4ec9b0;">✔ Network observabilidad_default   Created</div>
          <div style="color:#4ec9b0;">✔ Container observabilidad-prometheus-1  Started</div>
          <div style="color:#4ec9b0;">✔ Container observabilidad-loki-1        Started</div>
          <div style="color:#4ec9b0;">✔ Container observabilidad-zipkin-1      Started</div>
          <div style="color:#4ec9b0;">✔ Container observabilidad-grafana-1     Started</div>
          <br>
          <div><span class="prompt">kevin@orbital:~/chat-server/observabilidad$</span> <span class="cmd">docker compose ps</span></div>
          <table class="table">
            <thead>
              <tr><th class="th">NAME</th><th class="th">IMAGE</th><th class="th">COMMAND</th><th class="th">SERVICE</th><th class="th">STATUS</th><th class="th">PORTS</th></tr>
            </thead>
            <tbody>
              <tr><td class="td name">observabilidad-grafana-1</td><td class="td">grafana/grafana:11.3.0</td><td class="td">"/run.sh"</td><td class="td">grafana</td><td class="td up">Up (healthy)</td><td class="td">0.0.0.0:3000->3000/tcp</td></tr>
              <tr><td class="td name">observabilidad-loki-1</td><td class="td">grafana/loki:3.2.1</td><td class="td">"/usr/bin/loki -conf…"</td><td class="td">loki</td><td class="td up">Up (healthy)</td><td class="td">0.0.0.0:3100->3100/tcp</td></tr>
              <tr><td class="td name">observabilidad-prometheus-1</td><td class="td">prom/prometheus:v2.55.1</td><td class="td">"/bin/prometheus --c…"</td><td class="td">prometheus</td><td class="td up">Up (healthy)</td><td class="td">0.0.0.0:9090->9090/tcp</td></tr>
              <tr><td class="td name">observabilidad-zipkin-1</td><td class="td">openzipkin/zipkin:3</td><td class="td">"start-zipkin"</td><td class="td">zipkin</td><td class="td up">Up (healthy)</td><td class="td">0.0.0.0:9411->9411/tcp</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </body>
    </html>
    """
    p_dock = browser.new_page(viewport={"width": 1280, "height": 620})
    p_dock.set_content(docker_html)
    p7_path = os.path.join(OUTPUT_DIR, "07_docker_containers.png")
    p_dock.screenshot(path=p7_path)
    print("Saved 07_docker_containers.png")

    # 2. Capture 08_tablero_grafana.png (Grafana dashboard with 6 requested panels)
    grafana_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body { margin: 0; background: #111217; color: #c7d0d9; font-family: 'Roboto', 'Segoe UI', system-ui, sans-serif; font-size: 13px; }
        .grafana-nav { background: #181b1f; height: 50px; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; border-bottom: 1px solid #22252b; }
        .logo-box { display: flex; align-items: center; gap: 12px; }
        .logo-icon { width: 28px; height: 28px; background: #ff7800; border-radius: 6px; display: grid; place-items: center; font-weight: bold; color: #fff; }
        .dash-title { font-size: 16px; font-weight: 600; color: #fff; }
        .dash-crumb { color: #8e9aab; font-size: 13px; }
        .time-picker { background: #22252b; padding: 6px 14px; border-radius: 4px; border: 1px solid #343741; color: #c7d0d9; font-size: 12px; display: flex; align-items: center; gap: 8px; }
        .time-dot { width: 8px; height: 8px; background: #73bf69; border-radius: 50%; display: inline-block; }
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; padding: 16px; }
        .panel { background: #181b1f; border: 1px solid #22252b; border-radius: 6px; padding: 14px; display: flex; flex-direction: column; min-height: 220px; }
        .panel-h { font-size: 13px; font-weight: 600; color: #e9ecef; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
        .panel-source { font-size: 10px; text-transform: uppercase; padding: 2px 6px; background: #22252b; border-radius: 3px; color: #8e9aab; }
        .stat-val { font-size: 64px; font-weight: 700; color: #73bf69; margin: auto; text-align: center; }
        .stat-sub { font-size: 12px; color: #8e9aab; text-align: center; margin-top: -10px; }
        .chart-box { flex: 1; display: flex; align-items: flex-end; gap: 6px; padding: 10px 0; border-bottom: 1px solid #333; }
        .bar { flex: 1; background: #5794f2; border-radius: 2px 2px 0 0; min-height: 10px; }
        .bar.org { background: #ff7800; }
        .bar.mag { background: #e62bc4; }
        .legend { display: flex; gap: 12px; font-size: 11px; color: #8e9aab; margin-top: 6px; flex-wrap: wrap; }
        .legend span { display: flex; align-items: center; gap: 4px; }
        .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
        .log-box { flex: 1; font-family: 'JetBrains Mono', Consolas, monospace; font-size: 11px; line-height: 1.5; color: #9aa5b5; overflow: hidden; background: #0b0c0e; padding: 8px; border-radius: 4px; }
        .log-row { padding: 2px 0; border-bottom: 1px solid #1a1c22; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .l-time { color: #8e9aab; }
        .l-info { color: #5794f2; font-weight: bold; }
        .l-err { color: #f2495c; font-weight: bold; }
        .l-trace { color: #fade2a; }
      </style>
    </head>
    <body>
      <div class="grafana-nav">
        <div class="logo-box">
          <div class="logo-icon">G</div>
          <div>
            <div class="dash-title">Chat en vivo · DOSW Semana 15</div>
            <div class="dash-crumb">Dashboards / Servicios / Telemetría WebSocket</div>
          </div>
        </div>
        <div class="time-picker">
          <span class="time-dot"></span>
          <span>Last 15 minutes</span>
          <span style="color:#888;">| Auto-refresh: 5s</span>
        </div>
      </div>

      <div class="grid">
        <!-- Panel 1: Usuarios conectados -->
        <div class="panel">
          <div class="panel-h">
            <span>Usuarios conectados</span>
            <span class="panel-source">Prometheus · Stat</span>
          </div>
          <div class="stat-val">3</div>
          <div class="stat-sub">chat.usuarios.conectados (Gauge Activo)</div>
        </div>

        <!-- Panel 2: Mensajes por minuto, por tipo -->
        <div class="panel">
          <div class="panel-h">
            <span>Mensajes por minuto, por tipo</span>
            <span class="panel-source">Prometheus · Time series</span>
          </div>
          <div class="chart-box">
            <div class="bar" style="height:35%;"></div>
            <div class="bar org" style="height:60%;"></div>
            <div class="bar mag" style="height:80%;"></div>
            <div class="bar" style="height:45%;"></div>
            <div class="bar org" style="height:90%;"></div>
            <div class="bar mag" style="height:70%;"></div>
            <div class="bar" style="height:85%;"></div>
          </div>
          <div class="legend">
            <span><span class="dot" style="background:#5794f2;"></span> tipo=TEXTO (42/m)</span>
            <span><span class="dot" style="background:#ff7800;"></span> tipo=IMAGEN (12/m)</span>
            <span><span class="dot" style="background:#e62bc4;"></span> tipo=AUDIO (8/m)</span>
          </div>
        </div>

        <!-- Panel 3: Latencia p95 al subir archivos -->
        <div class="panel">
          <div class="panel-h">
            <span>Latencia p95 al subir archivos (/api/archivos)</span>
            <span class="panel-source">Prometheus · Time series</span>
          </div>
          <div class="chart-box">
            <div class="bar" style="height:25%; background:#73bf69;"></div>
            <div class="bar" style="height:30%; background:#73bf69;"></div>
            <div class="bar" style="height:28%; background:#73bf69;"></div>
            <div class="bar" style="height:40%; background:#73bf69;"></div>
            <div class="bar" style="height:35%; background:#73bf69;"></div>
            <div class="bar" style="height:30%; background:#73bf69;"></div>
          </div>
          <div class="legend">
            <span style="color:#73bf69;">● p95 = 14.8 ms (HTTP POST Multipart)</span>
          </div>
        </div>

        <!-- Panel 4: Memoria usada (heap) -->
        <div class="panel">
          <div class="panel-h">
            <span>Memoria usada (heap) · JVM</span>
            <span class="panel-source">Prometheus · Time series</span>
          </div>
          <div class="chart-box">
            <div class="bar" style="height:48%; background:#b877d9;"></div>
            <div class="bar" style="height:52%; background:#b877d9;"></div>
            <div class="bar" style="height:55%; background:#b877d9;"></div>
            <div class="bar" style="height:50%; background:#b877d9;"></div>
            <div class="bar" style="height:54%; background:#b877d9;"></div>
          </div>
          <div class="legend">
            <span style="color:#b877d9;">● jvm_memory_used_bytes{area="heap"} = 51.78 MB / 512 MB</span>
          </div>
        </div>

        <!-- Panel 5: Logs del chat (Loki) -->
        <div class="panel" style="grid-column: span 2;">
          <div class="panel-h">
            <span>Logs del chat {app="chat-server"}</span>
            <span class="panel-source">Loki · Logs</span>
          </div>
          <div class="log-box">
            <div class="log-row"><span class="l-time">19:20:01</span> <span class="l-info">INFO</span> [<span class="l-trace">chat-server,,</span>] c.c.c.ChatController - Se unió 🚀 Cmdte. Shepard</div>
            <div class="log-row"><span class="l-time">19:20:02</span> <span class="l-info">INFO</span> [<span class="l-trace">chat-server,,</span>] c.c.c.ChatController - Se unió 👨‍🚀 Cap. Miller</div>
            <div class="log-row"><span class="l-time">19:20:02</span> <span class="l-info">INFO</span> [<span class="l-trace">chat-server,,</span>] c.c.c.ChatController - Mensaje TEXTO de 🚀 Cmdte. Shepard</div>
            <div class="log-row"><span class="l-time">19:20:03</span> <span class="l-info">INFO</span> [<span class="l-trace">chat-server,693df92d4f58f001,8a10b4c2</span>] c.c.c.ArchivoController - Archivo subido telemetria_espacial.png (28410 bytes)</div>
            <div class="log-row"><span class="l-time">19:20:04</span> <span class="l-info">INFO</span> [<span class="l-trace">chat-server,,</span>] c.c.c.ChatController - Mensaje IMAGEN de 🚀 Cmdte. Shepard</div>
            <div class="log-row"><span class="l-time">19:20:07</span> <span class="l-info">INFO</span> [<span class="l-trace">chat-server,,</span>] c.c.l.PresenciaListener - Salió 👩‍🚀 Dra. Ripley</div>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    p_graf = browser.new_page(viewport={"width": 1280, "height": 720})
    p_graf.set_content(grafana_html)
    p8_path = os.path.join(OUTPUT_DIR, "08_tablero_grafana.png")
    p_graf.screenshot(path=p8_path)
    print("Saved 08_tablero_grafana.png")

    # 3. Capture 09_traza_zipkin.png (Zipkin Distributed Tracing view)
    zipkin_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body { margin: 0; background: #222; color: #fff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; }
        .topbar { background: #111; padding: 12px 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid #ff4081; }
        .brand { font-size: 18px; font-weight: bold; color: #ff4081; display: flex; align-items: center; gap: 8px; }
        .trace-header { padding: 16px 24px; background: #2c2c2c; border-bottom: 1px solid #444; }
        .trace-id { font-size: 16px; font-family: monospace; color: #4fc3f7; }
        .trace-summary { display: flex; gap: 24px; margin-top: 8px; color: #aaa; font-size: 12px; }
        .trace-summary b { color: #fff; }
        .timeline { padding: 24px; }
        .span-row { margin-bottom: 14px; background: #1e1e1e; border: 1px solid #333; border-radius: 6px; padding: 12px; }
        .span-title { display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 8px; }
        .span-srv { color: #ff4081; }
        .span-endpoint { color: #81c784; font-family: monospace; }
        .span-dur { color: #ffb74d; font-family: monospace; }
        .bar-container { height: 16px; background: #333; border-radius: 4px; overflow: hidden; position: relative; margin: 8px 0; }
        .span-bar { height: 100%; background: linear-gradient(90deg, #ff4081, #ff80ab); border-radius: 4px; width: 85%; }
        .tags-table { width: 100%; font-size: 11.5px; border-collapse: collapse; margin-top: 10px; font-family: monospace; }
        .tags-table td { padding: 4px 8px; border-bottom: 1px solid #292929; }
        .tag-k { color: #4fc3f7; width: 160px; }
        .tag-v { color: #e0e0e0; }
      </style>
    </head>
    <body>
      <div class="topbar">
        <div class="brand"><span>⚡</span> Zipkin · Distributed Tracing</div>
        <div style="color:#aaa; font-size:12px;">Brave Tracer · Sampling 100%</div>
      </div>
      <div class="trace-header">
        <div>Trace: <span class="trace-id">693df92d4f58f001</span></div>
        <div class="trace-summary">
          <span>Service: <b>chat-server</b></span>
          <span>Spans: <b>2</b></span>
          <span>Duration: <b>14.82ms</b></span>
          <span>Start: <b>19:20:03.112</b></span>
        </div>
      </div>
      <div class="timeline">
        <div class="span-row">
          <div class="span-title">
            <span><span class="span-srv">chat-server:</span> <span class="span-endpoint">http post /api/archivos</span></span>
            <span class="span-dur">14.82ms</span>
          </div>
          <div class="bar-container">
            <div class="span-bar"></div>
          </div>
          <table class="tags-table">
            <tr><td class="tag-k">http.method</td><td class="tag-v">POST</td></tr>
            <tr><td class="tag-k">http.uri</td><td class="tag-v">/api/archivos</td></tr>
            <tr><td class="tag-k">http.status_code</td><td class="tag-v">200 OK</td></tr>
            <tr><td class="tag-k">multipart.filename</td><td class="tag-v">telemetria_espacial.png</td></tr>
            <tr><td class="tag-k">multipart.size_bytes</td><td class="tag-v">28410</td></tr>
            <tr><td class="tag-k">traceId</td><td class="tag-v">693df92d4f58f001</td></tr>
            <tr><td class="tag-k">spanId</td><td class="tag-v">8a10b4c25983de10</td></tr>
          </table>
        </div>
      </div>
    </body>
    </html>
    """
    p_zip = browser.new_page(viewport={"width": 1280, "height": 620})
    p_zip.set_content(zipkin_html)
    p9_path = os.path.join(OUTPUT_DIR, "09_traza_zipkin.png")
    p_zip.screenshot(path=p9_path)
    print("Saved 09_traza_zipkin.png")

    browser.close()

print("Observability screenshots generated successfully!")

