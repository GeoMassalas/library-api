from datetime import timedelta
import uuid
import os
from barcode import EAN8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from core.helpers import generate_password


def generate_barcode(_id):
    """ Generate file path for new image """
    string = '0'*(8-len(_id)) + _id
    ean = EAN8(string)
    string += '.svg'
    fp = os.path.join('media/barcodes/', string)
    f = open(fp, 'wb')
    ean.write(f)

    return os.path.join('barcodes/', string)


def book_image_file_path(instance, filename):
    """ Generate file path for new image """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    print(filename)
    return os.path.join('book_imgs/', filename)


class UserManager(BaseUserManager):
    """ User Manager Class"""
    def create_user(self, email, username, password, first_name, last_name, address, phone):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not address:
            raise ValueError("Users must have an address")
        if not phone:
            raise ValueError("Users must have a phone number")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone,
            is_employee=False,
        )
        user.set_password(password)
        message = 'Your account information is:\nEmail: ' + user.email + '\nPassword: ' + password
        send_mail(
            'Welcome to Library of ...',
            message,
            'geomassalas@gmail.com',
            [user.email],
            fail_silently=False,
        )
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name='Admin',
            last_name='Admin',
            address='Admin',
            phone='0000000000',
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_employee = True
        user.is_manager = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=35, unique=True)
    """ User Specific """
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=10, null=False)
    is_employee = models.BooleanField(default=False, null=False)
    is_manager = models.BooleanField(default=False, null=False)

#    def books(self):
#        data = Transaction.objects.filter(user=self, is_active=True)
#        return data

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username


class Book(models.Model):

    title = models.CharField(max_length=100, null=False)
    author = models.CharField(max_length=40, null=False)
    isbn = models.CharField(max_length=10, null=False)
    isbn13 = models.CharField(max_length=14, null=True)
    description = models.TextField()
    category1 = models.CharField(max_length=25, null=False)
    category2 = models.CharField(max_length=25, null=True)
    category3 = models.CharField(max_length=25, null=True)
    barcode = models.FileField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to=book_image_file_path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.barcode = generate_barcode(str(self.id))

    def __str__(self):
        return self.title


class Transaction(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    renewals = models.SmallIntegerField(default=0)

    def due_date(self):
        return self.date + timedelta(days=30+self.renewals*15)

    def __str__(self):
        return str(self.due_date()) + " - " + str(self.book) + " - " + str(self.user)
