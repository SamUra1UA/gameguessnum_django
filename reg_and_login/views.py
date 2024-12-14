from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gamemodel.models import GameSession


@login_required
def profile(request):
    # Отримати всі ігрові сесії користувача
    games = GameSession.objects.filter(user=request.user).order_by('-created_at')

    # Обчислити статистику
    total_games = games.count()
    wins = games.filter(result="Win").count()
    losses = games.filter(result="Lose").count()

    if total_games > 0:
        win_percentage = round((wins / total_games) * 100, 2)
        loss_percentage = round((losses / total_games) * 100, 2)
    else:
        win_percentage = loss_percentage = 0

    stats = {
        "total_games": total_games,
        "wins": wins,
        "losses": losses,
        "win_percentage": win_percentage,
        "loss_percentage": loss_percentage,
    }

    return render(request, "profile.html", {"user": request.user, "games": games, "stats": stats})


from django.db.models import Count
from django.shortcuts import render
from gamemodel.models import GameSession

def home(request):
    # Знайти топ 25 гравців за кількістю перемог у всіх іграх
    top_players = GameSession.objects.values('user__username').annotate(wins=Count('id')).order_by('-wins')[:25]

    return render(request, 'home.html', {'top_players': top_players})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # Перенаправлення на головну сторінку після виходу
    else:
        return HttpResponseForbidden("Метод не дозволений")
