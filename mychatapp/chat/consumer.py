import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import *


class ChatConsumer(AsyncWebsocketConsumer):
    
    
    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name,self.channel_name)
        await self.accept()
        

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name,self.channel_name)
        
    async def recieve(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json
        
    
    async def send_message(self,event):
        data = event['message']
        await self.create_message(data=data)
        response_data = {
            'sender':data['sender'],
            'message':data['message']
        }
        await self.send(text_data=json.dumps({'message':response_data}))