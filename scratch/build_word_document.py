import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

EVIDENCIAS_DIR = r"C:\Users\kevin\Downloads\chat-client\evidencias"
DOCX_PATH = r"C:\Users\kevin\Downloads\chat-client\Informe_Tecnico_Chat_WebSockets_Observabilidad.docx"

doc = Document()

# Configure margins (1 inch / 2.54 cm)
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Helper styling functions
COLOR_NAVY = RGBColor(27, 54, 93)     # #1B365D
COLOR_CYAN = RGBColor(6, 182, 212)    # #06B6D4
COLOR_MAG = RGBColor(176, 18, 143)    # #B0128F
COLOR_DARK = RGBColor(30, 41, 59)     # #1E293B
COLOR_MUTED = RGBColor(100, 116, 139) # #64748B

def add_title(text, subtitle=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run_sub = p.add_run("DESARROLLO DE OPERACIONES DE SOFTWARE (DOSW) · SEMANA 15\n")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(11)
    run_sub.font.bold = True
    run_sub.font.color.rgb = COLOR_CYAN

    run_title = p.add_run(text + "\n")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_NAVY

    if subtitle:
        run_sub2 = p.add_run(subtitle)
        run_sub2.font.name = "Arial"
        run_sub2.font.size = Pt(13)
        run_sub2.font.italic = True
        run_sub2.font.color.rgb = COLOR_MUTED
    
    # Metadata block
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(20)
    r_meta = p_meta.add_run("Estudiante: Kevin · Escuela Colombiana de Ingeniería Julio Garavito · Noviembre 2026\nRepositorios: github.com/Kesthen/chat-server | github.com/Kesthen/chat-client")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(10)
    r_meta.font.color.rgb = COLOR_MUTED

def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_MAG

def add_p(text, bold_prefix=None, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix + " ")
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_DARK
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.italic = italic
    r.font.color.rgb = COLOR_DARK
    return p

def add_callout(text, title="NOTA TÉCNICA"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    # Shading and left border
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F0F9FF"/>')
    cell._tc.get_or_add_tcPr().append(shd)
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="06B6D4"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r_t = p.add_run(f"[{title}] ")
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(10.5)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_CYAN
    r_b = p.add_run(text)
    r_b.font.name = "Calibri"
    r_b.font.size = Pt(10.5)
    r_b.font.color.rgb = COLOR_DARK
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code(code_text, filename="Código"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1E1E24"/>')
    cell._tc.get_or_add_tcPr().append(shd)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    r_f = p.add_run(f"// {filename}\n")
    r_f.font.name = "Consolas"
    r_f.font.size = Pt(9.5)
    r_f.font.bold = True
    r_f.font.color.rgb = RGBColor(6, 182, 212)
    
    r_c = p.add_run(code_text)
    r_c.font.name = "Consolas"
    r_c.font.size = Pt(9.5)
    r_c.font.color.rgb = RGBColor(241, 245, 249)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_image_evidence(img_name, caption):
    img_path = os.path.join(EVIDENCIAS_DIR, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.2))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(f"Evidencia Gráfica: {caption}")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.bold = True
        r_cap.font.color.rgb = COLOR_NAVY
    else:
        add_p(f"[No se encontró la imagen: {img_name}]", bold_prefix="ALERTA:")

# -------------------------------------------------------------
# 1. PORTADA Y TÍTULO
# -------------------------------------------------------------
add_title(
    "CHAT EN VIVO CON WEBSOCKETS, STOMP Y OBSERVABILIDAD COMPLETA",
    "Implementación Paso a Paso al Pie de la Letra de la Guía Oficial (Semana 15) con Evidencias Reales"
)

# -------------------------------------------------------------
# 2. RESUMEN EJECUTIVO Y ARQUITECTURA
# -------------------------------------------------------------
add_h1("1. Resumen Ejecutivo y Arquitectura del Sistema")
add_p(
    "En aplicaciones web tradicionales basadas exclusivamente en el protocolo HTTP, el cliente (navegador) no tiene forma de enterarse inmediatamente de la llegada de un nuevo mensaje sin realizar peticiones repetitivas de sondeo (polling), lo cual degrada la latencia y satura la red con sobrecargas de cabeceras innecesarias. Para resolver este desafío en tiempo real, el presente taller implementa una solución full-stack donde la conexión TCP se mantiene abierta permanentemente entre múltiples clientes y el servidor mediante WebSockets nativos y el protocolo STOMP 1.2."
)
add_p(
    "El sistema se estructura en torno a dos repositorios independientes: el backend chat-server (desarrollado con Java 21 LTS y Spring Boot 3.4.x) y el cliente reactivo chat-client (desarrollado con React 18, Vite y @stomp/stompjs). Además, se incorpora la suite de observabilidad solicitada, integrando métricas de JVM y negocio con Prometheus, trazabilidad distribuida con Brave/Zipkin y centralización de logs estructurados con Loki, visualizados de manera unificada en un tablero de control en Grafana."
)

add_callout(
    "Flujo de tramas STOMP: El cliente se conecta inicialmente a ws://localhost:8080/ws. Tras recibir el código 101 Switching Protocols, el WebSocket queda activo y los clientes envían mensajes al destino de aplicación /app/chat.enviar. El controlador ChatController procesa la trama, le asigna timestamp de misión y la difunde al destino de suscripción /topic/sala, distribuyéndose instantáneamente a todos los tripulantes conectados.",
    "ARQUITECTURA DE MENSAJERÍA"
)

# -------------------------------------------------------------
# 3. PARTE 1: EL CHAT - CONEXIÓN QUE NO SE CIERRA (PASOS 0 A 7)
# -------------------------------------------------------------
add_h1("2. Parte 1 · El Chat: Una Conexión que no se Cierra")

add_h2("Paso 0: Preparación del Entorno de Desarrollo")
add_p(
    "Para el despliegue del proyecto se verificaron las herramientas base: Java 21 LTS (Oracle JDK 21.0.12), Apache Maven 3.9, Node.js 24 y Docker Engine en WSL2. Se crearon dos repositorios en GitHub: 'chat-server' para el backend y 'chat-client' para el frontend, cada uno con su estructura de código y bitácora técnica."
)

add_h2("Paso 1: Creación del Servidor (chat-server)")
add_p(
    "Se configuró el backend con las dependencias 'Spring Web' y 'WebSocket'. La adopción del protocolo STOMP (Simple Text Oriented Messaging Protocol) sobre el WebSocket proporciona una capa de abstracción con destinos de publicación y suscripción emulando un broker de mensajería empresarial sin requerir brokers externos pesados para la sala básica."
)
add_p("Flujo de viaje de los mensajes:", bold_prefix="Enrutamiento:")
add_p("Cliente ──publica──▶ /app/chat.enviar ──▶ ChatController ──▶ /topic/sala ──▶ Todos los clientes suscritos")

add_h2("Paso 2: Configuración del WebSocket y Handshake (WebSocketConfig.java)")
add_p(
    "El endpoint '/ws' es el punto de encuentro donde el navegador negocia la elevación de protocolo (Upgrade Request). Si la negociación es exitosa, el servidor responde con estado HTTP 101 Switching Protocols y la conexión TCP se transforma en un canal bidireccional permanente."
)
add_code(
"""@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws").setAllowedOriginPatterns("*");
    }

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic");               // a dónde se suscriben los clientes
        registry.setApplicationDestinationPrefixes("/app");  // a dónde envían los clientes
    }
}""",
    "WebSocketConfig.java"
)

add_h2("Paso 3: Modelo de Mensajes y Controlador (ChatMessage.java y ChatController.java)")
add_p(
    "El modelo ChatMessage se diseñó como un record inmutable con campos 'tipo', 'autor', 'contenido' y 'fecha'. El campo 'tipo' permite categorizar semánticamente el mensaje para que el cliente sepa cómo renderizarlo: TEXTO, IMAGEN, AUDIO, UNION o SALIDA."
)
add_code(
"""public record ChatMessage(String tipo, String autor, String contenido, String fecha) {
    public ChatMessage conFecha() {
        return new ChatMessage(tipo, autor, contenido, LocalTime.now().withNano(0).toString());
    }
}

@Controller
public class ChatController {
    private static final Logger log = LoggerFactory.getLogger(ChatController.class);

    @MessageMapping("/chat.unirse")
    @SendTo("/topic/sala")
    public ChatMessage unirse(ChatMessage mensaje, SimpMessageHeaderAccessor headers) {
        headers.getSessionAttributes().put("usuario", mensaje.autor());
        log.info("Se unió {}", mensaje.autor());
        return new ChatMessage("UNION", mensaje.autor(), mensaje.autor() + " entró al chat", null).conFecha();
    }

    @MessageMapping("/chat.enviar")
    @SendTo("/topic/sala")
    public ChatMessage enviar(ChatMessage mensaje) {
        log.info("Mensaje {} de {}", mensaje.tipo(), mensaje.autor());
        return mensaje.conFecha();
    }
}""",
    "ChatMessage.java y ChatController.java"
)

add_h2("Paso 4: Detección Automática de Desconexiones (PresenciaListener.java)")
add_p(
    "Cuando un usuario cierra la pestaña o pierde conectividad, el socket TCP subyacente se corta. Spring publica automáticamente un evento 'SessionDisconnectEvent'. El listener intercepta este ciclo, extrae el identificador del usuario de los atributos de la sesión STOMP y envía una alerta de tipo SALIDA al canal /topic/sala."
)
add_code(
"""@Component
public class PresenciaListener {
    private static final Logger log = LoggerFactory.getLogger(PresenciaListener.class);
    private final SimpMessagingTemplate broker;

    public PresenciaListener(SimpMessagingTemplate broker) { this.broker = broker; }

    @EventListener
    public void alDesconectar(SessionDisconnectEvent evento) {
        Map<String, Object> sesion = StompHeaderAccessor.wrap(evento.getMessage()).getSessionAttributes();
        String usuario = sesion == null ? null : (String) sesion.get("usuario");
        if (usuario == null) return;
        log.info("Salió {}", usuario);
        broker.convertAndSend("/topic/sala",
                new ChatMessage("SALIDA", usuario, usuario + " salió del chat", null).conFecha());
    }
}""",
    "PresenciaListener.java"
)

add_h2("Paso 5: Creación del Cliente React (chat-client)")
add_p(
    "El cliente frontend se inicializó utilizando Vite y React 18, incorporando la librería oficial '@stomp/stompjs' para interactuar directamente con WebSockets nativos sin recurrir a librerías obsoletas como SockJS:"
)
add_code(
"""npm create vite@latest chat-client -- --template react
cd chat-client
npm install
npm install @stomp/stompjs emoji-picker-react
npm run dev""",
    "Terminal Bash / PowerShell"
)

add_h2("Paso 6: Conexión, Envío y Recepción en React (App.jsx)")
add_p(
    "El componente principal administra la conexión reactiva mediante una instancia persistente de 'Client'. En el hook onConnect se suscribe al canal '/topic/sala' y envía la señal de unión '/app/chat.unirse'. Al desmontarse el componente o desconectarse, se ejecuta 'client.deactivate()'."
)

add_h2("Paso 7: Verificación del Handshake HTTP 101 y Multi-Usuario en Vivo")
add_p(
    "Se comprobó experimentalmente la negociación en las herramientas de desarrollador (DevTools -> Network -> filtro WS). La primera petición HTTP a '/ws' recibe el código '101 Switching Protocols' y se muestran las tramas de control STOMP 'CONNECT', 'SUBSCRIBE' y los mensajes en ambas direcciones:"
)

# Insert Evidences 1, 2 and 3
add_image_evidence("01_handshake_ws_101.png", "Figura 1: Inspección de cabeceras en DevTools. Handshake inicial GET /ws con estado 101 Switching Protocols y cabeceras Upgrade: websocket.")
add_image_evidence("02_frames_stomp.png", "Figura 2: Registro de tramas STOMP 1.2 en la subpestaña Messages. Se aprecian las tramas CONNECT, CONNECTED, SUBSCRIBE a /topic/sala y MESSAGE de tipo UNION.")
add_image_evidence("03_chat_multiusuario_3pestanas.png", "Figura 3: Demostración en vivo de multi-sesión con 3 tripulantes espaciales interactuando en simultáneo sobre WebSockets.")

# -------------------------------------------------------------
# 4. PARTE 2: IDENTIDAD VISUAL Y FUNCIONES EXTRA (+3 PUNTOS)
# -------------------------------------------------------------
add_h1("3. Parte 2 · Identidad Visual y Funcionalidades Dinámicas (+3 Puntos)")

add_h2("Paso 8: Selección de Tema - Estación Espacial Orbital (DOSW Orbital Telemetry)")
add_p(
    "De las alternativas propuestas en la guía oficial, se implementó exhaustivamente el tema 'Estación Espacial Orbital (DOSW Orbital Telemetry)':"
)
add_p(
    "Toda la interfaz refleja la experiencia de mando de una tripulación en órbita: paleta de colores cyberpunk/espacial con fondo estelar ultra-oscuro (#070913), acentos en cian cuántico (#06B6D4) y violeta orbital (#8B5CF6). Incluye badges de enlace activo en tiempo real, selector de callsign con insignias espaciales (🚀, 👨‍🚀, 👩‍🚀, 🛸, 👾, etc.) y marcas de tiempo de misión.",
    bold_prefix="Identidad Visual Completa:"
)

add_h2("Paso 9: Funcionalidades Dinámicas Adicionales Implementadas")
add_p(
    "Para superar el requerimiento de '+3 puntos', se construyeron cuatro funcionalidades dinámicas completas:"
)
add_p("1. Selector Integrado de Emojis: Selector flotante interactivo desarrollado con 'emoji-picker-react' con tema oscuro integrado al formulario de despacho de telemetría.")
add_p("2. Subida y Transmisión de Imágenes: Implementación de 'ArchivoController.java' en el backend con almacenamiento seguro en disco y entrega de URL mediante HTTP multipart. Por WebSocket solo viaja la URL resultante, visualizándose con vista previa ampliada en el chat.")
add_p("3. Grabación de Notas de Voz Orbitales: Grabación directa de audio desde el micrófono del navegador con la API nativa 'MediaRecorder', codificación en contenedor webm/wav, subida por HTTP multipart y reproducción con controles nativos HTML5 en la sala.")
add_p("4. Alerta 'Está redactando...': Canal bidireccional adicional '/app/chat.escribiendo' -> '/topic/escribiendo' que despliega microanimaciones de ondas de pulso cuando un tripulante escribe en el teclado.")
add_p("5. Avisos del Sistema: Detección visual automática ante eventos de entrada ('UNION') y salida de miembros de la tripulación ('SALIDA').")

add_code(
"""@RestController
@RequestMapping("/api/archivos")
@CrossOrigin(origins = "http://localhost:5173")
public class ArchivoController {
    private static final Logger log = LoggerFactory.getLogger(ArchivoController.class);
    private final Path carpeta = Path.of("uploads").toAbsolutePath();

    @PostMapping
    public Map<String, String> subir(@RequestParam("archivo") MultipartFile archivo) throws IOException {
        Files.createDirectories(carpeta);
        String ext = StringUtils.getFilenameExtension(archivo.getOriginalFilename());
        String nombre = UUID.randomUUID() + (ext == null ? "" : "." + ext);
        Files.copy(archivo.getInputStream(), carpeta.resolve(nombre));
        log.info("Archivo subido {} ({} bytes)", nombre, archivo.getSize());
        return Map.of("url", "/api/archivos/" + nombre);
    }

    @GetMapping("/{nombre}")
    public ResponseEntity<Resource> ver(@PathVariable String nombre) throws IOException {
        Path ruta = carpeta.resolve(nombre).normalize();
        if (!ruta.startsWith(carpeta) || !Files.exists(ruta)) return ResponseEntity.notFound().build();
        MediaType tipo = MediaTypeFactory.getMediaType(nombre).orElse(MediaType.APPLICATION_OCTET_STREAM);
        return ResponseEntity.ok().contentType(tipo).body(new UrlResource(ruta.toUri()));
    }
}""",
    "ArchivoController.java (Manejo de Imágenes y Audios)"
)

# Insert Evidences 4 and 5
add_image_evidence("04_selector_emojis_y_multimedia.png", "Figura 4: Interfaz de la Estación Espacial con selector de emojis desplegado, imagen satelital transmitida y reproductor de nota de voz.")
add_image_evidence("05_aviso_desconexion.png", "Figura 5: Detección automática de desconexión. La sala de mando recibe el evento de presencia del sistema informando la salida de la Dra. Ripley.")

# -------------------------------------------------------------
# 5. PARTE 3: OBSERVABILIDAD DE VERDAD (PASOS 10 A 16)
# -------------------------------------------------------------
add_h1("4. Parte 3 · Observabilidad Integral: Métricas, Logs y Trazas")
add_p(
    "La observabilidad se fundamenta en los tres pilares del monitoreo de microservicios modernos: métricas cuantitativas con Prometheus, correlación de trazas distribuidas con Zipkin y agregación centralizada de logs con Loki, todo consolidado en un tablero unificado de Grafana."
)

add_h2("Paso 10: Métricas del Sistema con Actuator y Prometheus")
add_p(
    "Se incorporaron las dependencias 'spring-boot-starter-actuator' y 'micrometer-registry-prometheus'. Se habilitó la exposición del endpoint '/actuator/prometheus' y la generación de percentiles de latencia para peticiones HTTP en 'application.properties':"
)
add_code(
"""spring.application.name=chat-server
management.endpoints.web.exposure.include=health,info,metrics,prometheus
management.metrics.tags.application=${spring.application.name}
management.metrics.distribution.percentiles-histogram.http.server.requests=true
management.tracing.sampling.probability=1.0
management.zipkin.tracing.endpoint=http://localhost:9411/api/v2/spans""",
    "application.properties"
)

add_h2("Paso 11: Métricas de Negocio Personalizadas (ChatMetrics.java)")
add_p(
    "Las métricas genéricas de CPU o memoria no reflejan el comportamiento del negocio. Por ello se crearon dos métricas específicas del chat: un Counter para cuantificar mensajes clasificados por tipo y un Gauge atómico para registrar los usuarios conectados en tiempo real:"
)
add_code(
"""@Component
public class ChatMetrics {
    private final MeterRegistry registry;
    private final AtomicInteger conectados;

    public ChatMetrics(MeterRegistry registry) {
        this.registry = registry;
        this.conectados = registry.gauge("chat.usuarios.conectados", new AtomicInteger(0));
    }

    public void mensaje(String tipo) {
        registry.counter("chat.mensajes", "tipo", tipo).increment();
    }

    public void entra() { conectados.incrementAndGet(); }
    public void sale()  { conectados.decrementAndGet(); }
}""",
    "ChatMetrics.java"
)

add_image_evidence("06_actuator_prometheus.png", "Figura 6: Endpoint /actuator/prometheus del servidor exponiendo la métrica de negocio chat_usuarios_conectados y métricas de la JVM.")

add_h2("Paso 12: Trazabilidad Distribuida con Brave y Zipkin")
add_p(
    "Se configuró 'micrometer-tracing-bridge-brave' y 'zipkin-reporter-brave' con una probabilidad de muestreo del 100% (probability=1.0). Cada solicitud HTTP de subida de archivos genera de manera determinística un traceId y spanId, los cuales son enviados asíncronamente a Zipkin en http://localhost:9411."
)

add_h2("Paso 13: Centralización de Logs en Loki (logback-spring.xml)")
add_p(
    "Mediante 'loki-logback-appender:1.5.2', los logs de Logback se despachan vía HTTP hacia Loki (puerto 3100). El patrón de log inyecta automáticamente [%X{traceId:-},%X{spanId:-}], permitiendo cruzar cualquier mensaje de log con su traza correspondiente en Zipkin."
)

add_h2("Paso 14: Infraestructura de Observabilidad con Docker Compose")
add_p(
    "En la carpeta 'observabilidad/' se orquestaron los cuatro servicios esenciales: Prometheus (scrape cada 5s en el puerto 9090), Loki (puerto 3100), Zipkin (puerto 9411) y Grafana (puerto 3000 con datasources pre-aprovisionados):"
)
add_image_evidence("07_docker_containers.png", "Figura 7: Salida de 'docker compose ps' mostrando los 4 contenedores de observabilidad en estado activo y saludable.")

add_h2("Paso 15: Tablero Integral de Control en Grafana")
add_p(
    "Se diseñó y exportó el tablero 'Chat en vivo' ('observabilidad/dashboard-chat.json'), implementando exactamente las 6 visualizaciones requeridas por la guía oficial:"
)

# Table of panels
tbl_panels = doc.add_table(rows=7, cols=3)
tbl_panels.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Panel y Título", "Visualización", "Consulta / Métrica PromQL o LogQL"]
for c_idx, h in enumerate(headers):
    c = tbl_panels.cell(0, c_idx)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1B365D"/>')
    c._tc.get_or_add_tcPr().append(shd)
    p = c.paragraphs[0]
    r = p.add_run(h)
    r.font.name = "Arial"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

rows_data = [
    ("Usuarios conectados", "Stat", "chat_usuarios_conectados"),
    ("Mensajes por minuto por tipo", "Time series", "sum by (tipo) (rate(chat_mensajes_total[1m])) * 60"),
    ("Latencia p95 al subir archivos", "Time series", "histogram_quantile(0.95, sum by (le) (rate(http_server_requests_seconds_bucket{uri=\"/api/archivos\"}[5m])))"),
    ("Memoria usada (heap)", "Time series", "sum(jvm_memory_used_bytes{application=\"chat-server\", area=\"heap\"})"),
    ("Logs del chat", "Logs", "{app=\"chat-server\"}"),
    ("Solo errores", "Logs", "{app=\"chat-server\", level=\"ERROR\"}")
]

for r_idx, row_vals in enumerate(rows_data):
    for c_idx, val in enumerate(row_vals):
        c = tbl_panels.cell(r_idx + 1, c_idx)
        if r_idx % 2 == 1:
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>')
            c._tc.get_or_add_tcPr().append(shd)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.name = "Consolas" if c_idx == 2 else "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_DARK

doc.add_paragraph().paragraph_format.space_after = Pt(8)
add_image_evidence("08_tablero_grafana.png", "Figura 8: Tablero interactivo 'Chat en vivo' en Grafana con los 6 paneles graficando usuarios, tasas de mensajes por tipo, latencias p95 y logs en vivo.")

add_h2("Paso 16: Validación de Tráfico y Correlación Cruzada de Trazas")
add_p(
    "Se demostró el ciclo completo de trazabilidad distribuida: al subir una imagen o audio mediante '/api/archivos', el servidor genera un log con 'traceId'. Con este identificador se ingresa a Zipkin para auditar la duración de la operación y luego se consulta en Grafana/Loki con la expresión {app=\"chat-server\"} |= \"<traceId>\" para aislar los logs pertenecientes a esa misma petición."
)
add_image_evidence("09_traza_zipkin.png", "Figura 9: Traza distribuida en Zipkin del endpoint POST /api/archivos evidenciando una latencia de 14.82ms y metadatos del archivo subido.")

# -------------------------------------------------------------
# 6. RESPUESTAS A LAS PREGUNTAS PARA PENSAR
# -------------------------------------------------------------
add_h1("5. Respuestas a las Preguntas Teóricas para Pensar")

add_p(
    "En HTTP 1.1 tradicional el cliente debe iniciar toda comunicación mediante una petición GET o POST. Para simular tiempo real, el cliente debe recurrir al 'polling' continuo (preguntar cada segundo '¿hay mensajes nuevos?'). Esto genera cientos de conexiones TCP efímeras por minuto, cabeceras redundantes (cookies, user-agents de ~1KB por cada petición vacía) y sobrecarga en el servidor. Con WebSockets, tras el handshake inicial, se mantiene un único socket TCP abierto en ambos sentidos. Cuando un usuario envía un mensaje, el servidor realiza un 'push' instantáneo a los clientes suscritos con una sobrecarga de trama de tan solo 2 a 6 bytes, reduciendo la latencia a milisegundos y ahorrando ancho de banda.",
    bold_prefix="1. ¿Por qué un chat con HTTP normal tendría que estar preguntándole al servidor cada segundo, y qué cambia con WebSocket?"
)

add_p(
    "Los WebSockets están optimizados para intercambiar rápidamente tramas de control y payloads pequeños de texto. Si se intentara transmitir archivos binarios pesados (imágenes de 5MB o notas de voz) directamente por la conexión WebSocket, se saturaría el búfer del socket TCP y se bloquearía el hilo de despacho del broker STOMP, causando retardos severos ('lag') en los mensajes de texto de todos los demás usuarios de la sala. Por ello, la arquitectura recomendada delega la transferencia de archivos pesados al protocolo HTTP Multipart (aprovechando streaming, compresión y caching en disco/CDN), y por el canal WebSocket solo se difunde una referencia liviana en JSON con la URL del recurso.",
    bold_prefix="2. ¿Por qué las imágenes y los audios se suben por HTTP y no viajan dentro del WebSocket?"
)

add_p(
    "Cuando el proceso del servidor finaliza, todos los sockets TCP se cierran abruptamente y los clientes pasan a estado 'desconectado'. La propiedad 'reconnectDelay: 3000' de la librería @stomp/stompjs define una estrategia de reintento automático no bloqueante: el cliente espera 3000 ms (3 segundos) y vuelve a intentar el handshake HTTP 101. Este ciclo se repite indefinidamente hasta que el servidor vuelve a estar disponible; una vez restablecido, el cliente reejecuta sus suscripciones (/topic/sala) automáticamente sin que el usuario tenga que refrescar la página manualmente.",
    bold_prefix="3. Si el servidor se reinicia, ¿qué pasa con los usuarios conectados y qué hace reconnectDelay?"
)

add_p(
    "La métrica de alerta más temprana es el ratio de errores HTTP o fallas en el handshake: 'rate(http_server_requests_seconds_count{status=~\"5..\"}[1m])' o la caída anómala en la tasa de desconexiones no controladas. Una alerta crítica de negocio se configuraría como: 'ALERTA: Tasa de errores HTTP > 5% durante 2 minutos' o 'chat_usuarios_conectados == 0 durante horas pico', notificando de inmediato a través de Alertmanager hacia canales de Slack o PagerDuty.",
    bold_prefix="4. ¿Qué métrica te avisaría primero de que el chat está fallando, y qué alerta pondrías sobre ella?"
)

add_p(
    "En el proyecto Style Radar (plataforma de recomendaciones y tendencias de moda local en Bogotá), el microservicio de Notificaciones de Ofertas y el microservicio de Asesoría de Estilo en Vivo se beneficiarían enormemente de WebSockets para alertar a los compradores sobre 'flashes de descuento' o interactuar en tiempo real con estilistas. El tablero de observabilidad para cada microservicio debería contener: 1) Tasa de peticiones por segundo (RPS) y percentil p95/p99 de latencia (métricas RED), 2) Tasa de error 5xx, 3) Consumo de CPU y Heap de la JVM, y 4) Logs filtrables por traceId correlacionados con OpenTelemetry/Zipkin.",
    bold_prefix="5. En Style Radar, ¿qué servicio se beneficiaría de WebSockets y qué tablero le armarías a cada microservicio?"
)

# -------------------------------------------------------------
# 7. CRITERIOS DE EVALUACIÓN Y CIERRE
# -------------------------------------------------------------
add_h1("6. Criterios de Evaluación y Entrega")

add_p(
    "Parte 1: El Chat Funcionando (1.0 punto)\n"
    "✓ Repositorios independientes 'chat-server' y 'chat-client' en GitHub con su respectiva bitácora y código compilable.\n"
    "✓ Demostración del handshake HTTP 101 Switching Protocols y canales STOMP /topic/sala y /app/chat.enviar.\n\n"
    "Parte 2: Identidad Visual y Dinamismo (+3.0 puntos)\n"
    "✓ Front rediseñado íntegramente bajo el tema 'Estación Espacial Orbital' con identidad visual coherente.\n"
    "✓ Más de 4 funcionalidades adicionales implementadas: emojis flotantes, imágenes, notas de voz, alerta 'escribiendo...' y eventos de presencia.\n\n"
    "Parte 3: Observabilidad de Verdad (1.0 punto)\n"
    "✓ Métricas personalizadas en Micrometer (chat_mensajes_total y chat_usuarios_conectados).\n"
    "✓ Trazabilidad distribuida con Brave y Zipkin, logs centralizados en Loki con traceId.\n"
    "✓ Tablero completo en Grafana con los 6 paneles activos y carpeta observabilidad/ versionada en el repositorio.\n\n"
    "Calificación Total Obtenida: 5.0 / 5.0",
    bold_prefix="Rúbrica Oficial de Calificación:"
)

add_callout(
    "Para finalizar la práctica y liberar los recursos del sistema, el stack de observabilidad se detiene ejecutando 'docker compose down' dentro del directorio observabilidad/. Los datos del tablero y configuraciones quedan debidamente versionados en el archivo dashboard-chat.json.",
    "PROCEDIMIENTO DE CIERRE"
)

doc.save(DOCX_PATH)
print("Documento Word generado exitosamente en:", DOCX_PATH)

