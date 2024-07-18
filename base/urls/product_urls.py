from django.urls import path
from base.views import product_views as views
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
# )

urlpatterns = [
    path('',views.getProducts,name="products"),
    path('upload/',views.uploadImage,name="upload_image"),
    path('<str:pk>/reviews/',views.createProductReview,name="create_review"),
    path('top/',views.getTopProducts,name="top_products"),
    path('<str:pk>',views.getSingle,name="singleproduct"),
    path('create/',views.createProduct,name="create-product"),
    path('update/<str:pk>/',views.updateProduct,name="update-product"),
    path('delete/<str:pk>',views.deleteProduct,name="delete-product"),
    
]
