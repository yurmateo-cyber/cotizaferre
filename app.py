from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cotizaferre-clave-secreta-2026")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'daidadalos@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'clave_temporal')
app.config['MAIL_DEFAULT_SENDER'] = 'daidadalos@gmail.com'

mail = Mail(app)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "webp", "doc", "docx", "xls", "xlsx"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solicitar', methods=['POST'])
def solicitar():
    nombre = request.form.get('nombre') or 'No especificado'
    telefono = request.form.get('telefono') or 'No especificado'
    marca = request.form.get('marca') or 'No especificada'
    comentarios = request.form.get('comentarios') or 'Sin comentarios'
    
    file = request.files.get('documento') or request.files.get('archivo')
    
    try:
        msg = Message(
            subject=f"📩 Nueva Cotización: {nombre} ({marca})",
            recipients=['daidadalos@gmail.com']
        )
        msg.body = f"""
        Nueva solicitud en CotizaFerre:
        - Cliente: {nombre}
        - Teléfono: {telefono}
        - Marca: {marca}
        - Comentarios: {comentarios}
        """
        
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_bytes = file.read()
            msg.attach(filename, file.content_type or 'application/octet-stream', file_bytes)
            
        mail.send(msg)
        flash("Solicitud enviada con éxito.", "success")
    except Exception as e:
        print(f"Error: {e}")
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
