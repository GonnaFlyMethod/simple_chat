from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='thread_creator')
	thread_name = models.CharField("The name of thread", max_length=120)
	timestamp = models.DateTimeField(auto_now_add=True)

	
	def __str__(self):
		string = f"Thread: {self.thread_name},\
		User: {self.creator.username}"
		return string


class ChatMessage(models.Model):
    thread_id = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name='sender',
    	                        on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
    	if len(self.message) > 10:
    		msg = f"{self.message[:11]} ..."
    	else:
    		msg = self.message

    	string = f"Thread: {self.thread_id.thread_name},\
    	Message: {msg}, User: {self.user_id.username}"