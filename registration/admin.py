from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import ActivationCode


class ActivationCodeInline(admin.TabularInline):
    model = ActivationCode
    fieldsets = [
        (None, {
            'fields': ['code', 'date', 'is_expired'],
        }),
    ]
    readonly_fields = ['date', 'is_expired']

    def is_expired(self, obj):
        return obj.is_expired()

    is_expired.boolean = True
    is_expired.short_description = 'Expired' 

    can_delete = False
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = [ActivationCodeInline,]


class ActivationCodeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['code', 'user', 'date', 'is_expired'],
        }),
    ]
    readonly_fields = ['date', 'is_expired']

    def is_expired(self, obj):
        return obj.is_expired()

    is_expired.boolean = True
    is_expired.short_description = 'Expired' 

    list_display = ['code', 'user', 'date', 'is_expired']
    list_filter = ['date']


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(ActivationCode, ActivationCodeAdmin)
