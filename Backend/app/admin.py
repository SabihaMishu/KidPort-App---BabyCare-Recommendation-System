from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app.models.user import User
from app.models.invitation import Invitation

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'role', 'terms_accepted', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'terms_accepted', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'role', 'terms_accepted')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('token', 'invited_by', 'role_offered', 'email', 'status', 'created_at', 'expires_at')
    list_filter = ('role_offered', 'status', 'created_at')
    search_fields = ('email', 'invited_by__email', 'invited_by__full_name', 'token')
    readonly_fields = ('token', 'created_at')

admin.site.register(User, UserAdmin)
admin.site.register(Invitation, InvitationAdmin)
