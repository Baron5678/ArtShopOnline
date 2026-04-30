from datetime import datetime, timezone
from typing import  Any

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.middleware.csrf import get_token
from django.shortcuts import render
import xml.etree.ElementTree as Et
import json

from django.views.decorators.http import require_POST
from lxml import etree
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.files import File
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, LoginForm, ProfileForm, CustomUserChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import login, authenticate, logout
from .tokens import generate_token
from .models import ArtProduct, Profile, Comment, CartItem, Order, OrderItem, Receipt


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            pass1 = form.cleaned_data.get("password1")
            pass2 = form.cleaned_data.get("password2")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists! Please try a different username.")
                return redirect('/register')
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
                return redirect('/register')
            if pass1 != pass2:
                messages.error(request, "Passwords do not match!")
                return redirect('/register')

            myuser = User.objects.create_user(username, email, pass1)
            myuser.username = username
            myuser.is_active = False
            myuser.save()

            subject = "Welcome to Our Django User Registration System"
            message = (f"Hello {myuser.username}!\n\nThank you for registering on our website. Please confirm your"
                   f"email address to activate your account.\n\nRegards,\nThe Django Team")
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email, to_list, fail_silently=False)

            current_site = get_current_site(request)
            email_subject = "Confirm Your Email Address"
            message2 = render_to_string('Authorization/Confirmation.html', {
                'name': myuser.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            send_mail(email_subject, message2, from_email, to_list, fail_silently=True)
            messages.success(request, """Your account has been created successfully! Please check your email 
                                              to confirm your email address and activate your account.""")
            return redirect('/login')
    else:
        form = RegisterForm()
    return render(request, 'Authorization/Registration.html', {'form': form})


def activate(request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
        new_profile = Profile()
        if myuser is not None and generate_token.check_token(myuser, token):
            myuser.is_active = True
            myuser.save()
            new_profile.user = myuser
            new_profile.avatar_height = 200
            new_profile.avatar_width = 200
            with open('static/images/oldman.jpg', 'rb') as f:
                new_profile.avatar.save("oldman.jpg", File(f), save=True)
            new_profile.bio = "Put some bio"
            new_profile.birthday = "2024-01-27"
            new_profile.save()
            messages.success(request, "Your account has been activated!")
            return redirect('login')
        else:
            return render(request, 'Authorization/ActivationFailed.html')


def user_login(request):
    if request.method == 'POST':
        if request.user.is_staff:
            return redirect('home')
        logform = LoginForm(request, data=request.POST)
        if logform.is_valid():
            username = logform.cleaned_data.get('username')
            raw_password = logform.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        logform = LoginForm()
    return render(request, 'Authorization/LogIn.html', {'logform': logform})


def home(request):
    context: dict[str, Any] = {'is_auth': request.user.is_authenticated,
                               'is_admin': request.user.is_staff}

    if context['is_auth'] and not context['is_admin']:
        context['username'] = request.user.username
        context['prof_id'] = request.user.profile.id
        context['cart'] = request.user.profile.cart.all()
        context['cart_items'] = CartItem.objects.filter(profile=request.user.profile)
        context['total_cart_price'] = sum(item.product.price * item.quantity for item in context['cart_items'])
        context['total_quantity'] = sum(item.quantity for item in context['cart_items'])

    context['art_products'] = ArtProduct.objects.all()

    if len(context['art_products']) == 0:
        generate_product()
        generate_product()
        generate_product()
    return render(request, 'HomePage.html', context)


def profile(request, prof_id):
    curr_prof = get_object_or_404(Profile, id=prof_id)
    cart_items = CartItem.objects.filter(profile=curr_prof)
    context = {'is_auth': curr_prof.user.is_authenticated,
               'is_admin': curr_prof.user.is_staff,
               'prof_id': curr_prof.id,
               'username': curr_prof.user.username,
               'current_profile': curr_prof,
               'cart_items': cart_items,
               'total_cart_price': sum(item.product.price * item.quantity for item in cart_items),
               'total_quantity': sum(item.quantity for item in cart_items),
               'receipts': Receipt.objects.filter(profile=curr_prof)
               }

    return render(request, 'Profile.html', context=context)

def edit_profile(request, prof_id):
    current_profile = get_object_or_404(Profile, pk=prof_id)

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=current_profile.user)
        prof_form = ProfileForm(request.POST, request.FILES, instance=current_profile)

        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile', prof_id=prof_id)
    else:
        user_form = CustomUserChangeForm(instance=current_profile.user)
        prof_form = ProfileForm(instance=current_profile)

    return render(request, 'EditProfile.html', {
        'is_auth': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'username': request.user.username,
        'user_form': user_form,
        'prof_form': prof_form,
        'prof_id': prof_id
    })


def serialize_product_to_xml(product_id, request):
    product = ArtProduct.objects.get(pk=product_id)
    comments = product.comments.all()
    csrf_token = get_token(request)

    page_element = Et.Element('Page')
    user_element = Et.SubElement(page_element,'User')
    product_element = Et.SubElement(page_element,'ArtProduct')
    comments_element = Et.SubElement(page_element, 'Comments')
    Et.SubElement(product_element, "id").text = str(product_id)
    Et.SubElement(product_element, "name").text = str(product.name)
    Et.SubElement(product_element, "price").text = str(product.price)
    Et.SubElement(product_element, "copies").text = str(product.copies)
    if product.image:
        Et.SubElement(product_element, "image").text = str(product.image.url)
    Et.SubElement(product_element, "image_width").text = str(product.image_width)
    Et.SubElement(product_element, "image_height").text = str(product.image_height)
    Et.SubElement(product_element, "paint_type").text = str(product.paint_type)
    Et.SubElement(product_element, "material").text = str(product.material)
    Et.SubElement(product_element, "genre").text = str(product.genre)
    Et.SubElement(product_element, "rate").text = str(product.rate)
    Et.SubElement(product_element, "description").text = str(product.description)

    Et.SubElement(user_element, "is_auth").text = str(request.user.is_authenticated)
    Et.SubElement(user_element, "is_admin").text = str(request.user.is_staff)
    if request.user.is_authenticated and not request.user.is_staff:
        Et.SubElement(user_element, "username").text = str(request.user.username)
        Et.SubElement(user_element, "prof_id").text = str(request.user.profile.id)
    for comment in comments:
        comment_el = Et.SubElement(comments_element, 'Comment')
        all_user_element = Et.SubElement(comment_el, 'user')
        all_user_element.text = comment.profile.user.username
        text_element = Et.SubElement(comment_el, 'text')
        text_element.text = comment.content
        date_element = Et.SubElement(comment_el, 'created_at')
        date_element.text = comment.created_at.strftime('%Y-%m-%d %H:%M')

    csrf_element = Et.SubElement(page_element, "csrf_token")
    csrf_element.text = csrf_token

    xml_data = Et.tostring(page_element, encoding='unicode')
    return xml_data

def transform_xml_to_html(xml_data):
    xslt_doc = etree.parse('static/products_details.xslt')
    xslt_transformer = etree.XSLT(xslt_doc)

    source_doc = etree.fromstring(xml_data)
    output_doc = xslt_transformer(source_doc)

    return str(output_doc)

def product_view(request, product_id):
    xml_data = serialize_product_to_xml(product_id, request)
    html_content = transform_xml_to_html(xml_data)
    return HttpResponse(html_content)


def products_set(request):
    context: dict[str, Any] = {
        'is_auth': request.user.is_authenticated,
        'username': request.user.username,
        'is_admin': request.user.is_staff,
        'art_products': ArtProduct.objects.all()
    }

    if request.user.is_authenticated and not request.user.is_staff:
        context['prof_id'] = request.user.profile.id

    return render(request, 'AllArtProducts.html', context)

def products_set_json(request):
    products = ArtProduct.objects.all()
    data = []
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image_url': product.image.url if product.image else '',
        }
        data.append(product_data)
    return JsonResponse(data, safe=False)


@login_required
@require_POST
@transaction.atomic
def add_to_cart(request, product_id):
    try:
        prod = ArtProduct.objects.get(id=product_id)
    except ArtProduct.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
    if prod.copies <= 0:
        return JsonResponse({'status': 'error', 'message': 'Product is out of stock'}, status=400)
    item, created = CartItem.objects.get_or_create(profile=request.user.profile, product=prod)
    if not created:
        item.quantity += 1
    else:
        item.quantity = 1
    item.total_price = prod.price * item.quantity
    item.save(update_fields=['quantity', 'total_price'])
    request.user.profile.cart.add(prod)
    prod.copies -= 1
    prod.save(update_fields=['copies'])
    return JsonResponse({'status': 'success', 'message': 'Product added to cart'})

@login_required
@require_POST
@transaction.atomic
def remove_from_cart(request, product_id):
    try:
        prod = ArtProduct.objects.get(id=product_id)
    except ArtProduct.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    if not request.user.profile.cart.filter(id=prod.id).exists():
        return JsonResponse({'status': 'error', 'message': 'Product is not in cart'}, status=400)
    try:
        item = CartItem.objects.get(
            profile=request.user.profile,
            product=prod
        )
    except CartItem.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product is not in cart'
        }, status=400)

    prod.copies += 1
    if item.quantity > 1:
        item.quantity -= 1
        item.total_price = prod.price * item.quantity
        item.save(update_fields=['quantity', 'total_price'])
    else:
        item.delete()
        request.user.profile.cart.remove(prod)
    prod.save(update_fields=['copies'])
    return JsonResponse({'status': 'success',
                         'message': 'Product removed from cart',
                         'amount': item.quantity,
                         'total_price': item.total_price})

