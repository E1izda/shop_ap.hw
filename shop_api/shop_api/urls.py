from django.contrib import admin
from django.urls import path, include
from .import  swagger


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/product/', include('product.urls')), 
    path('api/v1/users/', include('users.urls')), 
    # path('api/v1/categories/', views.category_list_view),
    # path('api/v1/categories/<int:id>/', views.category_detail_view),
    # path('api/v1/products/', views.product_list_view),
    # path('api/v1/products/<int:id>/', views.product_detail_view),
    # path('api/v1/reviews/', views.review_list_view),
    # path('api/v1/reviews/<int:id>/', views.review_detail_view),
    # path('api/v1/products/reviews/', views.products_with_reviews_view),
    # path('api/v1/categories/', views.categories_with_products_count_view),

]

urlpatterns += swagger.urlpatterns
