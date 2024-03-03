from django.urls import path
from rest_framework.routers import DefaultRouter

from edu.apps import EduConfig
from edu.views import LessonViewSet, ProductViewSet, GroupViewSet

app_name = EduConfig.name


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'lessons', LessonViewSet, basename='lessons')
router.register(r'groups', GroupViewSet, basename='groups')

urlpatterns = [
    path('products/<int:product_id>/lessons/', LessonViewSet.as_view({'get': 'list'}), name='product-lessons'),
]

urlpatterns += router.urls
