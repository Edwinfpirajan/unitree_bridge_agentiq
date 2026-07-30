# Conexión del G1, audio y reanudación

Última actualización: 29 de julio de 2026.

Este documento registra el estado validado del G1 EDU+ llamado **Migo** antes de cambiar la
batería. No contiene contraseñas, claves privadas ni la API key de ElevenLabs.

## Estado alcanzado

- El computador de desarrollo usa Windows y WSL `Ubuntu-24.04`.
- El G1 está conectado al computador mediante cable Ethernet.
- La interfaz Ethernet de Windows utilizó `192.168.123.99/24`.
- PC1 respondió en `192.168.123.161`.
- PC2 respondió en `192.168.123.164`.
- Se validó SSH a PC2 con el usuario `unitree` y una clave dedicada.
- PC2 ejecuta Ubuntu 20.04.6 LTS sobre ARM64.
- En PC2 están instalados CycloneDDS 0.10.2 y `unitree_sdk2_python`.
- El servicio oficial de audio SDK2 respondió correctamente.
- El volumen reportado y configurado en el G1 es `100`.
- El G1 reprodujo físicamente: `Hola, soy Migo. Mi sistema de voz está listo.`
- ElevenLabs genera correctamente PCM mono, 16 bits, 16 kHz.
- El puente de conversación en tiempo real ya está implementado: micrófono predeterminado de
  Windows, ElevenLabs y altavoz del G1 mediante una conexión SSH persistente.
- El puente fue validado con `G1_LIVE_AUDIO_READY`. Falta crear el agente porque la API key no
  tiene actualmente el permiso `convai_write`.

La configuración principal continúa deliberadamente en modo seguro:

```toml
mode = "mock"
hardware_enabled = false
```

El audio no habilita ni invoca APIs de movimiento.

## Identidades y archivos

La clave SSH privada permanece únicamente en Windows:

```text
C:\Users\hp\.ssh\migo_g1_ed25519
```

La clave pública correspondiente fue añadida a `/home/unitree/.ssh/authorized_keys`.

Archivos instalados o utilizados en PC2:

```text
/home/unitree/cyclonedds_ws/install/cyclonedds
/home/unitree/migo-audio-src/unitree_sdk2_python
/home/unitree/g1_audio_probe.py
/home/unitree/g1_audio_play_pcm.py
/home/unitree/migo-test.pcm
```

Los secretos de ElevenLabs permanecen en el archivo local `.env`. Nunca copiar `.env` al robot,
mostrar su contenido en una terminal compartida ni agregarlo a Git.

## Apagado antes de cambiar la batería

1. Detener cualquier conversación, reproducción o proceso de prueba con `Ctrl+C`.
2. Asegurar físicamente el robot según el manual de Unitree. No cambiar la batería durante una
   orden de movimiento o una actualización.
3. En la sesión SSH de PC2 ejecutar:

   ```bash
   sudo poweroff
   ```

4. Esperar a que PC2 termine de apagarse y a que cesen sus indicadores de actividad.
5. Cerrar la sesión SSH si la terminal no se cerró automáticamente.
6. Cambiar la batería siguiendo el procedimiento mecánico y eléctrico oficial de Unitree.

No retirar la batería mientras Linux esté escribiendo datos. Este repositorio no sustituye las
instrucciones físicas del fabricante.

## Reconexión después del cambio

Conectar nuevamente el Ethernet, encender el G1 y esperar a que PC2 termine de iniciar. Desde
PowerShell:

```powershell
ping 192.168.123.164
ssh.exe -i C:\Users\hp\.ssh\migo_g1_ed25519 unitree@192.168.123.164
```

La conexión correcta debe abrir un prompt similar a `unitree@ubuntu:~$`. No debería pedir la
contraseña si la clave pública sigue instalada. Si la IP no responde, comprobar primero que el
adaptador Ethernet de Windows conserve una dirección `192.168.123.x/24`.

## Verificación de audio sin generar voz nueva

En PC2, comprobar primero el volumen:

```bash
python3 /home/unitree/g1_audio_probe.py eth0
```

Resultado validado previamente:

```text
GetVolume=(0, {'volume': 100})
```

Después, y solo si se desea producir sonido físico, reproducir el PCM existente:

```bash
python3 /home/unitree/g1_audio_play_pcm.py \
  eth0 /home/unitree/migo-test.pcm \
  --volume 100 --confirm-g1-audio
```

Resultado esperado: `G1_AUDIO_PLAYBACK_OK`.

El reproductor debe esperar después de cada fragmento, incluido el último, antes de llamar
`PlayStop`. Sin esa espera el servicio acepta el audio, pero puede detenerlo antes de escucharlo.

## Arquitectura validada para tiempo real

El diseño acordado mantiene las credenciales fuera del robot:

```text
Micrófono del PC
  -> ElevenLabs Conversational AI
  -> audio PCM 16 kHz
  -> conexión Ethernet/SSH persistente
  -> SDK2 AudioClient.PlayStream en PC2
  -> altavoz del G1
```

Estado validado y trabajo que falta:

1. La identidad local es `Migo`.
2. Python 3.12, ElevenLabs y PyAudio fueron validados en `.venv-win`; un clon nuevo debe recrear
   ese entorno siguiendo [voice.md](voice.md).
3. La interfaz captura el micrófono predeterminado de Windows a 16 kHz.
4. El canal persistente hacia PC2 ya está implementado y validado.
5. Habilitar `convai_write` en la API key o crear un agente en el panel y copiar su Agent ID.
6. Crear/configurar el agente ejecutando `python scripts/provision_migo_agent.py` si todavía no
   existe.
7. Ejecutar `scripts/start_migo_live.ps1`; el transporte, la reproducción y `Ctrl+C` ya fueron
   validados. Las mediciones formales de interrupciones y latencia siguen pendientes.
8. Investigar después el micrófono interno del G1. Por ahora no se ha identificado una entrada
   física inequívoca entre los dispositivos APE/ADMAIF de PC2.

La API key y el Voice ID están configurados localmente. El Agent ID sigue vacío. No copiar
ninguna credencial a PC2.

## Diagnóstico rápido

- `Permission denied`: confirmar que se usa `-i` con la clave dedicada y el usuario `unitree`.
- No responde el ping: revisar batería, arranque, cable, adaptador Ethernet e IP de Windows.
- `GetVolume` funciona pero no se oye: verificar PCM 16 kHz mono de 16 bits y esperar el consumo
  del último fragmento antes de `PlayStop`.
- Se oye muy bajo: consultar `GetVolume`; el último valor validado fue 100.
- ElevenLabs funciona pero el robot no habla: separar el diagnóstico entre generación PCM,
  transporte a PC2 y reproducción SDK2.
