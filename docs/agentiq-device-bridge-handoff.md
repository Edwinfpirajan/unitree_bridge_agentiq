# Handoff para instalar AgentIQ en el PC conectado al Unitree G1

Fecha de referencia: 2026-07-30

Este documento esta escrito para que Codex pueda continuar el trabajo desde el
PC Windows que ya se uso para hacer hablar al Unitree G1 por Ethernet con un
prototipo directo de ElevenLabs.

URL publica de este handoff:

```text
https://app.agentiq.com.co/robotics/unitree-pilot-handoff.md
```

## 1. Instruccion para Codex

Codex debe leer este archivo completo antes de ejecutar comandos.

Objetivo:

1. conservar el prototipo anterior como respaldo de diagnostico;
2. detener cualquier proceso viejo que use ElevenLabs, microfono o parlante;
3. validar WSL/Ubuntu, red, SSH, Unitree SDK2 y audio;
4. instalar `AgentIQ Device Bridge` mediante el PIN generado en AgentIQ;
5. comprobar conversacion de voz sin habilitar movimientos;
6. entregar un reporte de aceptacion o un diagnostico concreto.

Restricciones:

- No borrar ni reescribir el repositorio anterior.
- No ejecutar el prototipo anterior al mismo tiempo que Device Bridge.
- No copiar secretos desde archivos `.env`.
- No imprimir, registrar ni pedir en el chat el PIN, la API key de AgentIQ, la
  API key de ElevenLabs o la password Linux del Unitree.
- El usuario introduce PIN y passwords directamente en la terminal interactiva.
- No instalar, importar ni invocar APIs de movimiento.
- No modificar AgentIQ cloud desde este PC.
- No inventar IPs, usuarios, interfaces o dispositivos. Validar primero.

## 2. Arquitectura vigente

El repositorio antiguo `unitree_bridge_agentiq` fue un prototipo local y ya no
es el runtime de produccion.

El flujo vigente es:

```text
Microfono PC/USB
  -> AgentIQ STT
  -> agente configurado en AgentIQ
  -> tools/CRM permitidos para ese agente
  -> AgentIQ TTS
  -> Device Bridge en Ubuntu
  -> SSH por Ethernet
  -> Unitree PC2 + SDK2 AudioClient.PlayStream
  -> parlante del G1
```

Configuracion central en AgentIQ:

- identidad e instrucciones;
- proveedor y modelo;
- idioma, voz y credencial de voz;
- CRM, acciones y permisos;
- palabra de activacion, frases de cierre y timeout;
- anuncios de conexion.

Configuracion local:

- red e IP del robot;
- usuario SSH;
- interfaz DDS;
- microfono;
- clave de dispositivo revocable generada por pairing.

El robot nunca recibe la API key de ElevenLabs.

## 3. Estado esperado del PC

Topologia validada por defecto:

| Elemento | Valor |
|---|---|
| Sistema del bridge | Ubuntu o WSL Ubuntu con systemd |
| Internet | Wi-Fi u otra interfaz |
| Conexion al robot | Ethernet |
| Unitree PC2 | `192.168.123.164` |
| Usuario PC2 | `unitree` |
| Interfaz DDS en PC2 | `eth0` |
| Entrada de audio | Microfono del PC o USB |
| Salida de audio | Parlante del G1 por SDK2 |

La IP, el usuario y la interfaz son defaults, no suposiciones obligatorias. Si
el robot real usa otros valores, se deben pasar al instalador con sus flags.

## 4. Fase A: inventario sin cambios

Desde PowerShell:

```powershell
wsl --status
wsl -l -v
```

Abrir Ubuntu y ejecutar:

```bash
uname -a
python3 --version
systemctl is-system-running || true
ip -br address
ip route
```

Si aparece `System has not been booted with systemd`, configurar WSL:

```bash
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```

Cerrar Ubuntu y ejecutar desde PowerShell:

```powershell
wsl --shutdown
```

Volver a abrir Ubuntu y confirmar:

```bash
systemctl is-system-running || true
```

Los estados `running` o `degraded` permiten continuar. Si systemd sigue sin
estar disponible, detener el proceso y diagnosticar WSL antes de instalar.

## 5. Fase B: detener el prototipo anterior

