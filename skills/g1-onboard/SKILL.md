---
name: g1-onboard
description: Preparar, inventariar y verificar de forma segura un Unitree G1 EDU/U2 y su estación Linux. Usar al recibir el robot, identificar variante o firmware, configurar red/DDS, instalar SDK oficial, ejecutar el primer bring-up o decidir si el equipo está listo para simulación o hardware.
---

# Incorporar un G1

1. Leer `docs/safety.md`, `docs/bringup.md` y `docs/hardware-profile.md`.
2. Mantener el proyecto en `mode = "mock"` hasta completar el perfil de hardware.
3. Recoger datos sin enviar comandos: etiquetas, DOF, manos, firmware, red y SDK entregado.
4. Consultar únicamente documentación y repositorios oficiales; fijar tags o commits.
5. Ejecutar `scripts/preflight.ps1` en Windows o los chequeos equivalentes en Linux.
6. Validar mock y simulación antes de proponer hardware.
7. Registrar incógnitas; no inferir tópicos, índices articulares, límites ni secuencias de habilitación.

Leer `references/checklist.md` para la lista de aceptación.

