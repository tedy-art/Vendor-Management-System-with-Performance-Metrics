from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from core import views

urlpatterns = [
    # Obtain authentication token
    path('token/', obtain_auth_token, name='api_token_auth'),

    # Vendor endpoints
    path('vendors/', views.vendor_list_create),
    path('vendors/<int:pk>/', views.vendor_retrieve),
    path('vendors/<int:pk>/update/', views.vendor_update),
    path('vendors/<int:pk>/delete/', views.vendor_delete),
    path('vendors/<int:vendor_id>/performance/', views.vendor_performance),

    # Purchase Order endpoints
    path('purchase_orders/', views.purchase_order_list_create),
    path('purchase_orders/<int:pk>/', views.purchase_order_retrieve),
    path('purchase_orders/<int:pk>/update/', views.purchase_order_update),
    path('purchase_orders/<int:pk>/delete/', views.purchase_order_delete),
    path('purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order),

    # Historical Performance endpoints
    path('historical_performances/', views.historical_performance_list_create),
    path('historical_performances/<int:pk>/', views.historical_performance_retrieve_update_destroy),
    
    # Authentication endpoints
    
]
