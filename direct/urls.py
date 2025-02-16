from django.urls import path
from direct.views import (
    inbox, directs, send_direct, user_search, new_conversation
)

urlpatterns = [
    path('', inbox, name='inbox'),
    path('directs/<str:username>/', directs, name='directs'),
    path('search/', user_search, name='usersearch'),
    path('new/<str:username>/', new_conversation, name='newconversation'),
    path('send/', send_direct, name='send_direct'),
]