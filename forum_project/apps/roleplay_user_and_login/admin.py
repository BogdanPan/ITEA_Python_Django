from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import MyUser


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm

    list_display = ('username', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('username', 'password', )}),

        ('Permissions', {'fields': ('is_admin',)}),
    )

    search_fields = ('username', )
    ordering = ('username', )

    filter_horizontal = ()


admin.site.unregister(MyUser)
admin.site.register(MyUser, CustomUserAdmin)
