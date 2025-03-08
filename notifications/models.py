from django.db import models

class Notification(models.Model):
    user = models.ForeignKey('users.User', related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # Indicateur si la notification a été lue

    def __str__(self):
        return f"Notification for {self.user.email} at {self.created_at}"

    def send_notification(self):
        # Logique pour envoyer la notification via WebSocket
        pass

    def delete_notification(self):
        self.delete()
