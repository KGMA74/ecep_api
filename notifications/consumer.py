# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = f'notifications_{self.user.id}'

        # Ajouter l'utilisateur à un groupe Redis
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Supprimer l'utilisateur du groupe Redis
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        notification = data['notification']
        
        # Enregistrer ou gérer la notification selon tes besoins

    async def send_notification(self, message):
        # Envoyer un message à un client via WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
