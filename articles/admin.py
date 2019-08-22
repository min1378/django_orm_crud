from django.contrib import admin
from .models import Article



class ArticleAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'content', 'create_at', 'update_at',)
# Register your models here.
admin.site.register(Article)



