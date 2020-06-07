from django.db import models
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
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
        user.save(using=self._db)
        return user

    def create_employee(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = False
        user.is_staff = True
        user.is_superuser = False
        user.is_employee = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_employee = True
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
    """ Station Specific """
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=50, null=False)
    is_employee = models.BooleanField(default=False, null=False)

    def books(self):
        data = Transaction.objects.filter(user=self, is_active=True)
        return data

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

    def __str__(self):
        return self.title


class Transaction(models.Model):

    TRANSACTIONS = [
        ('lending', 'Lending a book'),
        ('renewal', 'Renewing a book')
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=TRANSACTIONS)
    is_active = models.BooleanField(default=True)

    def due_date(self):
        if self.type == 'lending':
            d = timedelta(days=30)
        elif self.type == 'renewal':
            d = timedelta(days=15)
        return self.data+d

    def __str__(self):
        return self.date

