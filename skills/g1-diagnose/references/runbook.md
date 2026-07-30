# Runbook

1. Confirmar E-stop, batería, modo del robot y ausencia de otros controladores.
2. Verificar enlace físico y que la interfaz elegida exista y tenga la subred esperada.
3. Confirmar dominio DDS y `CYCLONEDDS_URI`; simulación y hardware no deben colisionar.
4. Enumerar tópicos/servicios y comparar tipos con la versión exacta del SDK/firmware.
5. Medir frecuencia, pérdida y antigüedad de estado sin publicar comandos.
6. Reproducir en un ejemplo oficial de solo lectura.
7. Reproducir en mock/simulación para separar aplicación de transporte.
8. Adjuntar comando, salida, hora, commit y configuración saneada.

