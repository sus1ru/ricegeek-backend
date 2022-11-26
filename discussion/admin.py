from django.contrib import admin

from discussion.models import DiscussionGroup, Message

# Register your models here.

admin.site.register(DiscussionGroup)
admin.site.register(Message)