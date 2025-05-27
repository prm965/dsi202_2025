from django.db import models
from django.contrib.auth.models import User

# -------------------
# 1. Address
# -------------------

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100)
    house_number = models.CharField(max_length=100)
    sub_district = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)


# -------------------
# 2. Allergen
# -------------------

class Allergen(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Allergens"


# -------------------
# 3. FoodCategory
# -------------------

class FoodCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "FoodCategory"


# -------------------
# 4. Restaurant
# -------------------

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='restaurants/')
    open_time = models.TimeField()
    close_time = models.TimeField()
    google_maps_url = models.URLField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Restaurants"


# -------------------
# 5. MenuItem
# -------------------

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    discount_percent = models.PositiveIntegerField(default=0)
    final_price = models.FloatField(blank=True, null=True)
    allergens = models.ManyToManyField(Allergen, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='menu/')

    def save(self, *args, **kwargs):
        self.final_price = self.price * (100 - self.discount_percent) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

    class Meta:
        verbose_name_plural = "Menu items"


# -------------------
# 6. CartItem
# -------------------

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.menu_item.final_price * self.quantity

    class Meta:
        verbose_name_plural = "Cart items"


# -------------------
# 7. Order & OrderItem
# -------------------

import uuid

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True, editable=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD{uuid.uuid4().hex[:10].upper()}"  # สร้างรหัสคำสั่งซื้อแบบสุ่ม
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number} by {self.user.username}"

    class Meta:
        verbose_name_plural = "Orders"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()  # snapshot final price

    def get_total_price(self):
        return self.price * self.quantity

    class Meta:
        verbose_name_plural = "Order items"

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(max_length=100, default='profile/avatar1.png')  # default png

    def __str__(self):
        return f"{self.user.username} Profile"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)



