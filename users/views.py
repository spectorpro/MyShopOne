from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, UserLoginForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES or None)
        if form.is_valid():
            user = form.save()
            # Отправляем письмо
            subject = 'Добро пожаловать в MyShop!'
            message = f'Привет, {user.username}! Ваш аккаунт успешно создан.'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]
            try:
                send_mail(subject, message, from_email, to_email, fail_silently=False)
            except Exception as e:
                # Обрабатываем ошибку отправки письма, но не блокируем регистрацию
                pass  # В продакшене лучше логировать
            login(request, user)
            return redirect('products:product_list')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next', 'products:product_list')
                return redirect(next_url)
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('users:login')
