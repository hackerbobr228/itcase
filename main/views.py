from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import AppItem


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'main/register.html', {'error': 'Пароли не совпадают'})

        try:
            user_obj = User.objects.get(username=email)
            if not user_obj.is_active:
                return render(request, 'main/register.html', {
                    'error': 'Этот email уже зарегистрирован, но аккаунт не активирован. Пожалуйста, <a href="/login/">войдите</a> и оплатите регистрацию для активации аккаунта.',
                    'show_login': True
                })
            else:
                return render(request, 'main/register.html', {
                    'error': 'Этот email уже зарегистрирован. Пожалуйста, <a href="/login/">войдите</a>.',
                    'show_login': True
                })
        except User.DoesNotExist:
            pass

        user = User.objects.create_user(username=email, email=email, password=password1, is_active=False)
        user.save()
        request.session['pending_user_id'] = user.id
        return redirect('payment_required')

    return render(request, 'main/register.html')

def payment_required(request):
    return render(request, 'main/payment_required.html')

def payme_initiate(request):
    from .payme import payme
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect('register')
    user = User.objects.get(id=user_id)
    order_id = f"regfee-{user.id}"
    amount = 9 * 10000  # PayMe works in tiyin, so $9 = 90000 tiyin
    payment_url = payme.create_payment_url(
        amount=amount,
        order_id=order_id,
        return_url=request.build_absolute_uri('/login/')
    )
    return redirect(payment_url)

import json
from django.http import JsonResponse
import logging

def payme_callback(request):
    # SECURITY: Only allow POST and require a secret key
    if request.method != 'POST':
        return JsonResponse({"error": {"message": "Only POST allowed"}}, status=405)

    secret = request.headers.get('X-ITCASE-PAYME-SECRET')
    if secret != 'YOUR_SECRET_KEY':  # Set a strong secret in your settings and PayMe config
        logging.warning(f"Invalid PayMe callback attempt from {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({"error": {"message": "Forbidden"}}, status=403)

    try:
        data = json.loads(request.body.decode('utf-8'))
        order_id = data.get('order_id')
        if order_id and order_id.startswith('regfee-'):
            user_id = int(order_id.split('-')[1])
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return JsonResponse({"result": {"message": "User activated"}})
        else:
            return JsonResponse({"error": {"message": "Invalid order_id"}}, status=400)
    except Exception as e:
        logging.exception("Error in PayMe callback")
        return JsonResponse({"error": {"message": str(e)}}, status=400)



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            if not user.is_active:
                return render(request, 'main/login.html', {
                    'error': 'Ваш аккаунт не активирован. Пожалуйста, оплатите регистрацию, чтобы активировать аккаунт.',
                    'payment_required': True
                })
            login(request, user)
            return redirect('dashboard')
        else:
            # Check if user exists but is inactive
            try:
                user_obj = User.objects.get(username=email)
                if not user_obj.is_active:
                    return render(request, 'main/login.html', {
                        'error': 'Ваш аккаунт не активирован. Пожалуйста, оплатите регистрацию, чтобы активировать аккаунт.',
                        'payment_required': True
                    })
            except User.DoesNotExist:
                pass
            return render(request, 'main/login.html', {'error': 'Неверные данные'})

    return render(request, 'main/login.html')


from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required(login_url='/login/')
def dashboard(request):
    if not request.user.is_active:
        return redirect('payment_required')
    
    apps = AppItem.objects.all()

    return render(request, 'main/dashboard.html', {'apps': apps, 'user': request.user})