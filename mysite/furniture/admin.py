from django.contrib import admin
from .models import Furniture, FurnitureImage, Order

class FurnitureImageInline(admin.TabularInline):
    model = FurnitureImage
    extra = 1
    ordering = ['order']

@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('furniture_id', 'name', 'category', 'price', 'created_at')
    list_filter = ('category',)
    search_fields = ('furniture_id', 'name')
    inlines = [FurnitureImageInline]
    readonly_fields = ('furniture_id',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone_number', 'furniture', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'phone_number', 'furniture__name')
    readonly_fields = ('created_at',)
    list_editable = ('status',)

