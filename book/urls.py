from django.urls import include
from rest_framework import routers
from .views import BooksViewSet
from django.urls import path


router = routers.DefaultRouter()
router.register('', BooksViewSet, basename="Transactions")

urlpatterns = [
    path('', include(router.urls))
]
