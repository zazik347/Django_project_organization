from django.shortcuts import render
from .models import UserActivity


def view_user_activity(request):
    # Получаем все действия текущего пользователя
    activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'activity.html', {'activities': activities})
