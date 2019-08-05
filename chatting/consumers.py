from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Room
from asgiref.sync import async_to_sync
from django.utils import timezone


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
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
        user = self.scope['user']
        event = text_data_json["event"]
        room = Room.objects.get(room_name=self.room_name)
        if event == "chat_message":
            model_object = Message(message=message, room=room, user=user)
            model_object.save()
        elif event == "update_message":
            model_object = Message.objects.get(pk=text_data_json["message_id"])
            model_object.message = message
            model_object.save()
        now_time = model_object.date.strftime('%H:%M')
        room.last_change = model_object.date
        room.save()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': event,
                'message': message,
                'user': str(user),
                'now_time': str(now_time),
                'id': model_object.pk
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user = event["user"]
        now_time = event["now_time"]
        message_id = event["id"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'now_time': now_time,
            'id': message_id,
            'event': "chat_message",
        }))

    def update_message(self, event):
        message = event['message']
        user = event["user"]
        now_time = event["now_time"]
        message_id = event["id"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'now_time': now_time,
            'id': message_id,
            'event': "update_message"
        }))


class ChatListConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope["user"]
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            str(self.user.pk),
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            str(self.user.pk),
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event = text_data_json["event"]
        room = text_data_json["room"]
        room = Room.objects.get(room_name=room)
        room_name = room.room_name if not room.is_private else [i.username for i in room.chatuser_set.all() if i !=
                                                                self.user.username][0]
        if room.message_set.last():
            time = room.message_set.last().date
        else:
            time = timezone.now()
        time = time.strftime("%b. %e, %Y, |%I:%M %p").split("|")
        time = time[0] + time[1] if time[1][0] != "0" else time[0] + time[1][1:]
        time = time.replace("AM", "a.m.") .replace("AM", "a.m.") if "AM" in time else time.replace("PM", "p.m.")
        for user in room.chatuser_set.all():
            async_to_sync(self.channel_layer.group_send)(
                str(user.pk),
                {
                    'type': event,
                    'room': room.pk,
                    'last_message':
                        {'message': room.message_set.last().message, 'user': room.message_set.last().user.username},
                    'is_private': room.is_private,
                    'room_name': room_name,
                    'last_change': time
                }
            )

    def update_chat(self, event):
        event.update({'event': "new_message"})
        self.send(text_data=json.dumps(event))
