from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Comparison, ProductParameter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

class ProductParameterInline(admin.TabularInline):
    model = ProductParameter
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductParameterInline]    

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Comparison)