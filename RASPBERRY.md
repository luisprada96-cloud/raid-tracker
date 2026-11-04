# Raid Tracker — primer prototipo

Aplicación personal para registrar fallos por integrante, día y raid. Requiere Python 3.9 o posterior, con datos de zona horaria de Europa/Madrid disponibles. No necesita dependencias externas.

## Arrancar

```bash
python3 app.py
```

Abre http://localhost:8000 en el mismo equipo. Pulsa Ctrl+C para detenerla. Los datos se guardan en `raid.db` en el directorio desde el que se ejecuta; realiza copias de seguridad de ese archivo.

El servidor escucha solo en el propio equipo y no incluye inicio de sesión. Antes de acceder desde otros dispositivos o Internet hace falta configurar acceso protegido. No se ha desplegado en la Raspberry.

## Incluye

Crear raids con integrantes, registrar un fallo con un toque, deshacer el último fallo de cada integrante, consultar totales e historial por día, y archivar raids. El día se calcula en la zona horaria de Madrid.

## Por desarrollar

Editar integrantes, reabrir raids, gestionar sesiones que cruzan medianoche, estadísticas adicionales y despliegue seguro. Es un prototipo para validar el flujo.
