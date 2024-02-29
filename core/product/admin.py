from django.contrib import admin
from .models import Product, Lesson, Group, StudentInGroup


class StudentInGroupInline(admin.TabularInline):
    model = StudentInGroup
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = [StudentInGroupInline]
