from django.contrib import admin
from .models import TextileBale

class TextileBaleAdmin(admin.ModelAdmin):
    list_display = ('bale_id', 'waste_type', 'weight', 'price', 'upload_date', 'is_verified', 'posted_by')
    search_fields = ('waste_type', 'posted_by__username')
    list_filter = ('upload_date', 'is_verified', 'trader')

admin.site.register(TextileBale, TextileBaleAdmin)
