from django.contrib import admin
from .models import News
from .utils import refill_news
# Register your models here.


@admin.register(News)
class MyModelAdmin(admin.ModelAdmin):
    actions = ['refill_news']

    def refill_news(self, request, queryset):
        self.model.objects.all().delete()
        refill_news()
        self.message_user(request, "News are updated successfuly.")
    refill_news.short_description = "Clear and Refill News"
