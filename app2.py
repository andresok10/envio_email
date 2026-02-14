import os
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, send_from_directory
from flask_socketio import SocketIO

load_dotenv()

app = Flask(__name__, template_folder="vieww")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecret")

class Config: ## Configuración de Flask-Mail y smtp
    MAIL_SERVER = "smtp.gmail.com"   # smtp.mailtrap.io     smtp.gmail.com
    MAIL_PORT = 587
    MAIL_USERNAME = "davexgarcia@gmail.com" #  os.getenv("MAIL_USERNAME")  # usar .env
    MAIL_PASSWORD = "imai fcle anny vhxp"
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    #SECRET_KEY = "zzzzzzzzzzzxxxxxx"
    #MAIL_DEBUG = True
#class DevelopmentConfig(Config):
#    DEBUG = True
#class ProductionConfig(Config):
#    DEBUG = False
#    MAIL_DEBUG = False
#app.config.from_object('config.DevelopmentConfig')  # or ProductionConfig

app.config.from_object(Config)

# CONFIGURACIÓN DE SOCKET.IO
socketio = SocketIO(app, async_mode="threading", manage_session=False, cors_allowed_origins="*")

logging.basicConfig(level=logging.INFO)

# CONTROLADOR DE MESA PELADO,ARCHIVADOR  COORDINADOR DE LIMPIEZA
# ASISTENTE DE LIQUIDACIONES   SUPERVISOR IQF
# JEFE DE VALOR AGREGADO, SUPERVISOR PTAR (PLANTA DE TRATAMIENTO DE AGUAS RESIDUALES)
# Supervisor de clasificación
# INGENIERO JR. I - DPTO ARTIFICIAL INTELLIGENCE (AI)
## AYUDANTE TECNICO - OPU
# Coordinador de calidad
# Envasador  # estibador
a0 = "Monitor de Alimentacion automatica - Dave Garcia(Tecnologo en Sistema)"
a1 = "Control Monitor de calidad o Liquidador(PRODUCCION-V.A) - Dave Garcia(Tecnologo en Sistema)"
a2 = "Auxiliar de Operaciones - Dave Garcia(Tecnologo en Sistema)"
a3 = "Supervisor de Limpieza - Dave Garcia(Tecnologo en Sistema)"
a4 = "Obrero de Planta - Dave Garcia(Tecnologo en Sistema)"

a17 = "ASISTENTE DE SELECCION - Dave Garcia(Ingeniero en Sistema)"
a5 = "Supervisor de Produccion - Dave Garcia(Tecnologo en Sistema)"
a6 = "DESARROLLADOR DE SOFTWARE - Dave Garcia(Tecnologo en Sistema)"
a7 = "TECNOLOGO EN SISTEMA - Dave Garcia"
a8 = "Monitorista - Dave Garcia(Tecnologo en Sistema)"
a9 = "Monitoreo - Dave Garcia(Tecnologo en Sistema)"
a10 = "DIGITADOR - Dave Garcia(Tecnologo en Sistema)"
a11 = "DIGITADOR(PLANTA,EMPAQUE) - Dave Garcia(Tecnologo en Sistema)"
a12 = "DIGITALIZADOR - Dave Garcia(Ingeniero en software)"
###
a13 = "INGENIERO EN SOFTWARE - Dave Garcia"
a15 = "DESARROLLADOR FRONT-END y BACK-END - Dave Garcia(Ingeniero en software)"
a16 = "TECNICO DE INFRAESTRUCTURA(Sistemas) - Dave Garcia(Ingeniero en software)"
a18 = "INGENIERO DE SOFTWARE - Dave Garcia(Ingeniero en Software)"
a19 = "INGENIERO DE SOFTWARE JUNIOR - Dave Garcia(Ingeniero en Software)"
a20 = "INGENIERO JUNIOR - Dave Garcia(Ingeniero en Software)"
a21 = "INGENIERO DE MESA - Dave Garcia(Ingeniero en Sistema)"
a22 = "DESARROLLADOR WEB - Dave Garcia(Tecnologo en Sistema)"
a23 = "DESARROLLADOR WEB JUNIOR - Dave Garcia(Tecnologo en Sistema)"
a24 = "DESARROLLADOR JUNIOR - Dave Garcia(Ingeniero en software)"
a25 = "DESARROLLADOR SENIOR - Dave Garcia(Ingeniero en software)"
a26 = "Fiscalizador Motorizado - Dave Garcia(Ingeniero en software)"
a27 = "AYUDANTE TECNICO - Dave Garcia(Ingeniero en software)"
a28 = "AYUDANTE COORDINADOR - OPERACIONES URBANAS - Dave Garcia(Ingeniero en software)"
a29 = "BODEGUERO o AYUDANTE DE BODEGA GUAYAQUIL - Dave Garcia(Tecnologo en Sistema)"

htmlx = "app3.html"
a = "Solicitud para"
# asunto = a+" "+a0
asunto = a3

