# Puesta en marcha

## 1. Inventario sin energizar

Completar [hardware-profile.md](hardware-profile.md), fotografiar etiquetas, identificar cargador,
baterías, mando, E-stop, soporte y manuales recibidos. No conectar actuadores.

## 2. Estación Linux

Usar Ubuntu compatible con la versión oficial seleccionada. Crear una cuenta sin privilegios,
sincronizar reloj, registrar la interfaz Ethernet dedicada y desactivar Wi-Fi durante pruebas si
la política del laboratorio lo permite.

## 3. Software

Fijar commits/tags de los repositorios oficiales, verificar licencias y checksums, y mantener SDK,
simulador y aplicación en entornos separados. Unitree SDK2 usa CycloneDDS; no mezclar el dominio
de simulación con el del robot.

## 4. Verificación local

Ejecutar `g1ctl doctor`, `g1ctl status` y `python -m unittest discover -s tests` con
`mode = "mock"`. Después implementar el
adaptador de simulación y repetir los mismos casos de uso.

## 5. Primera conexión

Robot inmóvil y soportado, mando y E-stop verificados. Conectar únicamente lectura de estado.
Registrar firmware, tópicos/servicios DDS, frecuencia, latencia, batería y mapa articular. No
enviar comandos hasta comparar esa evidencia con el SDK de la versión fijada.

## 6. Primer movimiento

Revisión por dos personas, límites mínimos, watchdog activo y una sola articulación o API de alto
nivel soportada por el fabricante. Probar parada antes que movimiento. Terminar si el estado real
no coincide con el esperado.
