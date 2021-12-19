from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Product, Category, Tag, Manufacturer
from django.utils.text import slugify
from .forms import CommentForm


def new_comment(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.product = product
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(product.get_absolute_url())
    else:
        raise PermissionDenied


class ProductCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    fields = ['title', 'price', 'name', 'hook_text', 'content', 'head_image', 'open_at', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(ProductCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/shop/')


class ProductUpdate(LoginRequiredMixin, UpdateView):  # 모델명_form
    model = Product
    fields = ['title', 'price', 'name', 'hook_text', 'content', 'head_image', 'open_at', 'category']

    template_name = 'shop/product_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ProductUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)

        return context

    def form_valid(self, form):
        response = super(ProductUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response


# CBV 형식, 파라미터로 listview를 전달 받음
# Create your views here.
class ProductList(ListView):
    model = Product
    ordering = '-pk'  # pk의 역순으로 나열
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_product_count'] = Product.objects.filter(category=None).count()
        return context


#    template_name = 'blog/product_list.html'
# product_list.html, 자동으로 인식하는 방법을 사용해서 주석 처리


class ProductDetail(DetailView):  # 디테일뷰는 디테일리스트
    model = Product

    # product_detail.html, 자동으로 인식하는 방법을 사용해서 주석 처리

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_product_count'] = Product.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context


class ProductSearch(ProductList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        product_list = Product.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return product_list

    def get_context_data(self, **kwargs):
        context = super(ProductSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q}({self.get_queryset().count()})'

        return context


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


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    product_list = tag.product_set.all()

    return render(request, 'shop/product_list.html',
                  {
                      'product_list': product_list,
                      'categories': Category.objects.all(),
                      'no_category_post_count': Product.objects.filter(category=None).count(),
                      'tag': tag
                  })

# def index(request):
#     posts = Post.objects.all().order_by('-pk') # pk의 역순
#
#     return render(request, 'blog/product_list.html',
#                   {
#                       'posts': posts
#                   })
#
#
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(request, 'blog/product_detail.html',
#                   {
#                       'post': post
#                   })
