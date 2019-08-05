from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Room(models.Model):
    # add response many to many for room and user
    room_name = models.TextField(verbose_name="name")
    is_private = models.BooleanField(default=False)
    last_change = models.DateTimeField(verbose_name="change time", auto_now_add=True)

    @staticmethod
    def is_exist(name):
        try:
            Room.objects.get(room_name=name)
            return True
        except Room.DoesNotExist:
            return False

    @staticmethod
    def get_default_chat():
        try:
            default_chat = Room.objects.get(room_name="global")
        except Room.DoesNotExist:
            default_chat = Room(room_name="global", is_private=False)
            default_chat.save()
        return default_chat


class ChatUser(User):

    rooms = models.ManyToManyField(Room)

    def is_user_in_room(self, room):
        try:
            self.rooms.get(room_name=room)
            return True
        except Room.DoesNotExist:
            return False

    def add_user_to_room(self, room):
        if not self.is_user_in_room(room.room_name):
            self.rooms.add(room)


class Message(models.Model):
    # add response one to many for user and message
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="message time", auto_now_add=True)
    message = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    @property
    def can_edit(self):
        if (timezone.now() - self.date) > timezone.timedelta(minutes=30):
            return False
        return True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        self.room.last_change = timezone.now()