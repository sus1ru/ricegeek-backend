import base64
import json
from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from discussion.api.serializers import DiscussionGroupSerializer,MessageSerializer
from discussion.models import DiscussionGroup,Message
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
# from rest_framework.pagination import LimitOffsetPagination

from rest_framework.decorators import api_view

# @login_required(login_url='/accounts/login/')
# @api_view(['GET',]) 
# def get_user_date(request):
#         profile = request.user.get_profile()
#         return Response(profile, status=status.HTTP_201_CREATED)



class Discussion(APIView):
    def get(self, request):
        discussion = DiscussionGroup.objects.all()

        # results = self.paginate_queryset(discussion, request, view=self)
        serializer = DiscussionGroupSerializer(
        discussion, many=True, context={'request': request})
        # return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @method_decorator(login_required) 
    def post(self, request):
        serializer = DiscussionGroupSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class DiscussionGroupDetail(APIView):

    def get(self, request, pk):
        try:
            platform = DiscussionGroup.objects.get(pk=pk)
        except DiscussionGroup.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DiscussionGroupSerializer(
            platform, context={'request': request})
        print(serializer)
        return Response(serializer.data)

    def put(self, request, pk):
        platform = DiscussionGroup.objects.get(pk=pk)
        serializer = DiscussionGroupSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = DiscussionGroup.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class MessageCreate(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  
        return Message.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk') 
        group = DiscussionGroup.objects.get(pk=pk)
        group.save()
        serializer.save(group=group)

class MessageList(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Message.objects.filter(group=pk)

# class Message(APIView):
#     permission_classes = (IsAuthenticated,)
#     def get(self, request):

#         discussion = Message.objects.all()
#         serializer = MessageSerializer(
#         discussion, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
        
#         serializer = MessageSerializer(data=request.data)
#         print(serializer)
#         print(request.user)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)




        # token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        # print(token)
        # print("This is for usrname")
        # token = token.replace("Token ", "")
        # user_json = json.loads(base64.b64decode(token.split(".")[1]))
        # print(user_json)
        # user_id = user_json['user_id']
        # User = get_user_model()
        # user_obj = User.objects.get(id=user_id)
        # print(user_obj)