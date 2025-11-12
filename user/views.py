from django.contrib.auth.models import User
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
from user_profile.models import UserActivity
from user.models import Profile



def user_login(request):
    # Очищаем старые сообщения
    if request.method == 'GET':
        storage = messages.get_messages(request)
        for _ in storage:
            pass
    if request.method == 'POST':
        username = request.POST.get('username')  # Получаем логин
        password = request.POST.get('password')  # Получаем пароль

        # Проверяем, есть ли такой пользователь
        user = authenticate(username=username, password=password)

        if user is not None:
            # Если пользователь существует — авторизуем его
            login(request, user)
            # Сохраняем IP-адрес при входе
            ip_address = request.META.get('REMOTE_ADDR') or '0.0.0.0'
            # Получаем или создаём профиль
            profile, created = Profile.objects.get_or_create(user=user)
            profile.login_ip = ip_address
            profile.save()
            # Profile.objects.update_or_create(
            #     user=user,
            #     defaults={'login_ip': ip_address}
            # )
            # Записываем событие "Вход"
            UserActivity.objects.create(
                user=user,
                action_type='login',
                ip_address=ip_address
            )
            return redirect('main_page:index')  # Перенаправляем на главную страницу
        else:
            # Если не нашли пользователя — показываем ошибку
            messages.error(request, 'Неверный логин или пароль')
            # return redirect('users:login')  # Возвращаемся на страницу входа
            return render(request, 'login.html', {})

    return render(request, 'login.html', {})


def user_logout(request):
    logout(request)
    return redirect('main_page:index')

def user_register(request):
    # Очищаем старые сообщения
    if request.method == 'GET':
        storage = messages.get_messages(request)
        for _ in storage:
            pass
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Проверяем совпадение паролей
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return redirect('user:register')

        # Проверяем, существует ли пользователь с таким логином
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Этот логин уже занят')
            return redirect('user:register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Этот email уже используется')
            return redirect('user:register')
        # Если всё ок — создаём нового пользователя
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            user.save()
            # Сохраняем IP-адрес при регистрации
            ip_address = request.META.get('REMOTE_ADDR') or '0.0.0.0'
            Profile.objects.create(user=user, registration_ip=ip_address)

            # Записываем событие "Регистрация"
            UserActivity.objects.create(
                user=user,
                action_type='register',
                ip_address=ip_address
            )
            login(request, user)  # Авторизуем пользователя
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('user:login')
        except Exception as e:
            messages.error(request, f'Ошибка при регистрации: {e}')
            return redirect('user:register')

    return render(request, 'register.html')

