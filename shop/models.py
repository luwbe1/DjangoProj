from django.db import models
from django.contrib.auth.models import User
import os
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.


class Manufacturer(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100, null=True)
    phone = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/tag/{self.slug}'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    title = models.CharField(max_length=30)     # 30개 글자
    price = models.IntegerField(null=True)
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()

    # 이미지를 저장할 수 있는 ImageField, blank=true면 필수 항목은 아님
    # pip install pillow (이미지 처리를 위한 설치), 이거 하고 makemigrations & migrate
    head_image = models.ImageField(upload_to='shop/images/%Y/%m/%d/', blank=True)   # 디렉터리가 저렇게 형성됨
    file_upload = models.FileField(upload_to='shop/files/%Y/%m/%d/', blank=True)    # 파일 필드라 이미지랑 크게 다르지 않음

    created_at = models.DateTimeField(auto_now_add=True)    # 새로 작성했을 때 생성
    open_at = models.DateTimeField(auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)    # 수정했을 때 업데이트

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    tags = models.ManyToManyField(Tag, blank=True)

    name = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'
    # 해당 포스트의 pk 값, 해당 포스트의 title 값 앞에 pk와 title로 바뀐다.

    def get_absolute_url(self):     # 고유 url 부여하기
        return f'/shop/{self.pk}/'   # int 타입에 해당하는 primary key를 넣어주면 됨

    def get_content_markdown(self):
        return markdown(self.content)

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://doitdjango.com/avatar/id/421/f684407a17bf5022/svg/{self.author.email}/'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.product.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://doitdjango.com/avatar/id/421/f684407a17bf5022/svg/{self.author.email}/'
