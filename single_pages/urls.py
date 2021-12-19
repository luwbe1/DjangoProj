from django.urls import path
from . import views


urlpatterns = [  # 서버 IP/
    path('', views.landing),  # 서버IP/ 주소 뒤에 아무것도 없다.
    path('about_me/', views.about_me),  # 서버IP/about_me/ view에 있는 about_me를 호출하겠다.
    path('my_page/', views.my_page)
]
