# Política de seguridad

Un humanoide de tamaño completo puede caer, pellizcar, golpear o dañar el entorno. Estas reglas son
condiciones de operación, no sugerencias:

- Mantener área despejada, operador entrenado y paro de emergencia al alcance.
- Primera energía y primer control de articulaciones con soporte de suspensión.
- No trabajar solo durante pruebas de movimiento.
- No puentear límites de fábrica, protecciones, E-stop ni control remoto.
- Separar físicamente la red de desarrollo de redes públicas.
- Mantener deshabilitados el acceso remoto por Internet y OTA durante pruebas, salvo una ventana
  de mantenimiento planificada y supervisada.
- Ensayar primero en mock, después simulación y finalmente robot a velocidad reducida.
- Ejecutar un solo publicador de comandos y definir quién tiene autoridad de control.
- Detener ante telemetría vencida, pérdida de enlace, sobretemperatura, batería crítica o estado no esperado.
- No habilitar control de bajo nivel hasta conocer variante, mapa articular y firmware exactos.

## Puerta de promoción

`mock -> simulación -> robot suspendido -> robot en suelo, área controlada`.

Cada transición requiere evidencia de pruebas, revisión de límites, procedimiento de parada y
aprobación del responsable del laboratorio.
