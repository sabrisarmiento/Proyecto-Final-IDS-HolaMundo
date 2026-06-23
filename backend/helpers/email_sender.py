import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

def send_attendance_email(destinatario, nombre_alumno, attendance_link, valido_hasta=None, clase=None):
    remitente = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = f"Asistencia - Clase {clase.get('numero')} de {clase.get('materia')}" if clase else "Asistencia - Link para marcar presente"

    validez = f"<p>El código es válido hasta las <b>{valido_hasta}</b>.</p>" if valido_hasta else ""
    detail = (
        f"<p><b>Clase N.º {clase.get('numero')}</b> — {clase.get('materia')} (Cátedra {clase.get('catedra')})</p>"
        f"<p>Fecha: {clase.get('fecha')} · Tema: {clase.get('temas') or '—'}</p>"
    ) if clase else ""

    is_virtual = bool(clase) and clase.get("modalidad") == "Virtual"
    geo_aviso = "" if is_virtual else "<p>Recordá que el sistema validará tu <b>geolocalización</b> al dar el presente.</p>"

    cuerpo = f"""
    <html>
        <body>
            <h3>Hola {nombre_alumno},</h3>
            {detail}
            <p>Para marcar tu asistencia, hacé clic en el siguiente enlace:</p>
            <a href="{attendance_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Dar el Presente
            </a>
            {geo_aviso}
            {validez}
        </body>
    </html>
    """
    mensaje.attach(MIMEText(cuerpo, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.send_message(mensaje)
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar mail: {e}")
        return False