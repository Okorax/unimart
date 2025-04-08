from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import PurchaseRequest, Message

class PurchaseRequestChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract purchase request ID from the URL
        self.purchase_request_id = self.scope['url_route']['kwargs']['purchase_request_id']
        self.group_name = f'purchase_request_{self.purchase_request_id}'

        # Fetch the purchase request
        purchase_request = await self.get_purchase_request(self.purchase_request_id)
        if not purchase_request:
            await self.close()
            return

        # Verify the user is the buyer or seller
        user = self.scope['user']
        if user.is_anonymous or (user != purchase_request.buyer and user != purchase_request.product.seller):
            await self.close()
            return

        # Accept the connection and join the group
        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, close_code):
        # Leave the group on disconnect
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Handle incoming messages
        data = json.loads(text_data)
        if data['type'] == 'chat_message':
            content = data['content']
            user = self.scope['user']
            purchase_request = await self.get_purchase_request(self.purchase_request_id)

            # Save the message
            message = await self.create_message(purchase_request, user, content)

            # Broadcast to the group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'sender': user.username,
                    'content': content,
                    'timestamp': message.timestamp.isoformat()
                }
            )

    async def chat_message(self, event):
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_purchase_request(self, purchase_request_id):
        try:
            return PurchaseRequest.objects.get(id=purchase_request_id)
        except PurchaseRequest.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, purchase_request, sender, content):
        return Message.objects.create(
            purchase_request=purchase_request,
            sender=sender,
            content=content
        )