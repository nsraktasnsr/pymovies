from django.contrib import admin
from .models import Comment
from .models import Message

# Register your models here.

@admin.register(Comment)

class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user','movie','comment','rating','created_date']
    
    list_display_links = ['user','movie','comment']
    
    search_fields = ['movie']
    
    list_filter = ['created_date']

    class Meta:
        model = Comment


    
@admin.register(Message)

class MessagesAdmin(admin.ModelAdmin):
    list_display = ['email','name','surname','message','created_date']
    
    list_display_links = ['email']
    
    search_fields = ['email']
    
    list_filter = ['created_date']

    class Meta:
        model = Comment