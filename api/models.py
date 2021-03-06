
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.fields import CharField
from django.db.models.manager import Manager

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user


    def create_superuser(self,username, email, password):
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user
        
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, unique=False,default='')
    last_name = models.CharField(max_length=255, unique=False, default='')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def get_full_name(self):
        return self.username


    
    def __str__(self):
        return self.username
        
    def has_perm(self, perm, obj=None):
       return self.is_admin

    def has_module_perms(self, app_label):
       return self.is_admin


class Post(models.Model):
    Username=models.ForeignKey(User,on_delete=models.CASCADE,default='1')
    name=models.CharField(max_length=55)
    name_result=models.BooleanField(default=False)
    text=models.CharField(max_length=500)
    text_result=models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Result(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    chk=models.BooleanField(max_length=24,default=False)