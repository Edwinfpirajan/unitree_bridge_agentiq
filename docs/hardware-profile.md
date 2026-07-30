# Perfil del hardware (obligatorio antes de modo real)

| Campo | Valor |
|---|---|
| Modelo comercial exacto | Unitree G1 EDU+ |
| Variante / revisión U2 | Denominación local U2; significado comercial pendiente |
| Número de serie | CONFIRMADO (conservar fuera de Git) |
| 23 o 29 DOF | 29 DOF |
| Tipo de manos | Manos fijas/no articuladas; monitoreo de efector final desactivado |
| Computador interno / GPU | PC2 ARM64 confirmado; modelo de GPU pendiente |
| Software del robot | V1.5.4 |
| Hardware | V1.0 |
| Fecha de verificación | 2026-07-29 |
| SDK suministrado / tag | `unitree_sdk2_python` instalado en PC2; commit/tag pendiente |
| IP del robot | PC1 `192.168.123.161`, PC2 `192.168.123.164` en la prueba validada |
| Interfaz Ethernet del PC | Ethernet Windows `192.168.123.99/24` en la prueba validada |
| ROS 2 / DDS confirmado | CycloneDDS 0.10.2 confirmado en PC2; ROS 2 pendiente |
| Mando y E-stop probados | PENDIENTE |
| Soporte de suspensión | PENDIENTE |

Guardar secretos, IP y serie en `config/robot.toml` o inventario privado, nunca en Git.

Fuente de los campos confirmados: pantalla local “About Robot” y confirmación del propietario.
La captura contiene datos identificadores y no debe incorporarse al repositorio.

## Red observada

- `wlan0`: conectada a una LAN privada `192.168.1.0/24`.
- `wlan1`: dirección link-local `169.254.0.0/16`; no demuestra acceso a la red DDS.
- Modos AP y Wi‑Fi disponibles.
- La pantalla `Network` mostró inicialmente la conexión remota deshabilitada.
- Posteriormente el propietario habilitó manualmente la conexión remota y el permiso OTA para la
  revisión. Deben volver a deshabilitarse al terminar, antes de usar la red de desarrollo.
- Interfaz Ethernet de desarrollo y direcciones PC1/PC2 verificadas para audio. La topología DDS
  necesaria para control de movimiento todavía debe documentarse y aprobarse por separado.
- El compartimento posterior contiene conectores RJ45; uno está ocupado por cableado interno y
  otro aparece libre. Usar únicamente el RJ45 libre para la prueba de desarrollo, sin desconectar
  cables internos ni tocar los conectores de alimentación `BAT`, `24V` y `12V`.

Las direcciones concretas son dinámicas o privadas y deben permanecer en `config/robot.toml`, no
en este archivo versionado.

## Periféricos observados

- Mando remoto Unitree vinculado por Bluetooth; su identificador se considera privado y no se
  guarda.
- La app ofrece prueba funcional y visualización de botones del mando; la prueba física de todos
  los controles sigue pendiente.
- Efector final seleccionado: `Turn Off`. Las opciones Dex2/5 y Dex1-1 aparecen disponibles en la
  app, pero no están seleccionadas.

## Batería observada

- Software del BMS: 1.6.
- Contador mostrado: 7 ciclos.
- Estado al capturar: descarga, 68 %, aproximadamente 49.0 V.
- Temperaturas observadas: MOS 27 °C, BAT1 23 °C y RES 22 °C.

Porcentaje, voltaje, estado y temperaturas son telemetría temporal; no describen límites seguros.
Usar los umbrales oficiales del fabricante cuando estén disponibles.
