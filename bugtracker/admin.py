from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from bugtracker.models import MyUser, Ticket
# Register your models here.

class MyUserAdmin(UserAdmin):
    list_display = ('username', 'display_name', 'is_staff', 'is_active',)
    list_filter = ('username', 'display_name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'display_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {"slug":("title",)}



admin.site.register(MyUser, UserAdmin)
admin.site.register(Ticket, TicketAdmin)