Cerrar la terminal donde se ejecutaba el agente directo de ElevenLabs. Buscar
procesos relacionados sin revelar variables de entorno:

```powershell
Get-Process python,python3 -ErrorAction SilentlyContinue |
  Select-Object Id,ProcessName,Path
```

Desde Ubuntu:

```bash
pgrep -af 'python|g1|unitree|elevenlabs' || true
```

Codex debe mostrar los procesos encontrados y confirmar su identidad antes de
detenerlos. No terminar procesos desconocidos.

El repositorio viejo se conserva. No se usa para arrancar la conversacion nueva.

## 6. Fase C: preflight de conectividad

Validar la distribucion publica y la API:

```bash
curl -fsSI https://app.agentiq.com.co/robotics/install.sh
curl -fsSI https://app.agentiq.com.co/robotics/agentiq-device-bridge.tar.gz
curl -sS -o /dev/null -w '%{http_code}\n' \
  https://api.agentiq.com.co/api/v1/robotics/configuration
```

Resultados esperados:

- los dos artefactos responden `200`;
- Robotics configuration responde `401` sin credencial, lo cual confirma que
  la ruta existe y esta protegida.

Validar SSH:

```bash
timeout 5 bash -c '</dev/tcp/192.168.123.164/22' && echo UNITREE_SSH_OK
ssh unitree@192.168.123.164
```

Ya dentro de PC2:

```bash
source /home/unitree/cyclonedds_ws/install/setup.bash
python3 -c 'import unitree_sdk2py; print("UNITREE_SDK_OK")'
exit
```

No continuar si falta `unitree_sdk2py` o el setup de CycloneDDS. Esa
dependencia vive en PC2 y no pertenece al prototipo AgentIQ anterior.

Listar audio local si `alsa-utils` ya esta instalado:

```bash
arecord -l || true
arecord -L || true
```

Si esos comandos no existen, el instalador agregara `alsa-utils`.

## 7. Fase D: configuracion en AgentIQ

Esta fase la realiza el usuario en el navegador:

1. Abrir el agente correcto.
2. Entrar a `Voz`.
3. Seleccionar idioma, proveedor y voz.
4. Seleccionar credencial de AgentIQ o API propia de la organizacion.
5. Guardar cambios.
6. Entrar a `Canales > Robotics`.
7. Seleccionar `Unitree G1`.
8. Configurar palabra de activacion, frases de cierre y timeout.
9. Mantener activos los anuncios de conexion para el primer piloto.
10. Generar el pairing.

El pairing entrega un PIN de cuatro digitos y un comando con UUID. El PIN dura
cinco minutos y se consume una sola vez.

No crear una Agent API key manual para Robotics. El pairing crea una key
limitada al agente, dispositivo y canal, y el instalador la guarda con permisos
restringidos.

## 8. Fase E: instalacion

El usuario debe copiar exactamente el comando mostrado por AgentIQ. Tiene esta
forma:

```bash
curl -fsSL "https://app.agentiq.com.co/robotics/install.sh" \
  | sudo bash -s -- \
  --server "https://api.agentiq.com.co" \
  --pairing-id "UUID_GENERADO_POR_AGENTIQ" \
  --profile "unitree-g1"
```

Durante la instalacion:

1. introducir el PIN de AgentIQ directamente en la terminal;
2. introducir la password de `unitree` cuando `ssh-copy-id` la solicite;
3. no pegar ninguna de esas credenciales en Codex;
4. esperar a que finalice `doctor` y se reinicie el servicio.

El instalador:

- instala dependencias Ubuntu;
- descarga el runtime publico de AgentIQ;
- crea el usuario local `agentiq`;
- consume el pairing y guarda la key en
  `/etc/agentiq-device-bridge.env`;
- crea una clave SSH exclusiva;
- autoriza la clave en PC2;
- copia el helper de audio;
- instala y arranca `agentiq-device-bridge.service`.

Si el PIN expira o se consume durante una instalacion fallida, generar un
pairing nuevo. Nunca reutilizar un PIN.

## 9. Fase F: verificacion

```bash
sudo systemctl status agentiq-device-bridge --no-pager
sudo journalctl -u agentiq-device-bridge -n 100 --no-pager
```

Ejecutar el doctor manualmente si es necesario:

