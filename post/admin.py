from django.contrib import admin
from post.models import Post, Tag, Stream

# Register your models here.
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Stream)
