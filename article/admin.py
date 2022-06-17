from django.contrib import admin

from .models import article,Comment

# Register your models here.

admin.site.register(Comment)

@admin.register(article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ["title","author","created_date"]

    list_display_links = ["title","created_date"]

    search_fields = ["title"]

    list_filter = ["created_date"]

    prepopulated_fields = {'slug':('title',)} 

    class Meta:
        model = article

