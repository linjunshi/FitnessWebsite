from django.contrib import admin
from .models import UserAccounts, FitnessVideo


class UserAccountsAdmin(admin.ModelAdmin):
    list_display = ('username', )


class FitnessVideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_date', 'update_date', )

admin.site.register(FitnessVideo, FitnessVideoAdmin)
admin.site.register(UserAccounts, UserAccountsAdmin)

#admin.site.register(Chat)
