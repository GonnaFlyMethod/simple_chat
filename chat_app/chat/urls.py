from django.urls import path

from . import views


app_name = 'chat'

urlpatterns = [
   path('threads/', views.ThreadListView.as_view(), name='thread-list'),
   path('thread/<int:thread_id>/', views.ThreadDetailView.as_view(),
        name='thread-detail'),
]
