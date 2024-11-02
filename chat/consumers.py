from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message
from users.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"chat_{self.scope['user'].id}"
        self.room_group_name = f"chat_{self.scope['user'].id}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        recipient_id = data['recipient_id']
        message = data['message']

        recipient = await User.objects.get(id=recipient_id)

        await Message.objects.create(
            sender=self.scope['user'],
            recipient=recipient,
            content=message
        )

        await self.channel_layer.group_send(
            f"chat_{recipient_id}",
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope['user'].username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))
