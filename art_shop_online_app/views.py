from typing import Mapping, Any

from django.shortcuts import render
import xml.etree.ElementTree as Et
import json
from lxml import etree
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.files import File
from django.core.mail import EmailMessage, send_mail
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
from .models import ArtProduct, Profile
from django.views.decorators.csrf import csrf_exempt


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
            message2 = render_to_string('confirmation.html', {
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
    return render(request, 'Registration.html', {'form': form})


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
            with open('static/Images/oldman.jpg', 'rb') as f:
                new_profile.avatar.save("oldman.jpg", File(f), save=True)
            new_profile.bio = "Put some bio"
            new_profile.birthday = "2024-01-27"
            new_profile.save()
            messages.success(request, "Your account has been activated!")
            return redirect('login')
        else:
            return render(request, 'activation_failed.html')


def user_login(request):
    if request.method == 'POST':
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
    return render(request, 'LogIn.html', {'logform': logform})


def home(request):
    context: dict[str, Any] = {'is_auth': request.user.is_authenticated,
                               'is_admin': request.user.is_staff}

    if context['is_auth'] and not context['is_admin']:
        context['username'] = request.user.username
        context['prof_id'] = request.user.profile.id

    context['art_products'] = ArtProduct.objects.all()

    if len(context['art_products']) == 0:
        generate_product()
    return render(request, 'HomePage.html', context)


def profile(request, prof_id):
    curr_prof = get_object_or_404(Profile, id=prof_id)
    context = {'is_auth': curr_prof.user.is_authenticated,
               'user_name': curr_prof.user.username,
               'current_cart': curr_prof.cart,
               'current_profile': curr_prof,
               'current_user': curr_prof.user,
               'current_profile_id': curr_prof.id}

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
        'user_form': user_form,
        'prof_form': prof_form,
        'prof_id': prof_id
    })


def serialize_product_to_xml(product_id):
    product = ArtProduct.objects.get(pk=product_id)

    product_element = Et.Element('ArtProduct')

    id_element = Et.SubElement(product_element, "id")
    id_element.text = str(product_id)

    name_element = Et.SubElement(product_element, "name")
    name_element.text = product.name

    price_element = Et.SubElement(product_element, "price")
    price_element.text = str(product.price)

    if product.image:
        image_element = Et.SubElement(product_element, "image")
        image_url = product.image.url
        image_element.text = image_url

    price_element = Et.SubElement(product_element, "image_width")
    price_element.text = str(product.image_width)

    price_element = Et.SubElement(product_element, "image_height")
    price_element.text = str(product.image_height)

    price_element = Et.SubElement(product_element, "paint_type")
    price_element.text = str(product.paint_type)

    price_element = Et.SubElement(product_element, "material")
    price_element.text = str(product.material)

    price_element = Et.SubElement(product_element, "genre")
    price_element.text = str(product.genre)

    xml_data = Et.tostring(product_element, encoding='unicode')
    return xml_data


def transform_xml_to_html(xml_data):
    xslt_doc = etree.parse('static/products_details.xslt')
    xslt_transformer = etree.XSLT(xslt_doc)

    source_doc = etree.fromstring(xml_data)
    output_doc = xslt_transformer(source_doc)

    return str(output_doc)


def products_set(request):
    context = {
        'is_auth': request.user.is_authenticated,
        'username': request.user.username,
        'prof_id': request.user.profile.id,
        'is_admin': request.user.is_staff,
    }
    return render(request, 'SetProducts.html', context)


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


def product_view(request, product_id):
    xml_data = serialize_product_to_xml(product_id)
    html_content = transform_xml_to_html(xml_data)
    return HttpResponse(html_content)


@csrf_exempt
def add_to_cart(request, product_id):
    try:
        product = ArtProduct.objects.get(id=product_id)
    except ArtProduct.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
    request.user.profile.cart.add(product)
    return JsonResponse({'status': 'success', 'message': 'Product added to cart'})


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

    with open('static/Images/oldman.jpg', 'rb') as f:
        product.image.save("oldman.jpg", File(f), save=True)

    product.material = 'Paper'
    product.paint_type = 'Acrylic'

    product.save()



