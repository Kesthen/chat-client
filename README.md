# 🛸 Chat Client - Interfaz Orbital React (DOSW Semana 15)

Cliente frontend reactivo con estética de **Estación Espacial Orbital**, desarrollado con **React**, **Vite** y comunicación en tiempo real sobre **WebSockets nativos** mediante el protocolo **STOMP 1.2** (`@stomp/stompjs`).

---

## 🌌 1. Características e Identidad Visual (Parte 2: +3 Puntos)

El frontend ha sido diseñado completamente bajo la identidad de una **Estación Espacial Orbital (DOSW Orbital Telemetry)**:
- **Tema Espacial:** Paleta cyberpunk espacial (`#070913`, cian eléctrico `#06b6d4`, violeta orbital `#8b5cf6`), tipografía temática (*Orbitron* y *Poppins*), badges de telemetría y efectos de resplandor cuántico.
- **Selector de Insignias / Avatares:** Al ingresar, el tripulante puede elegir su insignia espacial (🚀, 👨‍🚀, 👩‍🚀, 🛸, 🛰️, 👾, ⚡, 🤖) y su callsign identificador.
- **Selector Integrado de Emojis:** Selector flotante mediante `emoji-picker-react` con búsqueda y paleta oscura.
- **Subida de Archivos y Transmisiones Visuales:** Envío de imágenes directamente a `/api/archivos` mediante HTTP `POST` multipart y difusión de su URL por el WebSocket.
- **Transmisiones de Voz:** Grabación de notas de voz en tiempo real con la API del navegador `MediaRecorder`, conversión a formato contenedor y reproducción integrada.
- **Alerta de Telemetría ("Está redactando..."):** Indicador sincronizado con microanimación de pulsos cuando otro tripulante teclea en el canal `/topic/escribiendo`.
- **Detección de Presencia:** Anuncios automáticos del sistema ante el ingreso (`UNION`) o desconexión (`SALIDA`) de miembros de la tripulación.
- **Conexión Resiliente:** Reconexión automática cada 3 segundos (`reconnectDelay: 3000`) si el enlace sufre interrupciones.

---

## 📡 2. Destinos STOMP Utilizados

- **Broker URL:** `ws://localhost:8080/ws`
- **Suscripciones del Cliente:**
  - `/topic/sala`: Recibe todas las transmisiones de texto, imágenes, audio y eventos de presencia.
  - `/topic/escribiendo`: Recibe la señal de redacción de los demás tripulantes.
- **Publicaciones del Cliente:**
  - `/app/chat.unirse`: Envía el mensaje inicial de ingreso a la sala de mando.
  - `/app/chat.enviar`: Envía el payload con el tipo (`TEXTO`, `IMAGEN`, `AUDIO`), autor y contenido.
  - `/app/chat.escribiendo`: Envía el nombre del usuario que está redactando.

---

## 🚀 3. Instrucciones de Ejecución

### Prerrequisitos
- **Node.js 20+** o **Node.js 24+**
- **npm** o **pnpm**
- Servidor `chat-server` en ejecución en `http://localhost:8080`

### Pasos para iniciar el cliente
```bash
# 1. Clonar el repositorio
git clone https://github.com/Kesthen/chat-client.git
cd chat-client

# 2. Instalar dependencias
npm install

# 3. Iniciar el servidor de desarrollo Vite
npm run dev
```

La aplicación estará disponible inmediatamente en `http://localhost:5173`.

---

## 🛰️ 4. Inspección del Handshake en DevTools

Para comprobar la arquitectura WebSocket explicada en clase:
1. Abre Google Chrome o Edge en `http://localhost:5173`.
2. Presiona `F12` para abrir las **DevTools** y dirígete a la pestaña **Network**.
3. Selecciona el filtro **WS** (WebSockets).
4. Recarga la página y conéctate:
   - Observarás la petición inicial `GET /ws` con código de respuesta **101 Switching Protocols**.
   - En la subpestaña **Messages / Mensajes** podrás ver los frames STOMP que viajan en ambas direcciones (`CONNECT`, `CONNECTED`, `SUBSCRIBE`, `SEND`, `MESSAGE`) sobre la misma conexión TCP persistente sin generar nuevas peticiones HTTP.

---

## 📋 5. Respuestas a las Preguntas Teóricas

1. **¿Por qué un chat con HTTP normal tendría que estar preguntándole al servidor cada segundo, y qué cambia con WebSocket?**
   - En HTTP clásico, el protocolo es unidireccional (el cliente siempre debe iniciar la petición). Para enterarse de nuevos mensajes, el cliente debe hacer *polling* constante (peticiones GET periódicas), lo cual satura la red y genera cabeceras repetitivas. Con WebSocket, tras el handshake inicial, se mantiene un socket TCP bidireccional abierto; cuando alguien envía un mensaje, el servidor lo empuja inmediatamente (*push*) a todos los clientes suscritos.

2. **¿Por qué las imágenes y los audios se suben por HTTP y no viajan dentro del WebSocket?**
   - Los WebSockets están diseñados para el intercambio rápido de tramas pequeñas de texto o control. Transmitir archivos binarios pesados o cadenas base64 gigantes por el canal del WebSocket puede bloquear el event loop del broker, causar lag a otros usuarios conectados y aumentar drásticamente el consumo de memoria. Por tanto, se usa HTTP multipart para transferir el archivo al servidor y por WebSocket solo viaja la URL liviana resultante.

3. **Si el servidor se reinicia, ¿qué pasa con los usuarios conectados y qué hace reconnectDelay?**
   - Al apagarse el servidor, los sockets TCP se cierran y los clientes quedan desconectados. Gracias a la configuración `reconnectDelay: 3000` de `@stomp/stompjs`, el cliente intenta reabrir el WebSocket automáticamente cada 3 segundos hasta que el servidor vuelva a estar en línea, restaurando las suscripciones sin necesidad de refrescar el navegador.
