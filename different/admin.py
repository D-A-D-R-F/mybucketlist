from django.contrib import admin

from .models import User , Bucket_List , Connect_Users , Shared_Items

admin.site.register(User)
admin.site.register(Bucket_List)
admin.site.register(Connect_Users)
admin.site.register(Shared_Items)