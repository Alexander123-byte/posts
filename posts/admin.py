from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(BaseUserAdmin):
    # Указываем поля, которые будут отображаться в списке пользователей
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active')

    # Указываем поля для фильтрации в интерфейсе администрирования
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    # Указываем, какие поля будут доступны для редактирования
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # Указываем поля для отображения при создании пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')}
         ),
    )

    form = UserChangeForm
    add_form = UserCreationForm

    # Обновляем поле ordering
    ordering = ('email',)  # Заменяем 'username' на 'email' или любое другое поле, которое есть в вашей модели


admin.site.register(User, UserAdmin)
