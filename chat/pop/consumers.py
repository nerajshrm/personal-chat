# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))




from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        #before websocket when the user get to the page url , show all the message from the 
        #database too , 
        #if logged in , if have permission to chat too ,  then join the group , 

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group, 
        #send message to chat_message function , which send to frot end,  
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
        #chat_message fucntion is used , so that the message are received by each member in 
        #group-name or channelname 
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event): #function to receive message send to group , and process it , 
    #much like receive , process the indiviual message 
        message = event['message']
        
        #also save the message to database before sending to frontend
        """
        Thread.objects.create(message =message, user= self.user, thread=self.thread )
        """

        # Send message to WebSocket(frontend)
        self.send(text_data=json.dumps({
            'message': message
        }))



