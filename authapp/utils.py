import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

def send_email_with_html_body(subject:str, receivers:list, template:str, context:dict):
    try:
        message = render_to_string(template,context)
        send_mail(
            subject=subject,
            message='',  # Message texte brut (vide si tu n'en as pas besoin)
            from_email=settings.EMAIL_HOST_USER,  # Adresse de l'expéditeur
            recipient_list=receivers,  # Liste des destinataires (obligatoire)
            fail_silently=False,  # Laisser False pour voir les erreurs
            html_message=message  # Contenu HTML de l'email
        )

        return True
    except Exception as e:
        logger.error(e)
    return False