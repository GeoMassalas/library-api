from django.urls import path, include
from rest_framework import routers
from .views import TransactionViewSet

router = routers.DefaultRouter()
router.register('', TransactionViewSet, basename="Register Station")

urlpatterns = [
    path('', include(router.urls))
]
