from django.contrib import admin

# Register your models here.
from .models import Home, Spouse, NumChild, Luxury
from .models import User

class HomeAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Home Type", {'fields': ['value']})
    ]

admin.site.register(Home)
admin.site.register(Spouse)
admin.site.register(NumChild)
admin.site.register(Luxury)
admin.site.register(User)
