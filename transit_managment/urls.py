from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'transit_managment'

router = DefaultRouter()
router.register('statuses', views.StatusViewSet)
router.register('transaction-types', views.TransactionTypeViewSet)
router.register('categories', views.CategoryViewSet)
router.register('transactions', views.TransactionViewSet)

urlpatterns = [
    path('backend/api/', include(router.urls)),
    path('', views.home, name='home'),
    path('transaction/create/', views.transaction_create, name='transaction_create'),
    path('transaction/<int:pk>/edit/', views.transaction_edit, name='transaction_edit'),
    path(
        'transaction/<int:pk>/delete/',
        views.transaction_delete,
        name='transaction_delete',
    ),
    path('reference-management/', views.reference_management, name='reference_management'),
    path(
        'ajax/categories-by-type/',
        views.get_categories_by_type,
        name='categories_by_type',
    ),
]
