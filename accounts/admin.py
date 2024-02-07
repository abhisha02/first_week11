from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,AccountUser,Profile,Address,UserProfile

# Register your models here.
class AccountAdmin(UserAdmin):
  list_display=('email','first_name','last_name','last_login','date_joined','is_active')
  list_display_links=('email','first_name','last_name')
  readonly_fields=('last_login','date_joined')
  ordering=('-date_joined',)

  filter_horizontal=()
  list_filter=()
  fieldsets=()

admin.site.register(Account,AccountAdmin)

class AccountUserAdmin(UserAdmin):
    list_display = ('first_name','last_name', 'email', 'phone_number', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('first_name', 'email', 'phone_number')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(AccountUser, AccountUserAdmin)
admin.site.register(Profile)
admin.site.register(Address)

class UserProfileAdmin(admin.ModelAdmin):
   liat_display=('user','city','state','country')

admin.site.register(UserProfile,UserProfileAdmin)