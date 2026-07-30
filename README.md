# G1 Edu U2

Base segura y reproducible para desarrollar con un Unitree G1 EDU+. El proyecto empieza en modo
`mock`; ningún módulo incluido envía órdenes de movimiento al robot real hasta implementar y
habilitar explícitamente el adaptador de Unitree. La integración de audio sí fue validada con el
micrófono del PC y el altavoz del G1, sin habilitar movimiento.

## Migracion a AgentIQ

Este repositorio conserva la validacion de hardware y el prototipo directo de
ElevenLabs. El runtime productivo para conversaciones es ahora AgentIQ Device
Bridge; no se deben ejecutar ambos procesos al mismo tiempo.

En el PC conectado al robot, actualizar este repositorio y pedirle a Codex:

```text
Lee docs/agentiq-device-bridge-handoff.md completo. Ejecuta el empalme por
fases, sin borrar este repositorio, sin mostrar secretos y sin habilitar
movimientos. Detente solamente si necesitas que yo introduzca el PIN o una
password en la terminal.
```

El procedimiento completo, los preflight de WSL/Ubuntu, Ethernet, SSH, SDK2,
audio USB, pairing y criterios de aceptacion estan en
[docs/agentiq-device-bridge-handoff.md](docs/agentiq-device-bridge-handoff.md).

## Inicio rápido

Requisitos de desarrollo: Python 3.11+ y Git. Ubuntu 22.04 es el entorno recomendado para ROS 2
Humble; en Windows se puede ejecutar el modo `mock` y el puente de conversación. El SDK/DDS real
se ejecuta en Linux o en PC2.

```bash
git clone https://github.com/Edwinfpirajan/unitree_bridge_agentiq.git
cd unitree_bridge_agentiq
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
cp config/robot.example.toml config/robot.toml
g1ctl --config config/robot.toml doctor
g1ctl --config config/robot.toml status
python -m unittest discover -s tests
```

No cambie `mode = "mock"` durante la primera puesta en marcha. Siga
[docs/bringup.md](docs/bringup.md) con el robot suspendido en su soporte y el paro de emergencia
accesible.

## Mapa

- `src/g1edu`: núcleo, contratos, seguridad, CLI y adaptadores.
- `config`: configuración versionada sin secretos.
- `tests`: verificaciones que no necesitan hardware.
- `docs`: arquitectura, seguridad, puesta en marcha y decisiones pendientes.
- `skills`: procedimientos reutilizables para operar este repositorio con Codex.
- `personality`: identidad conversacional separada de los permisos físicos.

La integración opcional de ElevenLabs se explica en [docs/voice.md](docs/voice.md).

## Conversación validada en Windows

El 29 de julio de 2026 se validó este recorrido completo:

```text
micrófono predeterminado del PC
  -> ElevenLabs Conversational AI
  -> PCM mono de 16 bits a 16 kHz
  -> SSH persistente por Ethernet
  -> SDK2 AudioClient.PlayStream en PC2
  -> altavoz del G1
```

La instalación desde cero y el arranque se describen en [docs/voice.md](docs/voice.md). El puente
solo transporta audio: no importa ni invoca APIs de movimiento.

## Cambio de batería y reanudación

El procedimiento para apagar, cambiar la batería y retomar la conexión, junto con el estado
validado de Ethernet, SSH, SDK2, audio y ElevenLabs, está documentado en
[docs/connection-and-resume.md](docs/connection-and-resume.md).

## Estado actual

La arquitectura, el modo simulado y el puente de conversación están listos. El equipo está
identificado como G1 EDU+ de 29 DOF, con manos fijas, software V1.5.4 y hardware V1.0. Ethernet,
SSH a PC2, CycloneDDS 0.10.2, `unitree_sdk2_python` y el servicio oficial de audio fueron
verificados. El adaptador de movimiento físico permanece bloqueado hasta fijar formalmente el SDK
compatible y completar las puertas de seguridad.
