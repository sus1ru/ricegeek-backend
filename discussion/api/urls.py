from django.urls import path
from discussion.api.views import Discussion, DiscussionGroupDetail,MessageCreate,MessageList



urlpatterns = [
    path('list/', Discussion.as_view(), name='discussion-list'),
    path('<int:pk>/', DiscussionGroupDetail.as_view(), name='discussion-detail'),
    path('<int:pk>/message-create/', MessageCreate.as_view(), name='message-create'),
    path('<int:pk>/messages/', MessageList.as_view(), name='message-list'),

 
] 