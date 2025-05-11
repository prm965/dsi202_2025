from django.contrib import admin
from .models import Restaurant, MenuItem, Allergen, CartItem, Order, OrderItem, FoodCategory
import re
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

admin.site.register(User)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude']
    readonly_fields = ['map_preview']  # แสดง preview
    fields = ['name', 'google_maps_url', 'latitude', 'longitude', 'open_time', 'close_time', 'image', 'rating', 'map_preview']  # เปลี่ยนจาก 'map_url' เป็น 'google_maps_url'

    def save_model(self, request, obj, form, change):
        if obj.google_maps_url:  # เปลี่ยนจาก 'map_url' เป็น 'google_maps_url'
            match = re.search(r'@([-.\d]+),([-.\d]+)', obj.google_maps_url)  # เปลี่ยนจาก 'map_url' เป็น 'google_maps_url'
            if match:
                obj.latitude = float(match.group(1))
                obj.longitude = float(match.group(2))
        super().save_model(request, obj, form, change)

    def map_preview(self, obj):
        if obj.google_maps_url:  # เปลี่ยนจาก 'map_url' เป็น 'google_maps_url'
            return mark_safe(f'<iframe width="100%" height="300" frameborder="0" src="{obj.google_maps_url}&output=embed"></iframe>')
        elif obj.latitude and obj.longitude:
            embed_url = f"https://maps.google.com/maps?q={obj.latitude},{obj.longitude}&hl=th&z=15&output=embed"
            return mark_safe(f'<iframe width="100%" height="300" frameborder="0" src="{embed_url}"></iframe>')
        return "ยังไม่มีพิกัด"
    map_preview.short_description = "พรีวิวแผนที่"

@admin.register(MenuItem)  # ลงทะเบียนเพียงครั้งเดียว
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'category', 'price', 'final_price']
    list_filter = ['category', 'restaurant']
    search_fields = ['name']
    fields = ['restaurant', 'category', 'name', 'price', 'discount_percent', 'final_price', 'allergens', 'description', 'image']

@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']  # จะแสดงชื่อประเภทอาหารใน Admin
    search_fields = ['name'] 
    
# Register other models
admin.site.register(Allergen)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
