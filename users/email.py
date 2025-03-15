from urllib.parse import urlencode
from djoser.email import ActivationEmail
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        self.template_name = f"users/emails/{'default' if context['user'].role=='admin' else context['user'].role}_activation.html"
        return context
    
    
def send_verification_email(student, verification_code, parent):
    

    url = f"{getattr(settings, 'PROTOCOL', 'http')}://{settings.DOMAIN}/parent/verify"
    # Prepare context for the email template
    context = {
        'code': verification_code,
        'student_id': student.user.id,
        'parent_name': f"{parent.user.firstname} {parent.user.lastname}",
        'verification_url': url,
        'valid_hours': 24
    }
    
    # Render HTML email
    html_message = render_to_string('users/emails/add_student_verification.html', context)
    # Create plain text version by stripping HTML
    plain_message = strip_tags(html_message)
    
    send_mail(
        'Vérification pour ajout à un compte parent',
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [student.user.email],
        html_message=html_message,
        fail_silently=False,
    )
    
