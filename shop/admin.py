from django.contrib import admin
from .models import Product, Category, Tag, Comment, Manufacturer
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
admin.site.register(Product, MarkdownxModelAdmin) #admin Post 모델 추가
admin.site.register(Comment)
admin.site.register(Manufacturer)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)

