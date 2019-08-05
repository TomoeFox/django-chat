from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.index), name='chat'),
    path('<room_name>/', login_required(views.RoomView.as_view()), name='room'),
    path('pr/<username>/', login_required(views.PrivateRoomView.as_view()), name='private')
]
