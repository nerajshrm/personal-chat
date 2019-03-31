from django import forms
from .models import ChatMessage



class MessageCreateForm(forms.ModelForm):
	class Meta:
		model = ChatMessage
		fields = ['message']