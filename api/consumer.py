import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpRequest
from django.contrib.auth.models import User
from rest_framework.request import Request
import queue #used between threads
import threading
from .ScrapUSA import ScrapUSA
import time
import shared

class ChatConsumer(AsyncWebsocketConsumer):
    q = queue.Queue()
    keywords =""

    async def connect(self):
        print(f'jothi connect request')
        self.group_name = "broadcast"

        # Join room group
        await self.channel_layer.group_add (
            self.group_name,
            self.channel_name
        )

        await self.accept()
        #important to send READY channel
        await self.channel_layer.group_send(
            "broadcast",
            {
                'type': 'chat_message',
                'message': "READY"
            }
        )
        
        return
    
    async def disconnect(self, close_code):
        print(f'jothi WebSocket disconnecting')
          # Leave room group
        self.channel_layer.group_discard(
            "broadcast",
            self.channel_name
        )
        shared.stop_scrap = True
        
    async def chat_message(self, event):
        message = event['message']
        print('sending ', message)
        #print('jothi chat message event', message)

        # Send message to WebSocket client (react)
        # use await
        await self.send(text_data=json.dumps({
            'message': message
        }))
    
    async def receive(self, text_data):
        print("jothi msg received ", text_data)
        
        json_data = json.loads(text_data)
        command = json_data['command']
        match command:
            case "StopScrap":
                shared.stop_scrap = True

            case "StartScrap":  
                shared.stop_scrap = False  
                self.keywords = json_data['keywords']
                self.scrapThread = threading.Thread(target=self.scrapfunction)
                self.scrapThread.daemon = True
                self.scrapThread.start()

    def scrapfunction(self):
        #sending scrap status to client
        self.sendThread = threading.Thread(target=self.sendfunction)
        self.sendThread.daemon = True
        self.sendThread.start()

        self.q.put("Started Scrapping from craigslist USA ")
        self.q.put("\n")
        #pass shared queue
        print('jothi send words ', self.keywords)
        scrap_instance = ScrapUSA(self.keywords,self.q)
        scrap_instance.usamain()

        return

    def sendfunction(self):
        channel_layer = get_channel_layer()

        while True:
            if shared.stop_scrap == True:
                break
            msg = self.q.get()
            async_to_sync(channel_layer.group_send)(
                "broadcast",
                {
                    'type': 'chat_message',
                    'message': msg
                }
            )
            time.sleep(3)
            self.q.task_done()