from correos import prueba, fabricas_pro, empacadoras, guardia
correos = empacadoras
msg_camaron = """
<td style="font-family:Arial, sans-serif; font-size:14px; line-height:1.6; color:#000;">
Buenos dias estimado/a.<br>
Espero que esté bien.<br><br>

Me dirijo a usted para expresar mi interés laboral y asi contribuir al éxito de la empresa.<br>
Adjunto mi CV para su consideración, en cual detallo mi experiencia y habilidades.<br><br>

Saludos cordiales,<br>
Dave Garcia<br>
0961655965 - 0982601661<br>
davexgarcia@gmail.com
</td>
"""

# Espero que este mensaje le encuentre bien.
msg_pro = """
<td style="font-family:Arial, sans-serif; font-size:14px; line-height:1.6; color:#000;">
Buenos días estimado/a.<br>
Espero que esté bien.<br><br>

Me dirijo a usted para expresar mi interés laboral y así contribuir al éxito de la empresa.<br>
Cuento con una sólida formación en sistemas y tecnologías como herramientas de Office, Front-End y Back-End, lenguajes de programación y frameworks, etc.<br>
Soy una persona apasionada por el aprendizaje continuo y la innovación, y siempre estoy buscando nuevas formas de mejorar y aportar valor.<br><br>

Adjunto mi CV para su consideración, en el cual detallo mi experiencia y habilidades.<br><br>

Dave Garcia<br>
0961655965 - 0982601661<br>
davexgarcia@gmail.com
</td>
"""

msg = msg_pro

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVOS = f"{BASE_DIR}/camaron_pdf"
#ARCHIVOS = "D:/C_VITAE_DAVE/camaron_pdf"

@app.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(ARCHIVOS, filename)

def obtener_adjuntos():
    if not os.path.exists(ARCHIVOS):
        return []
    return [
        os.path.join(ARCHIVOS, f)
        for f in os.listdir(ARCHIVOS)
        if os.path.isfile(os.path.join(ARCHIVOS, f))
    ]

@app.route("/")
def index():
    archivos_para_vista = [
        {"filename": os.path.basename(p), "filepath": p}
        for p in obtener_adjuntos()
    ]
    return render_template(
        "app3.html",
        files=archivos_para_vista,
        emails=correos,
        asuntox=asunto
    )

@app.route("/send_email", methods=["POST"])
def send_email():
    archivos_a_enviar = obtener_adjuntos()

    def background_sender():
        with app.app_context():
            total = len(correos)
            enviados = 0
            fallidos = 0

            socketio.emit("process_status", {"status": "started", "total": total})

            try:
                # Iniciar conexión única
                server = smtplib.SMTP(app.config["MAIL_SERVER"], app.config["MAIL_PORT"])
                server.starttls()
                server.login(app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])

                for idx, recipient in enumerate(correos, start=1):
                    try:
                        mime_msg = MIMEMultipart()
                        mime_msg["From"] = app.config["MAIL_USERNAME"]
                        mime_msg["To"] = recipient
                        mime_msg["Subject"] = asunto
                        mime_msg.attach(MIMEText(msg, "html"))

                        # --- Lógica de Adjuntos Corregida ---
                        for ruta in archivos_a_enviar:
                            nombre_fichero = os.path.basename(ruta)
                            with open(ruta, "rb") as adj:
                                part = MIMEBase("application", "octet-stream")
                                part.set_payload(adj.read())
                                encoders.encode_base64(part)
                                part.add_header("Content-Disposition", f'attachment; filename="{nombre_fichero}"')
                                mime_msg.attach(part)

                        server.sendmail(app.config["MAIL_USERNAME"], recipient, mime_msg.as_string())
                        enviados += 1
                        estado = "success"
                        
                    except Exception as e:
                        fallidos += 1
                        estado = "failure"
                        logging.error(f"Error enviando a {recipient}: {e}")

                    # Notificar progreso
                    socketio.emit("progress_update", {
                        "recipient": recipient,
                        "sent": enviados,
                        "invalid": fallidos,
                        "current": idx,
                        "total": total,
                        "progress": round((idx / total) * 100, 2),
                        "status": estado,
                    })

                    # --- Control Anti-Spam ---
                    #if idx % 20 == 0:
                    #    time.sleep(60) # Pausa larga cada 20 correos
                    #else:
                    #    time.sleep(10) # Pausa corta entre envíos
                    '''PAUSA_LARGA = 60
                    PAUSA_CORTA = 10
                    time.sleep(PAUSA_LARGA if idx % 20 == 0 else PAUSA_CORTA)'''
                    time.sleep(60 if idx % 20 == 0 else 10)

                server.quit()
                socketio.emit("process_status", {"status": "finished"})

            except Exception as e:
                logging.error(f"Error crítico en el servidor SMTP: {e}")
                socketio.emit("process_status", {"status": "error", "message": str(e)})

    socketio.start_background_task(background_sender)
    flash(f"Iniciando envío a {len(correos)} contactos...", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":  ##
    socketio.run(app, debug=False)
    #socketio.run(app, host="127.0.0.1", port=5000, debug=False)
    #socketio.run(app, debug=False, use_reloader=False)
    #app.run(debug=True, use_reloader=False, port=5008)