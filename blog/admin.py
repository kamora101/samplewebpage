from django.contrib import admin

from  .models import Post,Author

class PostAdmin(admin.ModelAdmin):
  list_display= ("title", "created_on","id")

class AuthorAdmin(admin.ModelAdmin):
  list_display = ("name", "updated_on", "user_id")
  


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)

# Register your models here.

