from django.urls import path
from chats import views

urlpatterns = [
    path('inbox/', views.InboxListView.as_view({'get': 'list'}), name='inbox'),
    path('messages/<uuid:public_id>/', views.InboxMessageView.as_view({'get': 'list'}),name='inbox_message'),
    path('account/<uuid:public_id>/', views.UserInboxView.as_view({'get': 'retrieve'}),),
    path("contacts/", views.ChatContactsList.as_view(), name="chat_contacts"),
]