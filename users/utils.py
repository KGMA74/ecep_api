from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

def send_custom_activation_email(user):
    subject = ''
    html_message = ''
    
    if user.role == 'student':
        subject = _("Activate your Student Account")
        html_message = render_to_string('emails/student_activation.html', {'user': user})
    elif user.role == 'teacher':
        subject = _("Activate your Teacher Account")
        html_message = render_to_string('emails/teacher_activation.html', {'user': user})
    elif user.role == 'parent':
        subject = _("Activate your Parent Account")
        html_message = render_to_string('emails/parent_activation.html', {'user': user})
    else:
        subject = _("Activate your Account")
        html_message = render_to_string('emails/default_activation.html', {'user': user})
    
    # Envoyer l'email
    send_mail(
        subject,
        strip_tags(html_message),  # Partie texte de l'email
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message
    )
