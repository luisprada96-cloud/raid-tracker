# Raid Tracker — contexto para continuar con Codex

## Proyecto

Aplicación personal de Luis para registrar manualmente los fallos de cada integrante durante las raids de Final Fantasy XIV. Una raid representa un tier o una pelea que puede durar varios meses y contiene un número variable de integrantes y días. La prioridad es que sea muy fácil apuntar fallos en directo.

- Repositorio público: https://github.com/luisprada96-cloud/raid-tracker
- Web de prueba: https://luisprada96-cloud.github.io/raid-tracker/
- Objetivo posterior: alojar el proyecto en una Raspberry Pi cuando Luis tenga acceso físico a ella.
- El proyecto no está instalado en la Raspberry todavía.

## Qué quiere Luis

- Al entrar, ver directamente el dashboard de la raid cuyo día se guardó más recientemente, con botones de sus integrantes para sumar o deshacer fallos.
- En el menú superior, crear raids y abrir una biblioteca de raids activas y archivadas.
- Desde la biblioteca, llevar cualquier raid al dashboard para añadir un día, editar el nombre de la raid y de sus integrantes, o eliminar la raid con confirmación.
- Cada día se puede cerrar con **Guardar día**, consultar y editar después. Puede contener un enlace opcional a FFLogs, introducido manualmente. El enlace no requiere integración con su API.
- Conservar el historial de fallos al cambiar el nombre de un integrante. Se admiten raids con distinto número de integrantes.
- Las sesiones se organizan por fechas en la zona horaria de Madrid. El comportamiento de una sesión que cruza medianoche sigue pendiente de decidir.
- El diseño actual, oscuro, sencillo y práctico, le gusta como punto de partida. Quiere seguir iterando después de probarlo.

## Estado técnico actual

**Hay dos prototipos diferentes en el repositorio; el que se está probando y desarrollando es el de GitHub Pages.**

- `docs/index.html`: aplicación estática actual, con HTML, CSS y JavaScript en el mismo archivo. GitHub Pages publica la carpeta `/docs` de la rama `main`. Los cambios en esta carpeta se despliegan mediante GitHub Actions.
- Almacenamiento de la versión publicada: `localStorage` del navegador, clave `raid-tracker-v1`. Los datos están ligados al navegador y dispositivo, no se sincronizan y pueden perderse si se borran los datos del navegador. No hay copia en GitHub ni en la Raspberry.
- Los fallos se guardan automáticamente mientras se pulsan los botones; **Guardar día** cierra el día y marca su última fecha de guardado. Los días cerrados se pueden editar. Existe una migración en el frontend de los registros del formato inicial al formato de sesiones; preservarla y comprobar la compatibilidad al cambiar el modelo.
- `app.py`, `index.html` en la raíz y `RASPBERRY.md`: primer prototipo Python/SQLite, anterior a la versión de Pages. **No incorpora necesariamente las funciones nuevas**: no asumir que representa el producto actual ni que sus datos son los de `localStorage`. Escucha en `127.0.0.1:8000` y guarda `raid.db`; no se ha preparado para acceso remoto.
- No hay sincronización ni migración implementada entre el prototipo estático y SQLite. Antes de sustituir almacenamiento o cambiar de dominio/dispositivo, planificar una exportación/importación o copia que permita conservar los datos de prueba existentes.

## Empezar en el PC

```bash
git clone https://github.com/luisprada96-cloud/raid-tracker.git
cd raid-tracker
python3 -m http.server 8000 --directory docs
```

Abrir `http://localhost:8000` para probar el frontend de Pages. Este origen tiene su propio `localStorage`: no comparte automáticamente los datos de la web publicada. Para probar el prototipo Python antiguo por separado, detener el servidor anterior y ejecutar `python3 app.py` desde la raíz; consultar `RASPBERRY.md` para sus requisitos y limitaciones.

## Recomendaciones para la siguiente iteración

1. Revisar el código y el estado más reciente del repositorio antes de modificarlo; este documento es una foto del 4 de noviembre de 2026.
2. Pedir a Luis las próximas mejoras concretas e implementarlas sobre `docs/index.html` mientras GitHub Pages siga siendo la versión de referencia.
3. Al cambiar flujos, probar creación de raids, suma y deshacer, cierre y reapertura de días, edición de nombres sin pérdida de historial, enlaces de FFLogs, archivado, eliminación y compatibilidad con datos anteriores.
4. Antes de pasar a la Raspberry, acordar cómo se almacenarán, respaldarán y migrarán los datos, así como la forma de acceso desde otros dispositivos. Mantener el prototipo accesible mientras se valida el traslado.
