from django.urls import path
from . import views


urlpatterns = [
    path('search/<str:q>/', views.ProductSearch.as_view()),
    path('update_product/<int:pk>/', views.ProductUpdate.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('create_product/', views.ProductCreate.as_view()),
    path('tag/<str:slug>', views.tag_page),
    path('category/<str:slug>', views.category_page),
    path('<int:pk>/', views.ProductDetail.as_view()),  # 뒤에 blog+번호, CBV의 경우엔 class 이름 + as_view()
    path('', views.ProductList.as_view()),     # 뒤에 blog만 붙이면 됨
]
# python manage.py startapp ??? 무슨 무슨 앱