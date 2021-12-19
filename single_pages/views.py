from shop.models import Product, Comment, Category
from django.shortcuts import render
from django.http import HttpResponse


# FBV 방식
# Create your views here.
def landing(request):
    recent_products = Product.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html',
                  {'recent_products': recent_products})     # 앱 이름/html 주소
    # render 함수 리턴, 뒤에는 template에 있는 경로 작성


def about_me(request):
    return render(request, 'single_pages/about_me.html',
                  {
                      'categories': Category.objects.all()
                  })


def my_page(request):
    comment = Comment.objects.filter(author=request.user)
    return render(request, 'single_pages/my_page.html',
                  {'comment': comment})


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        product_list = Product.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        product_list = Product.objects.filter(category=category)

    return render(request, 'shop/product_list.html',
                  {
                      'product_list': product_list,
                      'categories': Category.objects.all(),
                      'no_category_product_count': Product.objects.filter(category=None).count(),
                      'category': category
                  })

