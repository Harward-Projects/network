from django.contrib import admin

# from django.contrib.auth.admin import UserAdmin


# Register models
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["content", "creation_date"]


# if wanting to show M2M's related fields or properties of M2M's related fields in the list_display attribute. For ManyToMany fields, you can display related fields using a method on the admin model class.
# Here's an example:
# from django.contrib import admin
# from .models import Post

# class PostAdmin(admin.ModelAdmin):
#     list_display = ('author', 'content', 'get_likes_count')

#     def get_likes_count(self, obj):
#         return obj.likes.count()

#     get_likes_count.short_description = 'Likes Count'

# admin.site.register(Post, PostAdmin)