```bash
sudo -u agentiq bash -lc '
  set -a
  source /etc/agentiq-device-bridge.env
  set +a
  exec /opt/agentiq-device-bridge/.venv/bin/agentiq-device-bridge doctor
'
```

Para logs en vivo:

```bash
sudo journalctl -u agentiq-device-bridge -f
```

Resultados esperados:

1. servicio `active (running)`;
2. dispositivo conectado en AgentIQ;
3. el G1 dice `Conectando a AgentIQ`;
4. el G1 dice `Conectado a AgentIQ`;
5. el bridge escucha el microfono local;
6. AgentIQ transcribe, responde y reproduce por el parlante del G1.

## 10. Microfono USB

El perfil Unitree debe conservar:

```env
AGENTIQ_AUDIO_BACKEND=unitree-g1
```

Esto mantiene la salida por el parlante del robot. Para cambiar solo la entrada
de audio:

```bash
arecord -L
sudo nano /etc/agentiq-device-bridge.env
```

Ejemplo:

```env
AGENTIQ_AUDIO_BACKEND=unitree-g1
AGENTIQ_INPUT_DEVICE=plughw:CARD=USB,DEV=0
```

Reiniciar:

```bash
sudo systemctl restart agentiq-device-bridge
sudo journalctl -u agentiq-device-bridge -f
```

No cambiar el backend a `alsa` en el perfil G1: eso desviaria tambien la salida
desde el parlante Unitree hacia el audio local.

## 11. Diagnostico

### Pairing rechazado o expirado

Generar un pairing nuevo desde AgentIQ y ejecutar el nuevo comando. No intentar
recuperar ni mostrar la API key.

### `ssh-copy-id` falla

Validar:

```bash
ip route
timeout 5 bash -c '</dev/tcp/192.168.123.164/22'
ssh unitree@192.168.123.164
```

Confirmar IP, usuario y password con el responsable del robot.

### `ModuleNotFoundError: unitree_sdk2py`

El problema esta en el entorno Python de PC2. Verificar el SDK oficial y
CycloneDDS en PC2. No resolverlo ejecutando el prototipo de ElevenLabs.

### El microfono no abre

```bash
arecord -l
arecord -L
sudo journalctl -u agentiq-device-bridge -n 100 --no-pager
```

Seleccionar un `AGENTIQ_INPUT_DEVICE` valido y confirmar que el usuario
`agentiq` pertenece al grupo `audio`.

### El audio sale dos veces o el dispositivo esta ocupado

Confirmar que el proceso viejo de ElevenLabs no siga ejecutandose.

### El robot no habla pero el servicio esta activo

Buscar en logs errores de SSH, `PlayStream`, SDK2 o CycloneDDS. Confirmar que el
helper remoto existe:

```bash
ssh unitree@192.168.123.164 \
  'ls -l /home/unitree/agentiq_g1_audio_stream.py'
```

### Como compartir logs

Se pueden compartir:

- `systemctl status`;
- mensajes de `journalctl`;
- IPs locales del robot;
- nombres ALSA;
- versiones de Python, SDK y bridge.

No compartir:

- contenido de `/etc/agentiq-device-bridge.env`;
- PIN;
- API keys;
- passwords;
- headers `Authorization`.

## 12. Criterios de aceptacion

El piloto queda aceptado cuando:

- el servicio arranca automaticamente;
- AgentIQ muestra heartbeat reciente del dispositivo;
- el robot reproduce los dos anuncios;
- una persona inicia una sesion con la frase configurada;
- el agente escucha y responde por voz;
- una segunda sesion no hereda el contexto privado de la primera;
- CRM solo se ejecuta si el agente tiene esa capacidad habilitada;
- ningun movimiento se invoca;
- reiniciar Ubuntu recupera la conexion sin volver a introducir passwords.

## 13. Reporte que Codex debe entregar

Codex debe finalizar con:

```text
Sistema:
- Windows/WSL/Ubuntu:
- systemd:

Red:
- Internet:
- SSH PC2:
- IP PC2:
- Interfaz DDS:

Unitree:
- CycloneDDS:
- unitree_sdk2py:
- helper remoto:

Audio:
- microfono:
- salida G1:

AgentIQ:
- servicio:
- device heartbeat:
- anuncios:
- conversacion:

Resultado:
- APROBADO / BLOQUEADO
- Bloqueo exacto:
- Siguiente accion:
```
