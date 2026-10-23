COTIZAFERRE - sitio web inicial (Python + Flask)
pip install Flask gunicorn
QUÉ INCLUYE
- Página minimalista y adaptable a celular y computadora.
- Marcas: Tuboplast, Nicoll y Pavco.
- Formulario para nombre/empresa, teléfono o WhatsApp, marca, comentarios y archivo.
- Recibe PDF, imágenes, Word y Excel (máximo 15 MB).
- Guarda solicitudes en solicitudes.json y archivos en la carpeta uploads/.
- No publica precios automáticamente: el equipo prepara y envía la cotización.

REQUISITOS
- Python 3.10 o superior recomendado.
- Internet solo para cargar la fuente DM Sans desde Google Fonts; la web funciona sin ella usando fuentes alternativas.

CÓMO EJECUTAR EN WINDOWS
1. Descomprime cotizaferre.zip en una carpeta.
2. Abre esa carpeta.
3. En la barra de dirección del Explorador escribe cmd y pulsa Enter.
4. Ejecuta:
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
5. Abre en el navegador:
   http://127.0.0.1:5000

DÓNDE LLEGAN LAS SOLICITUDES
- Los datos se guardan en solicitudes.json.
- Los archivos se guardan en uploads/.
- Este prototipo NO envía avisos por correo ni WhatsApp todavía. Debes revisar esos archivos para ver las solicitudes.

IMPORTANTE ANTES DE PUBLICAR EN INTERNET
Esto es una base funcional para pruebas locales, no una instalación lista para recibir documentos del público. Antes de publicarla:
- Cambia SECRET_KEY por una clave aleatoria y mantenla privada.
- Desactiva debug y usa un servidor de producción.
- Protege con inicio de sesión el acceso a solicitudes y archivos; los documentos pueden contener información personal.
- Configura HTTPS, copias de seguridad, límites y retención/eliminación de archivos.
- Añade un canal privado de notificación al negocio (correo o WhatsApp Business API) si lo necesitas.
- Publica en un servicio que soporte Python/Flask y configura almacenamiento persistente.
- Añade aviso de privacidad y consentimiento adecuado para el tratamiento de datos personales en Perú.

COTIZACIÓN EN PDF
La página recibe el archivo del cliente, pero no genera ni envía el PDF de precios. El equipo prepara el documento de cotización y se lo envía al cliente por el canal acordado. Puede añadirse un panel privado para administrar solicitudes y adjuntar el PDF de respuesta.
