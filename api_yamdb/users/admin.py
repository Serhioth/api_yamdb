from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'bio'
                    )
    list_editable = ('bio', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    list_filter = ('last_name', 'email')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
