from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import ListView
import json
import hashlib
from .models import Message, Room, ChatUser


def index(request):
    chat_user = ChatUser.objects.get(username=request.user.get_username())
    chat_list = chat_user.rooms.all()

    def merge_sort_chat(sort_list):

        def merge(_left, _right):
            result_merging = []
            while len(_left) > 0 and len(_right) > 0:
                if _left[0].last_change >= _right[0].last_change:
                    result_merging.append(_left[0])
                    del _left[0]
                else:
                    result_merging.append(_right[0])
                    del _right[0]
            while len(_left) > 0:
                result_merging.append(_left[0])
                del _left[0]
            while len(_right) > 0:
                result_merging.append(_right[0])
                del _right[0]
            return result_merging

        if len(sort_list) <= 1:
            return sort_list
        middle = len(sort_list) // 2
        left = sort_list[:middle]
        right = sort_list[middle:]
        left = merge_sort_chat(left)
        right = merge_sort_chat(right)
        result = merge(left, right)
        return result

    chat_list = merge_sort_chat(chat_list)
    return render(request, 'chat/index.html', {"chat_list": chat_list, "chat_user": chat_user})


class RoomView(ListView):
    template_name = 'chat/room.html'

    def get(self, request, *args, **kwargs):
        room_name = kwargs["room_name"]
        if not Room.is_exist(room_name):
            room = Room(room_name=room_name)
            room.save()
        else:
            room = Room.objects.get(room_name=room_name)
        ChatUser.objects.get(username=request.user.get_username()).add_user_to_room(room)
        messages = list(Message.objects.filter(room=room).order_by("-date"))[:10]
        messages.reverse()
        response = render(request, self.template_name, {"chat_messages": messages,
                                                        "room_name_json": mark_safe(json.dumps(room_name)),
                                                        "chat_name": room.room_name
                                                        })
        return response


class PrivateRoomView(ListView):

    template_name = 'chat/room.html'

    def get(self, request, *args, **kwargs):
        from_user = request.user.get_username()
        to_user = kwargs["username"]
        room_name = hashlib.md5(",".join(sorted([from_user, to_user])).encode()).hexdigest()
        try:
            room = Room.objects.get(room_name=room_name, is_private=True)
        except Room.DoesNotExist:
            room = Room(room_name=room_name, is_private=True)
            room.save()
        ChatUser.objects.get(username=from_user).add_user_to_room(room)
        ChatUser.objects.get(username=to_user).add_user_to_room(room)
        messages = list(Message.objects.filter(room=room).order_by("-date"))[:10]
        messages.reverse()
        response = render(request, self.template_name, {"chat_messages": messages,
                                                        "room_name_json": mark_safe(json.dumps(room_name)),
                                                        "chat_name": to_user})
        return response
