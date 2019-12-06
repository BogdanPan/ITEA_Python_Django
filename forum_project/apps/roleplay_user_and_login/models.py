# users/models.py
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from .tasks import send_mail_task

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have username')
        if not email:
            raise ValueError('Users must have mail')
        user = self.model(
            username=username,
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(blank=True, max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    def send_user_mail(self, subject, message):
        send_mail_task.delay(subject, message, self.email)

class Project(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    

class Inventory(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    @classmethod
    def get_user_inventorys(cls, user):
        return cls.objects.filter(user=user)

class Item(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    name = models.CharField(max_length=124)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.IntegerField(default=0, blank=True)
    in_stock = models.BooleanField(default=True, blank=True)

    @classmethod
    def get_inventory_items(cls, inventory):
        return cls.objects.filter(inventory=inventory)
    
    def __str__(self):
        return self.name
