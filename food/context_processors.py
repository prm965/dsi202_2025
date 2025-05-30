from .models import CartItem

def cart_context(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total = sum(item.get_total_price() for item in cart_items)
        return {
            'cart_items': cart_items,
            'total_cart_price': total
        }
    return {}

def cart_count(request):
    cart = request.session.get('cart', {})
    total_quantity = sum(item['quantity'] for item in cart.values())  # รวมจำนวนสินค้าทั้งหมดในตะกร้า
    return {'cart_count': total_quantity}

