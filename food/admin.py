from django.contrib import admin
from .models import Restaurant, MenuItem, Allergen, CartItem, Order, OrderItem
import re
from django.utils.safestring import mark_safe

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude']
    readonly_fields = ['map_preview']  # ✅ แสดง preview
    fields = ['name', 'map_url', 'latitude', 'longitude', 'open_time', 'close_time', 'image', 'rating', 'map_preview']

    def save_model(self, request, obj, form, change):
        if obj.map_url:
            match = re.search(r'@([-.\d]+),([-.\d]+)', obj.map_url)
            if match:
                obj.latitude = float(match.group(1))
                obj.longitude = float(match.group(2))
        super().save_model(request, obj, form, change)

    def map_preview(self, obj):
        if obj.latitude and obj.longitude:
            embed_url = f"https://maps.google.com/maps?q={obj.latitude},{obj.longitude}&hl=th&z=15&output=embed"
            return mark_safe(f'<iframe width="100%" height="300" frameborder="0" src="{embed_url}"></iframe>')
        return "ยังไม่มีพิกัด"
    map_preview.short_description = "พรีวิวแผนที่"

# Register others
admin.site.register(MenuItem)
admin.site.register(Allergen)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
