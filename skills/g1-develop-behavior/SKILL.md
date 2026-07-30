---
name: g1-develop-behavior
description: Diseñar e implementar comportamientos, locomoción, manipulación o percepción para Unitree G1 EDU/U2 con arquitectura de puertos y adaptadores, límites de seguridad y promoción mock-simulación-hardware. Usar al añadir una capacidad del robot, integrar SDK2/ROS 2, crear un controlador o preparar sim-to-real.
---

# Desarrollar un comportamiento

1. Leer `docs/architecture.md` y `docs/safety.md`.
2. Definir entradas, salidas, frecuencia, autoridad de control, límites y condiciones de aborto.
3. Implementar primero contra `RobotPort` sin importar SDK/DDS en el dominio.
4. Añadir pruebas unitarias para límites, estado vencido, desconexión, E-stop y apagado.
5. Probar en `MockRobot`; implementar después un adaptador de simulación.
6. Guardar evidencia según `references/promotion-gates.md`.
7. Implementar hardware solo contra la variante y versión confirmadas.
8. Mantener parada idempotente y ejecutarla en `finally`.

No copiar índices articulares ni constantes entre variantes.