def start_checkout(request):
    cart_items = CartItem.objects.filter(profile=request.user.profile)
    if not cart_items.exists():
        return render(request, "Status.html", {
            "status": 400,
            "message": "Your cart is empty."
        })

    order = Order.objects.create(profile=request.user.profile,
                                 status='pending',
                                 total_price=sum(item.total_price for item in cart_items))
    for item in cart_items:
        OrderItem.objects.create(order=order,
                                 product=item.product,
                                 product_name=item.product.name,
                                 price=item.product.price,
                                 amount=item.quantity)
    return redirect("fake_payment", order_id=order.id)

def fake_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, profile=request.user.profile)
    if order.status != 'pending':
        return render(request, "Status.html", {
            "status": 400,
            "message": "Invalid order status."
        })

    if request.method == 'POST':
      action = request.POST.get('action')
      if action == 'pay':
          return redirect('payment_success', order_id=order.id)
      elif action == 'cancel':
          return redirect('payment_cancel', order_id=order.id)

    return render(request, "Payments/FakePayment.html", {'order': order})

@login_required
def payment_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        profile=request.user.profile
    )

    if order.status != "pending":
        return render(request, "Status.html", {
            "status": 400,
            "message": "Invalid order status."
        })

    order.status = "paid"
    order.paid_at = datetime.now()
    order.save()

    for item in order.items.all():
        product = item.product
        product.save()

    CartItem.objects.filter(profile=request.user.profile).delete()

    Receipt.objects.create(
        profile=order.profile,
        order=order,
        total_price=order.total_price,
        payment_method="Fake card",
        billing_address="Fake billing address",
        shipping_address="Fake shipping address",
    )

    return render(request, "Payments/PaymentSuccess.html", {
        "order": order
    })
