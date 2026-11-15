import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

EVIDENCIAS_DIR = r"C:\Users\kevin\Downloads\chat-client\evidencias"
DOCX_CLIENT = r"C:\Users\kevin\Downloads\chat-client\Actividad_Semana_15_Chat_WebSockets_Observabilidad.docx"
DOCX_MAIN = r"C:\Users\kevin\Downloads\Actividad_Semana_15_Chat_WebSockets_Observabilidad.docx"

doc = Document()

# Configure standard margins (1 inch)
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

COLOR_BLACK = RGBColor(0, 0, 0)
COLOR_LINK = RGBColor(41, 128, 185)

def add_p(text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix + " ")
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_BLACK
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.font.color.rgb = COLOR_BLACK
    return p

def add_step_title(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_BLACK

def add_image(img_name, width_in=6.0):
    img_path = os.path.join(EVIDENCIAS_DIR, img_name)
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(12)
        r = p.add_run()
        r.add_picture(img_path, width=Inches(width_in))
    else:
        print(f"Warning: Image {img_name} not found!")

# =============================================================
# PÁGINA 1: PORTADA EXACTA (IDÉNTICA A LA SEMANA 14)
# =============================================================
# Logo de la Escuela Colombiana de Ingeniería
p_logo = doc.add_paragraph()
p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_logo.paragraph_format.space_before = Pt(20)
p_logo.paragraph_format.space_after = Pt(40)
r_logo = p_logo.add_run()
logo_path = os.path.join(EVIDENCIAS_DIR, "escuela_logo.png")
if os.path.exists(logo_path):
    r_logo.add_picture(logo_path, width=Inches(2.4))

def add_center_bold(text, size_pt, space_after=12):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(size_pt)
    r.font.bold = True
    r.font.color.rgb = COLOR_BLACK

add_center_bold("Diseño y Arquitectura de Software", 14, space_after=18)
add_center_bold("DOSW 2026-2", 14, space_after=18)
add_center_bold("Actividad Semana 15: Chat en vivo con WebSockets, STOMP y Observabilidad", 14, space_after=80)

add_center_bold("Profesor: Andres Martin Cantor Urrego", 13, space_after=80)

add_center_bold("Estudiante:", 12, space_after=6)
add_center_bold("Kevin Andrey Angel", 14, space_after=60)

add_center_bold("14/11/2026", 12, space_after=0)

# Salto de página tras la portada
doc.add_page_break()

# =============================================================
# PÁGINA 2: INTRODUCCIÓN Y REPOSITORIOS
# =============================================================
add_p(
    "En esta actividad se construyó un chat en tiempo real con WebSockets y STOMP usando Spring Boot en el backend (chat-server) y React con Vite en el frontend (chat-client). La conexión se mantiene abierta en ambos sentidos gracias al handshake 101 Switching Protocols. Se le dio una identidad visual propia con el tema de Estación Espacial Orbital y se le agregaron funciones interactivas (selector de emojis, subida de imágenes, notas de voz y estado de redacción). Para la observabilidad se configuraron métricas de negocio con Prometheus, logs centralizados con Loki, trazas distribuidas con Zipkin y un tablero en Grafana. A continuación están los pasos que fui haciendo con sus pantallazos."
)

p_rep = doc.add_paragraph()
p_rep.paragraph_format.space_before = Pt(8)
p_rep.paragraph_format.space_after = Pt(4)
r_rep = p_rep.add_run("Repositorios")
r_rep.font.name = "Arial"
r_rep.font.size = Pt(12)
r_rep.font.bold = True
r_rep.font.color.rgb = COLOR_BLACK

p_repo1 = doc.add_paragraph()
p_repo1.paragraph_format.space_after = Pt(2)
r1 = p_repo1.add_run("chat-server: ")
r1.font.bold = True
r1_link = p_repo1.add_run("https://github.com/nivek2329/chat-server")
r1_link.font.color.rgb = COLOR_LINK

p_repo2 = doc.add_paragraph()
p_repo2.paragraph_format.space_after = Pt(10)
r2 = p_repo2.add_run("chat-client: ")
r2.font.bold = True
r2_link = p_repo2.add_run("https://github.com/nivek2329/chat-client")
r2_link.font.color.rgb = COLOR_LINK

# =============================================================
# PASO 0: PREPARACIÓN
# =============================================================
add_step_title("Paso 0: Preparación")
add_p(
    "Primero revisé que tuviera Java 21 LTS, el wrapper de Maven con la versión 3.9.9 y Node.js para compilar el cliente en React. Creé los dos repositorios en GitHub: chat-server para el backend en Spring Boot y chat-client para el frontend con Vite."
)
add_image("00_preparacion_herramientas.png")

# =============================================================
# PASO 1 Y 2: SERVIDOR Y CONFIGURACIÓN WEBSOCKET
# =============================================================
add_step_title("Paso 1: Crear el servidor chat-server")
add_p(
    "Creé el proyecto en start.spring.io con Maven, Java 21 y las dependencias Spring Web y WebSocket. El chat utiliza STOMP sobre WebSocket, lo que nos da salas de suscripción y prefijos de envío como en un broker de mensajería."
)

add_step_title("Paso 2: Configurar el WebSocket y Handshake")
add_p(
    "En WebSocketConfig.java registré el endpoint /ws permitiendo cualquier origen con setAllowedOriginPatterns(\"*\"). El broker simple lo configuré en /topic para las suscripciones de los clientes y el prefijo de aplicación en /app para los mensajes que envía el navegador."
)
add_p(
    "En las DevTools de Chrome comprobé que al conectarse se envía una petición GET /ws con Upgrade: websocket y el servidor responde 101 Switching Protocols. A partir de ahí la conexión TCP queda abierta permanentemente."
)
add_image("01_handshake_ws_101.png")

# =============================================================
# PASO 3 Y 4: CONTROLADOR, MENSAJES Y SALIDA
# =============================================================
add_step_title("Paso 3: Mensajes y controller")
add_p(
    "Creé el record ChatMessage con tipo, autor, contenido y fecha. Los tipos soportados son TEXTO, IMAGEN, AUDIO, UNION y SALIDA. En ChatController agregué los métodos unirse() mapeado a /app/chat.unirse y enviar() mapeado a /app/chat.enviar, ambos enviando a /topic/sala."
)
add_p(
    "En la pestaña Messages de DevTools se ven las tramas STOMP CONNECT, CONNECTED, SUBSCRIBE y los frames MESSAGE que se transmiten por el mismo WebSocket."
)
add_image("02_frames_stomp.png")

add_step_title("Paso 4: Avisa cuando alguien sale")
add_p(
    "Creé la clase PresenciaListener con un @EventListener escuchando SessionDisconnectEvent. Cuando alguien cierra la pestaña del navegador, el listener recupera el nombre de usuario de la sesión y manda un mensaje con tipo SALIDA a /topic/sala para avisarle a toda la tripulación."
)
add_image("05_aviso_desconexion.png")

# =============================================================
# PASO 5, 6 Y 7: CLIENTE REACT Y PRUEBA MULTIUSUARIO
# =============================================================
add_step_title("Paso 5: Crear el cliente React")
add_p(
    "Creé el cliente con Vite usando la plantilla de React e instalé la librería @stomp/stompjs, que implementa el protocolo STOMP sobre el WebSocket nativo del navegador sin depender de SockJS."
)

add_step_title("Paso 6: Conectar, enviar y recibir")
add_p(
    "En App.jsx configuré la clase Client apuntando a ws://localhost:8080/ws con un reconnectDelay de 3000 ms. Al conectar se suscribe a /topic/sala y publica el evento de unión en /app/chat.unirse."
)

add_step_title("Paso 7: Probarlo en vivo con tres pestañas")
add_p(
    "Abrí el chat en tres pestañas con nombres y avatares distintos: Cmdte. Shepard, Cap. Miller y Dra. Ripley. Al chatear los mensajes llegan al instante en todas las ventanas sin recargar ni hacer peticiones HTTP adicionales."
)
add_image("03_chat_multiusuario_3pestanas.png")

# =============================================================
# PASO 8 Y 9: TEMA Y FUNCIONES EXTRA
# =============================================================
add_step_title("Paso 8: Tema de Estación Espacial Orbital")
add_p(
    "Elegí el tema de Estación Espacial Orbital. Cambié todo el front con una paleta cyberpunk espacial en fondo oscuro (#070913), acentos en cian (#06b6d4) y violeta (#8b5cf6), selector de insignia espacial en el login, badges de enlace activo (101 Switching) y marcas de tiempo de misión."
)

add_step_title("Paso 9: Funcionalidades extra (emojis, imágenes y voz)")
add_p(
    "Le agregué más de lo pedido: un selector de emojis flotante con emoji-picker-react, subida de imágenes con ArchivoController por HTTP multipart (por el WebSocket solo viaja la URL), grabación de notas de voz en directo con MediaRecorder y reproductor HTML5, y telemetría de 'está redactando...' en /topic/escribiendo."
)
add_image("04_selector_emojis_y_multimedia.png")

# =============================================================
# PASO 10 Y 11: ACTIVAR MÉTRICAS Y PROMETHEUS
# =============================================================
add_step_title("Paso 10: Actuator y Prometheus")
add_p(
    "Le agregué al servidor spring-boot-starter-actuator y micrometer-registry-prometheus. Expuse el endpoint /actuator/prometheus y activé los percentiles para las peticiones HTTP."
)

add_step_title("Paso 11: Métricas propias del chat")
add_p(
    "Creé la clase ChatMetrics con un Counter llamado chat.mensajes etiquetado por tipo, y un Gauge con AtomicInteger llamado chat.usuarios.conectados que sube al unirse y baja al desconectarse. Al entrar a /actuator/prometheus se ven las dos métricas registrando la actividad real."
)
add_image("06_actuator_prometheus.png")

# =============================================================
# PASO 12, 13 Y 14: TRAZAS, LOGS Y DOCKER COMPOSE
# =============================================================
add_step_title("Paso 12: Activar las trazas con Brave y Zipkin")
add_p(
    "Agregué micrometer-tracing-bridge-brave y zipkin-reporter-brave con muestreo al 100% apuntando a Zipkin en el puerto 9411. Con esto cada petición HTTP como la subida de archivos genera un traceId y spanId."
)

add_step_title("Paso 13: Mandar los logs a Loki")
add_p(
    "Agregué loki-logback-appender:1.5.2 y creé logback-spring.xml para enviar los logs a http://localhost:3100. En el formato del mensaje incluí traceId y spanId para correlacionarlos después con las trazas."
)

add_step_title("Paso 14: Levantar el stack de observabilidad")
add_p(
    "En la carpeta observabilidad/ creé docker-compose.yml con Prometheus, Loki, Zipkin y Grafana, junto con prometheus.yml y datasources.yml. Levanté los 4 contenedores con docker compose up -d."
)
add_image("07_docker_containers.png")

# =============================================================
# PASO 15 Y 16: TABLERO EN GRAFANA Y PRUEBA DE TRAZA
# =============================================================
add_step_title("Paso 15: Tablero en Grafana")
add_p(
    "En Grafana (puerto 3000) armé el tablero con los 6 paneles pedidos: Usuarios conectados (Stat), Mensajes por minuto por tipo (Time series), Latencia p95 al subir archivos (Time series), Memoria usada heap (Time series) y los dos paneles de logs de Loki (general y de solo errores). Exporté el JSON como dashboard-chat.json."
)
add_image("08_tablero_grafana.png")

add_step_title("Paso 16: Generar tráfico y seguir una traza")
add_p(
    "Subí una imagen espacial y en el log del servidor copié su traceId. Busqué ese traceId en Zipkin para ver la duración y las fases de la petición (14.8 ms), y en Grafana con Explore Loki verifiqué los logs asociados a esa misma transacción."
)
add_image("09_traza_zipkin.png")

# =============================================================
# PREGUNTAS TEÓRICAS (FORMATO EXACTO DEL PDF)
# =============================================================
p_preg = doc.add_paragraph()
p_preg.paragraph_format.space_before = Pt(18)
p_preg.paragraph_format.space_after = Pt(8)
p_preg.paragraph_format.keep_with_next = True
r_preg = p_preg.add_run("Preguntas")
r_preg.font.name = "Arial"
r_preg.font.size = Pt(13)
r_preg.font.bold = True
r_preg.font.color.rgb = COLOR_BLACK

add_p(
    "En HTTP normal el cliente siempre tiene que iniciar la petición, entonces para simular tiempo real le toca estar preguntando al servidor a cada rato si hay mensajes nuevos (polling). Eso satura la red porque cada segundo manda cabeceras repetidas y abre conexiones que la mayoría de veces vuelven vacías. Con WebSocket se hace un solo handshake al principio (101 Switching Protocols) y el canal TCP se queda abierto; cuando alguien envía un mensaje, el servidor se lo empuja a los demás de inmediato sin que ellos tengan que volver a preguntar.",
    bold_prefix="¿Por qué un chat con HTTP normal tendría que estar preguntándole al servidor cada segundo, y qué cambia con WebSocket?"
)

add_p(
    "Porque WebSocket está pensado para tramas de texto livianas y mensajes rápidos. Si uno mete una foto de varios megas o un archivo de audio por el WebSocket, bloquea el canal para los demás usuarios y le mete retardo a los mensajes de texto. Por eso el archivo pesado se sube por HTTP normal a un endpoint REST, el servidor lo guarda en disco y por el WebSocket solo viaja la URL en un texto cortico.",
    bold_prefix="¿Por qué las imágenes y los audios se suben por HTTP y no viajan dentro del WebSocket?"
)

add_p(
    "Cuando el servidor se apaga los WebSockets se caen y los clientes quedan desconectados. La opción reconnectDelay de @stomp/stompjs hace que el cliente intente volver a conectarse automáticamente cada 3 segundos sin que el usuario tenga que recargar la página. Apenas el servidor vuelve a subir, el cliente se reconecta solo y restaura sus suscripciones a la sala.",
    bold_prefix="Si el servidor se reinicia, ¿qué pasa con los usuarios conectados y qué hace reconnectDelay?"
)

add_p(
    "La métrica que avisaría primero es una subida en los errores HTTP al conectar (códigos 5xx) o la caída repentina de chat_usuarios_conectados a cero. Le pondría una alerta si la tasa de errores de conexión supera el 5% durante un minuto, o si la latencia al subir archivos supera los 2 segundos.",
    bold_prefix="¿Qué métrica te avisaría primero de que el chat está fallando, y qué alerta pondrías sobre ella?"
)

add_p(
    "En Style Radar se beneficiaría el servicio de Notificaciones (para avisar al instante cuando una tienda saca una nueva prenda o hay una oferta en vivo) y el chat con asesores de imagen. A cada microservicio le armaría un tablero con las cuatro métricas doradas: tasa de peticiones por segundo, latencia percentil 95, tasa de errores 5xx y uso de memoria heap de la JVM, más los logs filtrados por traceId.",
    bold_prefix="En Style Radar, ¿qué servicio se beneficiaría de WebSockets y qué tablero le armarías a cada microservicio?"
)

# Guardar en ambas rutas
doc.save(DOCX_CLIENT)
print("Guardado en:", DOCX_CLIENT)

doc.save(DOCX_MAIN)
print("Guardado en:", DOCX_MAIN)

