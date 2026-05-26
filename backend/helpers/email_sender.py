import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

def send_attendance_email(destinatario, nombre_alumno, qr_link):
    # cuenta de google para enviar los mails
    remitente = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = "Asistencia - Código QR Dinámico"

    cuerpo = f"""
    <html>
        <body>
            <h3>Hola {nombre_alumno},</h3>
            <p>Para marcar la asistencia, escaneá el código QR o hacé clic en el enlace:</p>
            <a href="{qr_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Dar el Presente
            </a>
            <p>Recordá que el sistema validará tu <b>geolocalización</b> al momento de escanear</p>
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