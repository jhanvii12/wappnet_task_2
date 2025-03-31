from django.urls import path, include
from .views import ResourceAllocationViewSet
from rest_framework.routers import DefaultRouter

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'resource-allocations', ResourceAllocationViewSet, basename='resource-allocation')

urlpatterns = [
    path('', include(router.urls)),
    path('resource-allocations/', ResourceAllocationViewSet.as_view({'get': 'list', 'post': 'create'}), name='resource-allocation-list-create'),
    path('resource-allocations/<int:pk>/', ResourceAllocationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='resource-allocation-detail'),
    path('resource-allocations/summary/', ResourceAllocationViewSet.as_view({'get': 'summary'}), name='resource-summary'),
]