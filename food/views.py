from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant, MenuItem, FoodCategory, CartItem

def home(request):
    query = request.GET.get("q", "")
    category_name = request.GET.get('category')  # รับค่า category จาก URL

    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query)
    elif category_name:
        # กรองเมนูตาม category ที่เลือก
        category = get_object_or_404(FoodCategory, name=category_name)
        menu_items = MenuItem.objects.filter(category=category)
    else:
        # ถ้าไม่มีการค้นหาหรือเลือก category ให้แสดงเมนูทั้งหมด
        menu_items = MenuItem.objects.all()

    # ส่งข้อมูลไปยัง template
    return render(request, "food/home.html", {
        "menu_items": menu_items,
        "restaurants": Restaurant.objects.all(),
        "cart": request.session.get('cart', {})  # ส่งข้อมูลตะกร้าไปยัง template
    })


def menu_detail(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    return render(request, "food/menu_detail.html", {"menu_item": menu_item})

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    
    # รับข้อมูลจำนวนสินค้า (จากฟอร์ม)
    quantity = int(request.POST.get('quantity', 1))  # ใช้ค่าเริ่มต้น 1 หากไม่ระบุ
    
    # ดึงข้อมูลตะกร้าจาก session
    cart = request.session.get('cart', {})
    
    # ถ้าสินค้าอยู่ในตะกร้าแล้ว, เพิ่มจำนวนสินค้า
    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += quantity
    else:
        # ถ้าไม่มี, เพิ่มสินค้าลงในตะกร้าใหม่
        cart[str(item_id)] = {
            'name': item.name,
            'price': item.final_price,
            'quantity': quantity,
            'image': item.image.url,
        }

    # บันทึกข้อมูลตะกร้าใหม่ใน session
    request.session['cart'] = cart

    # รีไดเรกต์กลับไปหน้าแรก
    return redirect('home')


# ฟังก์ชันเพื่อคำนวณจำนวนสินค้าทั้งหมดในตะกร้า
def get_cart_count(request):
    cart = request.session.get('cart', {})
    total_quantity = sum(item['quantity'] for item in cart.values())  # รวมจำนวนทั้งหมด
    return total_quantity

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)
    return render(request, 'food/view_cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def remove_from_cart(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    item.delete()
    return redirect('view_cart')

@login_required
def decrease_quantity(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('view_cart')
