from django.contrib import admin
from mfa.models import User_Keys as UserKeys


class UserKeysAdmin(admin.ModelAdmin):
    # site_header = "SITE_HEADER"
    # site_title = "SITE_TITLE"
    # index_title = "INDEX_TITLE"
    list_display = [
        "username",
        "properties",
        "added_on",
        "key_type",
        "enabled",
        "expires",
        "last_used",
        "owned_by_enterprise",
    ]


admin.site.register(UserKeys, UserKeysAdmin)
