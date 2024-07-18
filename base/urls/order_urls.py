from django.urls import path
from base.views import order_views as views
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
# )


urlpatterns = [
    path('',views.getOrders,name="orders"),
    path('add/',views.addOrderItems,name='orders-add'),
    path('myorders/',views.getMyOrders,name='myOrders'),
    path('<str:pk>/deliver/',views.updateOrderToDelivered,name='deliver'),
    path('<str:pk>/',views.getOrderById,name='getOrderById'),
    path('<str:pk>/pay/',views.updateOrderToPaid,name='pay'),
]
