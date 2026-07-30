---
name: g1-diagnose
description: Diagnosticar fallos de configuración, red, CycloneDDS/ROS 2, telemetría, SDK, simulación y estado de un Unitree G1 EDU/U2 sin emitir movimiento. Usar cuando no conecta, faltan tópicos, el estado está vencido, difieren simulación y robot o una prueba de puesta en marcha falla.
---

# Diagnosticar un G1

1. Detener publicadores y asegurar físicamente el robot antes de investigar.
2. Leer `references/runbook.md`.
3. Capturar configuración saneada, plataforma, interfaz, rutas, versiones y timestamps.
4. Avanzar de abajo arriba: energía/estado, enlace, IP, DDS, mensajes, SDK, aplicación.
5. Usar consultas de solo lectura; no probar conectividad enviando movimiento.
6. Separar hechos, hipótesis y próxima prueba.
7. Redactar un informe reproducible sin serie, credenciales ni datos sensibles.

Ejecutar `scripts/collect-local.ps1` para un diagnóstico local no invasivo.

