from django.urls import path, re_path

from . import views


app_name = 'chat'

urlpatterns = [
   path('threads/', views.ThreadListView.as_view(), name='thread-list'),
   path('thread/<int:thread_id>/', views.ThreadDetailView.as_view(),
        name='thread-detail'),
]

rest_api_urls = [
   re_path(r'^api/get-messages/(?P<thread_id>[0-9]+)/$',
           views.ChatMessageListing.as_view(), name='thread-messages-api'), 
]


urlpatterns += rest_api_urls
