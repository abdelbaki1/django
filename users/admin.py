from django.contrib import admin
from .models import Role,  User, token, User_activity
from django.contrib.contenttypes.models import ContentType as CT
from django.contrib.auth.models import Permission



# admin.site.register(Role)
admin.site.register(User)
admin.site.register(User_activity)
admin.site.register(token)
admin.site.register(CT)
admin.site.register(Permission)


# Register your models here.
