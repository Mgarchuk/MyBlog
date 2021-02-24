from django.contrib import admin
from .models import Post, Photo, Comment, Post_Image

admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Post_Image)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'published_date', 'status')
    list_filter = ('status', 'published_date')
    search_fields = ('author', 'text')


admin.site.register(Comment, CommentAdmin)
