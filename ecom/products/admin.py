from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Category)
admin.site.register(Coupon)
class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price', 'has_size')  # Display has_size in the list view
    list_editable = ('has_size',)  # Make has_size editable in the list view
    search_fields = ('product_name', 'category__category_name')    
    list_filter = ('category', 'has_size')
    inlines = [ProductImageAdmin]



@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'price']
    model = ColorVariant
@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price']
    model = SizeVariant


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
