from django.contrib import admin
from.models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_phone', 'get_total', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_phone']
    readonly_fields = ['created_at']
    ordering = ['-created_at'] # Yeni sifarişlər yuxarıda
    inlines = [OrderItemInline]
    
    class Media:
        js = ('admin/js/order_auto_refresh.js',) # Avto yeniləmə

    def get_total(self, obj):
        return f"{obj.total_amount} AZN"
    get_total.short_description = 'Cəmi'