@login_required
def payment_cancel(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        profile=request.user.profile)

    if order.status != "pending":
        return render(request, "Status.html", {
            "status": 400,
            "message": "Invalid order status."
        })

    order.status = "cancelled"
    order.save()
    return render(request, "Payments/PaymentCancel.html", {
        "order": order})

@login_required
def download_receipt_xml(request, receipt_id):
    receipt = get_object_or_404(
        Receipt,
        id=receipt_id,
        profile=request.user.profile
    )

    root = Et.Element("Receipt")

    Et.SubElement(root, "ReceiptId").text = str(receipt.id)
    Et.SubElement(root, "Profile").text = receipt.profile.user.username
    Et.SubElement(root, "TotalPrice").text = str(receipt.total_price)
    Et.SubElement(root, "PurchaseDate").text = str(receipt.purchase_date)
    Et.SubElement(root, "PaymentMethod").text = receipt.payment_method

    products_element = Et.SubElement(root, "Products")

    for item in receipt.order.items.all():
        product_element = Et.SubElement(products_element, "Product")

        Et.SubElement(product_element, "Name").text = item.product_name
        Et.SubElement(product_element, "Amount").text = str(item.amount)
        Et.SubElement(product_element, "Price").text = str(item.price)
        Et.SubElement(product_element, "Total").text = str(item.total_price())

    xml_data = Et.tostring(root, encoding="utf-8", xml_declaration=True)

    response = HttpResponse(xml_data, content_type="application/xml")
    response["Content-Disposition"] = f'attachment; filename="receipt_{receipt.id}.xml"'

    return response
def send_comment(request, product_id):
   if request.method == "POST":
       prod = get_object_or_404(ArtProduct, pk=product_id)
       comment_content = request.POST.get('comment')
       if comment_content and request.user.is_authenticated:
           Comment.objects.create(profile=request.user.profile, content=comment_content, product=prod)
       return redirect('product_details', product_id=product_id)
   return redirect('product_details', product_id=product_id)

def logout_view(request):
    logout(request)
    return redirect('home')


def generate_product():
    product = ArtProduct()
    product.price = 100
    product.name = 'Old artist'
    product.genre = 'Portrait'
    product.image_height = 200
    product.image_width = 200
    product.material = 'Paper'
    product.paint_type = 'Acrylic'
    product.rate = 4
    product.description = ('Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque '
                           'laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi '
                           'architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas '
                           'sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione '
                           'voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet,'
                           'consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et '
                           'dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum '
                           'exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi '
                           'consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam '
                           'nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla '
                           'pariatur? ')

    with open('static/images/oldman.jpg', 'rb') as f:
        product.image.save("oldman.jpg", File(f), save=True)
    product.save()



