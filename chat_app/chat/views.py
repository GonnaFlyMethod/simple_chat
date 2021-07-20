from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseForbidden

from .models import Thread, ChatMessage


class ThreadListView(View):
	
	def get(self, request):
		context = {

			'thread_list': Thread.objects.all(),
		}

		return render(request, 'chat/thread_list.html', context)


class ThreadDetailView(View):

	def get(self, request, thread_id):

		thread_obj = get_object_or_404(Thread, pk=thread_id)
		thread_messages = ChatMessage.objects.filter(thread_id=thread_id)

		context = {
			'thread_obj': thread_obj,
			'thread_messages': thread_messages,
		}

		return render(request, 'chat/thread_detail.html',context)

	def post(self, request, thread_id):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()

		current_user_id = request.user.id
		message = request.POST.get('message')
		is_anonymous = request.POST.get('is_anonymous_message')