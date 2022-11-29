from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import Permission,Group,UserManager

# ///////////////model managers/////////////
class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        super_instance : User = super().create_superuser(username, email, password, **extra_fields)
        admin_group : Group = Group.objects.get(name='admin');
        super_instance.groups.add(admin_group);
        return super_instance;


class Role(models.Model):
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(Permission)
    def __str__(self):
        return self.name


class User(AbstractUser):
    # user_image=models.ImageFiled(upload_to='')
    objects = CustomUserManager()
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    # role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    user_image = models.CharField(max_length=250, null=True)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.email


class token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_token = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.user_token

class User_activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, editable=False)
    activity = models.CharField(null=True, max_length=50, blank=True)

    def __str__(self):
        return str(self.date) + str(self.user)
