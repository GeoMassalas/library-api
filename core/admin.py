from django.contrib import admin
from .models import User, Transaction, Book

# Register your models here.
admin.site.register(Book)
admin.site.register(Transaction)
admin.site.register(User)
