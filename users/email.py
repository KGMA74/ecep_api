from djoser.email import ActivationEmail
from django.conf import settings

class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()

        # Récupérer le rôle de l'utilisateur
        user = context["user"]
        role = getattr(user, "role", "default")  # "default" si le rôle n'existe pas

        # Sélectionner le bon template d'email
        email_key = f"activation_{role}" if f"activation_{role}" in settings.EMAIL_TEMPLATES else "activation_default"
        # email_template = settings.EMAIL_TEMPLATES[email_key]
        email_template = EMAIL_TEMPLATES[email_key]

        # Personnaliser le sujet et le message
        context["subject"] = email_template["subject"]
        context["message"] = email_template["message"].format(
            nickname=user.nickname, 
            activation_link=context["url"]
        )
        return context

class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        self.template_name = f"users/emails/{'default' if context["user"].role=='admin' else context["user"].role}_activation.html"
        return context