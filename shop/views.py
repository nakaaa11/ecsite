from django.shortcuts import render, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from django.core.mail import send_mail
from django.conf import settings
import stripe
from django.http import JsonResponse

# Create your views here.

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('product_list')
    return render(request, 'shop/logout.html')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    return render(request, 'shop/cart.html', {'cart': cart, 'items': items})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('cart')

@login_required
def remove_from_cart(request, pk):
    cart, created = Cart.objects.get_or_create(user=request.user)
    item = get_object_or_404(CartItem, cart=cart, pk=pk)
    item.delete()
    return redirect('cart')

@login_required
def order_create(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    if not items:
        return redirect('cart')
    total = sum(item.product.price * item.quantity for item in items)
    order = Order.objects.create(user=request.user, total_price=total)
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    items.delete()
    # メール送信
    send_mail(
        subject='ご注文ありがとうございます',
        message=f'{request.user.username}様\nご注文を受け付けました。\n合計金額: {total}円',
        from_email=None,
        recipient_list=[request.user.email],
        fail_silently=True,
    )
    return redirect('order_history')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_history.html', {'orders': orders})

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    if not items:
        return redirect('cart')
    total = sum(item.product.price * item.quantity for item in items)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session_params = {
        'payment_method_types': ['card'],
        'line_items': [{
            'price_data': {
                'currency': 'jpy',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.product.price),  # 小数点以下を削除
            },
            'quantity': item.quantity,
        } for item in items],
        'mode': 'payment',
        'success_url': request.build_absolute_uri('/order/history/'),
        'cancel_url': request.build_absolute_uri('/cart/'),
    }
    if request.user.email:
        session_params['customer_email'] = request.user.email
    session = stripe.checkout.Session.create(**session_params)
    return redirect(session.url)
