# Voz y personalidad

## Alcance

La personalidad vive en `personality/g1-personality.md`; ElevenLabs sintetiza el texto final.
También puede generar archivos MP3 en el PC. La reproducción por el altavoz del G1 y la
conversación en vivo fueron validadas el 29 de julio de 2026 mediante el servicio oficial SDK2 de
audio.

Para conversación natural se usa ElevenAgents: micrófono, transcripción, LLM, turnos y TTS. El
primer ensayo utiliza los dispositivos de audio predeterminados del PC.

## Obtener credenciales

1. Crear una cuenta en ElevenLabs.
2. Crear una API key con el mínimo alcance necesario para texto a voz y lectura de voces.
3. Copiar `.env.example` como `.env`.
4. Guardar la clave en `ELEVENLABS_API_KEY`; no enviarla por chat ni guardarla en Git.
5. Añadir a la biblioteca la voz `David - Warm, Friendly and Warm`, variante
   latinoamericana, desde la sección española de ElevenLabs.
6. Ejecutar `g1ctl --config config/robot.toml voices --search David`.
7. Verificar nombre, descripción y acento; guardar su `voice_id` en
   `ELEVENLABS_VOICE_ID`.
8. Ejecutar `g1ctl --config config/robot.toml voice-info` para validar directamente el ID sin
   generar audio.

La disponibilidad por API depende del plan y de que la voz esté añadida a la biblioteca. No
copiar un ID encontrado en terceros.

## Permisos mínimos de la clave

- Mantener `Restringir clave` activado.
- Habilitar únicamente `De texto a voz`.
- Si existe un permiso separado de voces, habilitar solo lectura/listado de voces.
- Mantener sin acceso: voz a voz, voz a texto, efectos, clonación, diseño de voces, doblaje,
  proyectos, agentes y administración.
- En la sección avanzada seleccionar: `Audio nativo → Sin acceso`, `Voces → Leído`,
  `Generación de voz → Sin acceso`, `Alineación forzada → Sin acceso` y
  `Motor de anuncios → Sin acceso`.
- Fijar inicialmente un límite de 5 000 a 10 000 créditos por período, según el plan; aumentarlo
  únicamente después de medir el uso.
- No restringir por IP durante la prueba si la IP pública del laboratorio es dinámica. Considerar
  allowlist de IP al desplegar en una red con IP pública fija.

## Probar

```bash
g1ctl --config config/robot.toml speak "Hola. Soy Migo y mi sistema de voz está listo."
```

El comando guarda un MP3 en `audio-output/` y no controla ni mueve el robot.

## Conversación natural

1. En ElevenLabs abrir `Agents` y crear un agente con plantilla vacía.
2. Mantenerlo privado y nombrarlo `Migo G1`.
3. Establecer español como idioma principal.
4. Elegir `David - Warm, Friendly and Warm` como voz.
5. Copiar el contenido de `personality/g1-personality.md` al System Prompt.
6. Usar como primer mensaje: `Hola, soy Migo. ¿En qué puedo ayudarte?`
7. Copiar el Agent ID a `ELEVENLABS_AGENT_ID` en `.env`.
8. Instalar la dependencia opcional: `pip install -e ".[conversation]"`.
9. Ejecutar `g1ctl --config config/robot.toml converse`.

Finalizar con `Ctrl+C`. El comando no tiene herramientas ni permisos de movimiento del robot.

### Preparar Windows desde un clon limpio

Ejecutar desde PowerShell en la raíz del repositorio:

```powershell
py -3.12 -m venv .venv-win
.\.venv-win\Scripts\python.exe -m pip install --upgrade pip
.\.venv-win\Scripts\python.exe -m pip install -e ".[conversation]"
Copy-Item .env.example .env
Copy-Item config\robot.example.toml config\robot.toml
```

Completar `.env` con `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` y
`ELEVENLABS_AGENT_ID`. PyAudio puede requerir herramientas de compilación en algunas versiones de
Python; la combinación validada en este PC fue Python 3.12 con PyAudio instalado en `.venv-win`.

La conexión en vivo también requiere:

- OpenSSH Client de Windows y una clave autorizada en PC2.
- Ethernet del PC en la subred `192.168.123.0/24`.
- PC2 accesible por SSH y con CycloneDDS, SDK2 y `g1_audio_stream_stdin.py`.
- Ajustar los valores predeterminados de host, usuario, interfaz y clave en
  `G1LiveAudioInterface` si la instalación usa otros datos.

Después de completar estos requisitos:

```powershell
.\scripts\start_migo_live.ps1
```

Resultado validado: el micrófono predeterminado de este PC captura al usuario, ElevenLabs procesa
la conversación y el G1 reproduce la respuesta por su altavoz.

No enrutar audio al robot por métodos no documentados.

## Reproducir directamente en el G1

El adaptador usa exclusivamente el servicio oficial SDK2 `voice`. ElevenLabs entrega PCM mono de
16 bits a 16 kHz y el proyecto lo transmite por `AudioClient.PlayStream`.

Requisitos:

- Ejecutar en Ubuntu/PC2 con `unitree_sdk2_python` oficial instalado.
- Conectar la interfaz de red a la subred de desarrollo del G1.
- Verificar primero `AudioClient.GetVolume` con un ejemplo oficial de solo audio.

Prueba deliberada, a volumen moderado:

```bash
g1ctl --config config/robot.toml robot-speak \
  --interface eth0 \
  --volume 60 \
  --confirm-g1-audio \
  "Hola, soy Migo. Mi voz ya se reproduce desde el G1."
```

Sustituir `eth0` por la interfaz real. Este comando consume créditos TTS y produce sonido físico,
pero no importa ni invoca interfaces de movimiento.

## Modelos

- `eleven_multilingual_v2`: calidad y estabilidad para español.
- `eleven_flash_v2_5`: menor latencia para conversación interactiva.

Empezar con Multilingual v2; medir latencia y costo antes de cambiar a Flash.

## Límites

- No enviar secretos ni información privada como texto para sintetizar.
- Mantener frases cortas para controlar costo y latencia.
- No clonar voces sin consentimiento explícito de su propietario.
- Separar el permiso para hablar del permiso para ejecutar acciones físicas.
