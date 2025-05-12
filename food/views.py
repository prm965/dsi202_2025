from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant, MenuItem, FoodCategory, CartItem, Address, Order
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
import qrcode

def signin(request):
    return render(request, 'food/signin.html')

@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'food/address.html', {
        'addresses': addresses,
    })

@login_required
def add_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        house_number = request.POST.get('house_number')
        sub_district = request.POST.get('sub_district')
        district = request.POST.get('district')
        province = request.POST.get('province')
        postal_code = request.POST.get('postal_code')

        Address.objects.create(
            user=request.user,
            name=name,
            house_number=house_number,
            sub_district=sub_district,
            district=district,
            province=province,
            postal_code=postal_code,
        )
        return redirect('address')

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "รหัสผ่านไม่ตรงกัน")
            return redirect('signin')

        if User.objects.filter(username=email).exists():
            messages.error(request, "มีผู้ใช้งานนี้ในระบบแล้ว")
            return redirect('signin')

        if not first_name or not last_name:
            messages.error(request, "กรุณากรอกชื่อและนามสกุล")
            return redirect('signin')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        messages.success(request, "สมัครสมาชิกสำเร็จ กรุณาเข้าสู่ระบบ")
        return redirect('signin')

    return redirect('signin')


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "อีเมลหรือรหัสผ่านไม่ถูกต้อง")
            return redirect('signin')

    return redirect('signin')

def service_details(request):
    return render(request, 'service-details.html')

def starter_page(request):
    return render(request, 'starter-page.html')

def signin(request):
    return render(request, 'food/signin.html')


def index(request):
    query = request.GET.get("q", "")
    category_name = request.GET.get('category')

    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query)
    elif category_name:
        category = get_object_or_404(FoodCategory, name=category_name)
        menu_items = MenuItem.objects.filter(category=category)
    else:
        menu_items = MenuItem.objects.all()

    if 'cart' not in request.session:
        request.session['cart'] = {}

    # ✅ อัปเดตการนับจำนวนสินค้าทั้งหมด
    request.session['cart_count'] = sum(item['quantity'] for item in request.session['cart'].values())
    request.session.modified = True

    return render(request, "food/index.html", {
        "menu_items": menu_items,
        "restaurants": Restaurant.objects.all(),
        "cart": request.session.get('cart', {}),
        "cart_count": request.session.get('cart_count', 0)
    })

@login_required
def pay(request):
    # ดึงข้อมูลสินค้าจากตะกร้า
    cart = request.session.get('cart', {})
    
    # คำนวณยอดรวม
    total_price = 0
    for item in cart.values():
        total_price += item['price'] * item['quantity']
    
    # หมายเลขโทรศัพท์ของคุณที่เชื่อมกับ PromptPay
    phone_number = "0922157806"  # หมายเลขพร้อมเพย์ที่คุณใช้งาน
    
    # สร้าง URL สำหรับการใช้ใน promptpay.io
    payment_url = f"https://promptpay.io/{phone_number}/{total_price:.2f}"

    return render(request, 'food/pay.html', {
        'total_price': total_price,
        'qr_code_url': payment_url,  # ส่ง URL สำหรับ QR Code ไปยังเทมเพลต
        'cart_items': cart  # ส่งข้อมูลสินค้าที่อยู่ในตะกร้าไปยังเทมเพลต
    })



@login_required
def home(request):
    query = request.GET.get("q", "")
    category_name = request.GET.get('category')

    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query)
    elif category_name:
        category = get_object_or_404(FoodCategory, name=category_name)
        menu_items = MenuItem.objects.filter(category=category)
    else:
        menu_items = MenuItem.objects.all()

    if 'cart' not in request.session:
        request.session['cart'] = {}

    # ✅ อัปเดตการนับจำนวนสินค้าทั้งหมด
    request.session['cart_count'] = sum(item['quantity'] for item in request.session['cart'].values())
    request.session.modified = True

    # ถ้ามีการส่ง POST มาจากฟอร์มที่เลือกที่อยู่
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')
        if selected_address_id:
            selected_address = Address.objects.get(id=selected_address_id)
            request.session['selected_address'] = selected_address.id  # เก็บที่อยู่ใน session

    # ดึงที่อยู่ที่เลือกจาก session
    selected_address_id = request.session.get('selected_address')
    if selected_address_id:
        selected_address = Address.objects.get(id=selected_address_id)
    else:
        selected_address = None

    return render(request, "food/home.html", {
        "menu_items": menu_items,
        "restaurants": Restaurant.objects.all(),
        "cart": request.session.get('cart', {}),
        "cart_count": request.session.get('cart_count', 0),
        "selected_address": selected_address,  # ส่งที่อยู่ที่เลือก
    })


def get_cart_count(request):
    """
    ฟังก์ชันนี้จะดึงข้อมูลจำนวนสินค้าทั้งหมดในตะกร้า 
    และส่งกลับไปยัง Frontend ในรูปแบบ JSON
    """
    cart = request.session.get('cart', {})
    total_quantity = sum(item['quantity'] for item in cart.values())
    return JsonResponse({'cart_count': total_quantity})

def menu_detail(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    return render(request, "food/menu_detail.html", {"menu_item": menu_item})

@csrf_exempt
def clear_cart(request):
    if request.method == 'POST':
        request.session['cart'] = {}    # ✅ ล้างแค่ตะกร้าเท่านั้น
        request.session['cart_count'] = 0
        request.session.modified = True
        return JsonResponse({'message': 'Cart cleared', 'cart_count': 0})



@csrf_exempt
def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if str(item_id) in cart:
            if action == 'increase':
                cart[str(item_id)]['quantity'] += 1
            elif action == 'decrease':
                if cart[str(item_id)]['quantity'] > 1:
                    cart[str(item_id)]['quantity'] -= 1
                elif cart[str(item_id)]['quantity'] == 1:
                    # จะลบสินค้าออกหากเป็น 1
                    return JsonResponse({
                        'cart_count': sum(item['quantity'] for item in cart.values()),
                        'should_remove': True,
                        'item_id': item_id,
                        'item_name': cart[str(item_id)]['name']
                    })

            # ✅ เขียนกลับเข้า session
            request.session['cart'] = cart
            request.session['cart_count'] = sum(item['quantity'] for item in cart.values())
            request.session.modified = True

            # ส่งข้อมูลกลับไปที่ Frontend
            return JsonResponse({
                'cart_count': request.session['cart_count'],
                'item_quantity': cart[str(item_id)]['quantity'],
                'item_name': cart[str(item_id)]['name'],
                'should_remove': False
            })

    return JsonResponse({'error': 'Item not found'}, status=400)


@csrf_exempt
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if str(item_id) in cart:
            del cart[str(item_id)]
            request.session['cart'] = cart

            # ✅ อัปเดตตัวนับใหม่
            request.session['cart_count'] = sum(item['quantity'] for item in cart.values())
            if len(cart) == 0:
                request.session['cart_count'] = 0

            request.session.modified = True

            return JsonResponse({
                'message': 'Item removed',
                'cart_count': request.session['cart_count']
            })
    return JsonResponse({'error': 'Item not found'}, status=400)

 
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
    request.session['cart_count'] = sum(item['quantity'] for item in cart.values())
    request.session.modified = True

    # รีไดเรกต์กลับไปหน้าแรก
    return redirect('home')

    
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

