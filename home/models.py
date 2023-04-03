from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin , BaseUserManager
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.utils.text import slugify
# Create your models here.
class UserManager(BaseUserManager):

    def create_superuser(self, email, name, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('superuser must be assigned to is_staff=True'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('superuser must be assigned to is_staff=True'))

        if extra_fields.get('is_active') is not True:
            raise ValueError(_('superuser must be assigned to is_active=True'))

        return self.create_user(email, name, password, **extra_fields)

    def create_user(self, email, name, password, **extra_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        extra_fields.setdefault('is_active',True)
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_('email address'), unique = True)
    name = models.CharField(max_length = 30)
    address = models.CharField(max_length = 300,blank=True,default="")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    is_worker = models.BooleanField(default=False,null= False,blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects=UserManager()

    def __str__(self):
        return self.email

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name
    
class Service(models.Model):
    title = models.CharField(max_length = 30,null = False,blank=False,unique=True)
    image = models.ImageField(upload_to='category_imgs/',null=False,blank=False,default='category_imgs/default.jpg')
    wage = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False,default=0)
    description = models.TextField(null=False,blank=False,default="We offer the given service")
    slug = models.SlugField(blank=True,null=True,unique=True)

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
            
        super(Service,self).save(*args,**kwargs)

class Worker(models.Model):
    user =  models.OneToOneField ( User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name

class Transactions(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    Service = models.ForeignKey(Service, on_delete=models.CASCADE)

    