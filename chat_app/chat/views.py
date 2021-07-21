from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseForbidden

from .models import Thread, ChatMessage


class ThreadListView(View):
	
	def get(self, request):
		context = {

			'thread_list': Thread.objects.all(),
		}

		return render(request, 'chat/thread_list.html', context)

	def post(self, request):
		current_user = request.user
		thread_name = request.POST.get('thread_name')

		new_thread = Thread.objects.create(
			creator=current_user,
			thread_name=thread_name
		)

		return redirect('chat:thread-detail', thread_id=new_thread.id)


class ThreadDetailView(View):

	def get(self, request, thread_id):

		thread_obj = get_object_or_404(Thread, pk=thread_id)
		thread_messages = ChatMessage.objects.filter(thread_id=thread_id)

		context = {
			'thread_obj': thread_obj,
			'thread_messages': thread_messages,
		}

		return render(request, 'chat/thread_detail.html',context)
