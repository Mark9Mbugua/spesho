from django.contrib import admin
from .models import *

class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(Store)

