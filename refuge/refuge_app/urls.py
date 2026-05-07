from django.urls import path

from .views import (
    ChatsDisponiblesProxyView,
    PrendreChatView,
    RefugeCatListView,
    prendre_chat_web,
)

urlpatterns = [
    path("chats-disponibles/", ChatsDisponiblesProxyView.as_view(), name="chats-disponibles"),
    path("refuge-cats/", RefugeCatListView.as_view(), name="refuge-cats"),
    path("chats/<int:cat_id>/prendre-en-charge/", PrendreChatView.as_view(), name="prendre-chat"),
    path("chats/<int:cat_id>/prendre-en-charge-web/", prendre_chat_web, name="prendre-chat-web"),
]
