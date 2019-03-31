from django.shortcuts import render, HttpResponse
from .models import Thread, ChatMessage
from .forms import MessageCreateForm
# Create your views here.

def thread_list_view(request):
	object_list = Thread.objects.all()
	return render(request, 'thread_list.html', {'object_list': object_list})



def message_view(request, *args, **kwargs):
	other_username = kwargs.get('username')
	print(other_username)
	user = request.user
	try:
		obj , is_created = Thread.objects.get_or_new(user, other_username)
	except Exception as e:
		print(e)
		return HttpResponse('one value is returned only{e}')
	if obj == None:
		return HttpResponse('thread object is None ')

	if request.method == 'POST':
		form = MessageCreateForm(request.POST)
		if form.is_valid():
			message_instance = form.save(commit=False)
			message_instance.thread  = obj
			message_instance.user = request.user
			message_instance.save()

	else:
		form = MessageCreateForm()

	message_list = ChatMessage.objects.filter(thread = obj)
	return render(request, 'message.html', {'thread_obj': obj , 
												'message_list':message_list, 
												 'other_username': other_username,
												 'form': form
												 })



