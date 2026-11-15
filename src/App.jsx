import { useEffect, useRef, useState } from "react";
import { Client } from "@stomp/stompjs";
import EmojiPicker from "emoji-picker-react";

export const SERVER = "http://localhost:8080";
const WS_URL = "ws://localhost:8080/ws";

export default function App() {
  const [usuario, setUsuario] = useState("");
  const [avatar, setAvatar] = useState("🚀");
  const [conectado, setConectado] = useState(false);
  const [mensajes, setMensajes] = useState([]);
  const [texto, setTexto] = useState("");
  const [verEmojis, setVerEmojis] = useState(false);
  const [escribiendo, setEscribiendo] = useState("");
  const [grabando, setGrabando] = useState(false);
  const [subiendoArchivo, setSubiendoArchivo] = useState(false);

  const clientRef = useRef(null);
  const finRef = useRef(null);
  const timerEscribiendo = useRef(null);
  const grabadorRef = useRef(null);
  const archivoInputRef = useRef(null);

  const avatares = ["🚀", "👨‍🚀", "👩‍🚀", "🛸", "🛰️", "👾", "⚡", "🤖"];

  function conectar(e) {
    if (e) e.preventDefault();
    const nombreLimpio = usuario.trim();
    if (!nombreLimpio) return;

    const nombreConAvatar = `${avatar} ${nombreLimpio}`;

    const client = new Client({
      brokerURL: WS_URL,
      reconnectDelay: 3000,
      debug: (str) => {
        // Log interno STOMP para trazabilidad
        console.log("[STOMP Frame]", str);
      },
      onConnect: () => {
        setConectado(true);

        // Suscripción a mensajes de la sala
        client.subscribe("/topic/sala", (frame) => {
          try {
            const nuevoMensaje = JSON.parse(frame.body);
            setMensajes((prev) => [...prev, nuevoMensaje]);
          } catch (err) {
            console.error("Error parseando frame:", err);
          }
        });

        // Suscripción a indicador "está escribiendo..."
        client.subscribe("/topic/escribiendo", (frame) => {
          const autorEscribiendo = frame.body;
          if (autorEscribiendo && autorEscribiendo !== nombreConAvatar) {
            setEscribiendo(autorEscribiendo);
            if (timerEscribiendo.current) clearTimeout(timerEscribiendo.current);
            timerEscribiendo.current = setTimeout(() => setEscribiendo(""), 2000);
          }
        });

        // Notificar entrada al chat
        client.publish({
          destination: "/app/chat.unirse",
          body: JSON.stringify({ tipo: "UNION", autor: nombreConAvatar }),
        });
      },
      onDisconnect: () => {
        setConectado(false);
      },
      onWebSocketClose: () => {
        setConectado(false);
      },
      onStompError: (frame) => {
        console.error("Broker STOMP error:", frame.headers["message"]);
      },
    });

    client.activate();
    clientRef.current = client;
    setUsuario(nombreConAvatar);
  }

  function desconectar() {
    if (clientRef.current) {
      clientRef.current.deactivate();
      setConectado(false);
      setMensajes([]);
    }
  }

  function enviar(tipo, contenido) {
    if (!clientRef.current || !clientRef.current.connected) return;
    clientRef.current.publish({
      destination: "/app/chat.enviar",
      body: JSON.stringify({ tipo, autor: usuario, contenido }),
    });
  }

  function notificarEscritura() {
    if (clientRef.current && clientRef.current.connected) {
      clientRef.current.publish({
        destination: "/app/chat.escribiendo",
        body: usuario,
      });
    }
  }

  function enviarTexto(e) {
    e.preventDefault();
    if (!texto.trim()) return;
    enviar("TEXTO", texto.trim());
    setTexto("");
    setVerEmojis(false);
  }

  async function subirArchivo(archivo) {
    setSubiendoArchivo(true);
    try {
      const datos = new FormData();
      datos.append("archivo", archivo);
      const res = await fetch(`${SERVER}/api/archivos`, {
        method: "POST",
        body: datos,
      });
      if (!res.ok) throw new Error("Error en servidor al subir archivo");
      const respuesta = await res.json();
      return respuesta.url;
    } catch (err) {
      alert("Error subiendo archivo: " + err.message);
      return null;
    } finally {
      setSubiendoArchivo(false);
    }
  }

  async function manejarSeleccionImagen(e) {
    const archivo = e.target.files[0];
    if (!archivo) return;
    const url = await subirArchivo(archivo);
    if (url) {
      enviar("IMAGEN", url);
    }
    e.target.value = "";
  }

  async function iniciarGrabacionAudio() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const grabador = new MediaRecorder(stream);
      const fragmentos = [];

      grabador.ondataavailable = (ev) => fragmentos.push(ev.data);
      grabador.onstop = async () => {
        stream.getTracks().forEach((pista) => pista.stop());
        const blobAudio = new Blob(fragmentos, { type: grabador.mimeType });
        const extension = grabador.mimeType.includes("mp4") ? "mp4" : "webm";
        const archivoAudio = new File([blobAudio], `transmision_${Date.now()}.${extension}`, {
          type: grabador.mimeType,
        });
        const urlAudio = await subirArchivo(archivoAudio);
        if (urlAudio) {
          enviar("AUDIO", urlAudio);
        }
      };

      grabador.start();
      grabadorRef.current = grabador;
      setGrabando(true);
    } catch (err) {
      alert("No se pudo acceder al micrófono: " + err.message);
    }
  }

  function detenerGrabacionAudio() {
    if (grabadorRef.current && grabando) {
      grabadorRef.current.stop();
      setGrabando(false);
    }
  }

  useEffect(() => {
    return () => {
      if (clientRef.current) clientRef.current.deactivate();
    };
  }, []);

  useEffect(() => {
    finRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [mensajes, escribiendo]);

  // Pantalla de Login Orbital
  if (!conectado) {
    return (
      <div className="login-pantalla">
        <div className="login-tarjeta">
          <div className="icono-estacion">🛰️</div>
          <span className="subtitulo-orbital">DOSW ORBITAL TELEMETRY</span>
          <h1>Estación Espacial</h1>
          <p className="descripcion">
            Canal de transmisión en tiempo real sobre WebSockets puros y STOMP. Conéctate a la sala de mando.
          </p>

          <form onSubmit={conectar}>
            <label className="etiqueta">Selecciona tu insignia de tripulante:</label>
            <div className="avatar-selector">
              {avatares.map((av) => (
                <button
                  type="button"
                  key={av}
                  className={`avatar-btn ${avatar === av ? "activo" : ""}`}
                  onClick={() => setAvatar(av)}
                >
                  {av}
                </button>
              ))}
            </div>

            <div className="input-grupo">
              <span className="input-avatar">{avatar}</span>
              <input
                type="text"
                value={usuario}
                onChange={(e) => setUsuario(e.target.value)}
                placeholder="Identificador / Callsign (ej. Orión)"
                autoFocus
                required
              />
            </div>

            <button type="submit" className="btn-conectar">
              Iniciar Enlace Cuántico ⚡
            </button>
          </form>

          <div className="login-footer">
            <span>● Protocolo: <b>RFC 6455 / STOMP 1.2</b></span>
            <span>● Servidor: <b>Spring Boot 3.4.x</b></span>
          </div>
        </div>
      </div>
    );
  }

  // Pantalla de Chat Principal
  return (
    <div className="chat-app">
      {/* Barra superior de la Estación Espacial */}
      <header className="estacion-header">
        <div className="header-info">
          <div className="estacion-logo">🚀</div>
          <div>
            <div className="estacion-titulo">
              ESTACIÓN ORBITAL <b>DOSW-15</b>
            </div>
            <div className="estacion-sub">Canal Cuántico: <code>/topic/sala</code></div>
          </div>
        </div>

        <div className="header-estado">
          <span className="badge-online">
            <span className="punto-verde"></span> ENLACE ACTIVO (101 SWITCHING)
          </span>
          <span className="usuario-badge">{usuario}</span>
          <button className="btn-desconectar" onClick={desconectar} title="Cerrar conexión">
            Desconectar ⏏
          </button>
        </div>
      </header>

      {/* Área central de Mensajes */}
      <main className="mensajes-contenedor">
        <div className="bienvenida-banner">
          <span>📡 Canales bidireccionales sincronizados. Bienvenido a la sala de transmisiones.</span>
        </div>

        <ul className="mensajes-lista">
          {mensajes.map((m, i) => {
            const esMio = m.autor === usuario;
            const esSistema = m.tipo === "UNION" || m.tipo === "SALIDA";

            if (esSistema) {
              return (
                <li key={i} className={`msg-sistema ${m.tipo === "UNION" ? "union" : "salida"}`}>
                  <span className="sistema-icono">{m.tipo === "UNION" ? "⚡" : "🚪"}</span>
                  <span className="sistema-texto">{m.contenido}</span>
                  <span className="sistema-hora">{m.fecha}</span>
                </li>
              );
            }

            return (
              <li key={i} className={`msg-fila ${esMio ? "fila-mio" : "fila-otro"}`}>
                <div className="burbuja-msg">
                  <div className="burbuja-cabecera">
                    <span className="autor-nombre">{m.autor}</span>
                    <span className="autor-hora">{m.fecha}</span>
                  </div>

                  <div className="burbuja-contenido">
                    {m.tipo === "TEXTO" && <p className="texto-mensaje">{m.contenido}</p>}

                    {m.tipo === "IMAGEN" && (
                      <div className="imagen-wrapper">
                        <img
                          src={m.contenido.startsWith("http") ? m.contenido : `${SERVER}${m.contenido}`}
                          alt="Transmisión visual"
                          className="imagen-mensaje"
                          onClick={() => window.open(m.contenido.startsWith("http") ? m.contenido : `${SERVER}${m.contenido}`, "_blank")}
                        />
                        <span className="imagen-pie">Transmisión visual satelital (clic para ampliar)</span>
                      </div>
                    )}

                    {m.tipo === "AUDIO" && (
                      <div className="audio-wrapper">
                        <span className="audio-icono">🎙️ Registro de voz orbital:</span>
                        <audio
                          controls
                          src={m.contenido.startsWith("http") ? m.contenido : `${SERVER}${m.contenido}`}
                          className="audio-player"
                        />
                      </div>
                    )}
                  </div>
                </div>
              </li>
            );
          })}

          {/* Indicador de "está escribiendo..." */}
          {escribiendo && (
            <li className="escribiendo-alerta">
              <span className="animacion-puntos">
                <i></i><i></i><i></i>
              </span>
              <span><b>{escribiendo}</b> está transmitiendo telemetría...</span>
            </li>
          )}

          <li ref={finRef} />
        </ul>
      </main>

      {/* Barra de control y envío */}
      <footer className="estacion-footer">
        {/* Selector de Emojis flotante */}
        {verEmojis && (
          <div className="emoji-picker-contenedor">
            <EmojiPicker
              theme="dark"
              searchPlaceHolder="Buscar emoji espacial..."
              onEmojiClick={(emojiData) => {
                setTexto((prev) => prev + emojiData.emoji);
              }}
            />
          </div>
        )}

        {/* Input invisible de archivo */}
        <input
          type="file"
          accept="image/*"
          ref={archivoInputRef}
          style={{ display: "none" }}
          onChange={manejarSeleccionImagen}
        />

        <form onSubmit={enviarTexto} className="barra-formulario">
          <div className="barra-botones-extra">
            <button
              type="button"
              className={`btn-herramienta ${verEmojis ? "activo" : ""}`}
              onClick={() => setVerEmojis(!verEmojis)}
              title="Abrir selector de emojis"
            >
              😄
            </button>

            <button
              type="button"
              className="btn-herramienta"
              onClick={() => archivoInputRef.current?.click()}
              disabled={subiendoArchivo}
              title="Enviar imagen espacial"
            >
              {subiendoArchivo ? "⏳" : "🖼️"}
            </button>

            <button
              type="button"
              className={`btn-herramienta ${grabando ? "grabando" : ""}`}
              onClick={grabando ? detenerGrabacionAudio : iniciarGrabacionAudio}
              title={grabando ? "Detener transmisión de voz" : "Grabar registro de voz"}
            >
              {grabando ? "⏹️" : "🎙️"}
            </button>
          </div>

          <input
            type="text"
            className="input-mensaje"
            value={texto}
            onChange={(e) => {
              setTexto(e.target.value);
              notificarEscritura();
            }}
            placeholder="Escribe un mensaje para la tripulación orbital..."
            autoFocus
          />

          <button type="submit" className="btn-enviar" disabled={!texto.trim()}>
            Transmitir 🚀
          </button>
        </form>
      </footer>
    </div>
  );
}

