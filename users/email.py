from djoser.email import ActivationEmail
from django.conf import settings


class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        self.template_name = f"users/emails/{'default' if context['user'].role=='admin' else context['user'].role}_activation.html"
        return context