from django.urls import path
from .views import message_view, thread_list_view

urlpatterns = [
	path('<slug:username>/', message_view, name='message'),
]