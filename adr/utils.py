# profiles/utils.py
from io import BytesIO
from uuid import uuid4
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.conf import settings
def make_avatar_square(django_file, size=512, fmt="WEBP", quality=86):
    """
    - Corrige orientación EXIF
    - Recorte centrado a cuadrado
    - Redimensiona con LANCZOS
    - Exporta a WEBP (o JPEG)
    """
    img = Image.open(django_file)
    img = ImageOps.exif_transpose(img)     # corrige orientación
    img = img.convert("RGB")

    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top  = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = img.resize((size, size), Image.LANCZOS)

    buf = BytesIO()
    if fmt.upper() == "WEBP":
        img.save(buf, "WEBP", quality=quality, method=6)
        ext = "webp"
    else:
        img.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
        ext = "jpg"

    name = f"avatar_{uuid4().hex}.{ext}"
    return ContentFile(buf.getvalue(), name=name)

def enviar_notificacion_asunto(asunto: str, mensaje: str, destinatarios: list[str], from_email: str | None = None):
    """
    Envía un correo usando SendGrid HTTP API en segundo plano.
    No bloquea la operación principal y evita timeouts de Gunicorn.
    """
    import logging
    import threading
    from decouple import config
    
    logger = logging.getLogger(__name__)
    
    def _enviar_en_background():
        """Función interna que ejecuta el envío en un hilo separado usando SendGrid API"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail, To
            
            # Obtener configuración
            api_key = config('SENDGRID_API_KEY', default='')
            sender_email = from_email or config('EMAIL_FROM', default='iquiquepracticantes@gmail.com')
            
            if not api_key:
                logger.error("❌ SENDGRID_API_KEY no está configurada")
                return
            
            # Crear el mensaje
            message = Mail(
                from_email=sender_email,
                to_emails=[To(email) for email in destinatarios],
                subject=asunto,
                plain_text_content=mensaje
            )
            
            # Enviar usando la API HTTP
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"✅ Correo enviado exitosamente: '{asunto}' a {destinatarios}")
            else:
                logger.error(f"❌ Error SendGrid (código {response.status_code}): {response.body}")
                
        except Exception as e:
            logger.error(f"❌ Error al enviar correo '{asunto}' a {destinatarios}: {e}")
    
    # Iniciar el hilo para enviar el correo sin bloquear
    thread = threading.Thread(target=_enviar_en_background, daemon=True)
    thread.start()
    logger.info(f"📧 Correo programado para envío en segundo plano: '{asunto}'")