from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import GameSession
import random
from django.contrib.auth.decorators import login_required


@login_required
def play_game(request, session_id):
    session = GameSession.objects.get(id=session_id)

    # Якщо гра завершена, повертаємо повідомлення
    if not session.is_active:
        return redirect('play_game', session_id=session.id)

    # Ініціалізуємо список історії, якщо його ще немає
    if not hasattr(session, 'history'):
        session.history = []
    else:
        session.history = list(session.history)  # Забезпечуємо правильний тип (перетворюємо з JSONField, якщо потрібно)

    # Обробка POST запиту (коли користувач вводить число)
    if request.method == "POST":
        guess = int(request.POST['guess'])
        session.history.append(guess)  # Додаємо введене число до історії

        if guess == session.target_number:
            session.is_active = False
            session.result = "Win"
            session.save()
            return render(request, 'play.html', {
                'session': session,
                'message': "Вітаємо! Ви виграли!",
                'history': session.history,
                'range': f"0 - {session.target_range}"
            })
        elif guess < session.target_number:
            hint = "Більше"
        else:
            hint = "Менше"

        # Обчислення індикатора близькості
        difference = abs(session.target_number - guess)
        proximity_percentage = max(0, 100 - difference * 100 // session.target_range)

        # Зменшуємо кількість спроб і перевіряємо, чи залишилися спроби
        session.attempts_left -= 1
        if session.attempts_left == 0:
            session.is_active = False
            session.result = "Lose"
            session.save()
            return render(request, 'play.html', {
                'session': session,
                'message': f"Ви програли! Правильне число: {session.target_number}",
                'history': session.history,
                'range': f"0 - {session.target_range}"
            })

        session.save()

        return render(request, "game.html", {
            "hint": hint,
            "attempts_left": session.attempts_left,
            "proximity_percentage": proximity_percentage,
            "history": session.history,
            "range": f"0 - {session.target_range}"
        })

    return render(request, "game.html", {
        "attempts_left": session.attempts_left,
        "history": session.history,
        "range": f"0 - {session.target_range}"
    })

@login_required
def choose_difficulty(request):
    """
    Вибір рівня складності гри.
    """
    return render(request, "choose_difficulty.html")

@login_required
def start_game(request, difficulty):
    """
    Початок гри з вибором складності.
    """
    # Налаштування залежно від складності
    if difficulty == "easy":
        attempts = 10
        max_number = 100
    elif difficulty == "medium":
        attempts = 5
        max_number = 100
    elif difficulty == "hard":
        attempts = 3
        max_number = 500
    else:
        return redirect('choose_difficulty')  # Перенаправлення, якщо складність невірна

    # Генеруємо випадкове число для гри
    target_number = random.randint(1, max_number)

    # Створюємо нову ігрову сесію
    session = GameSession.objects.create(
        user=request.user,
        result="In Progress",
        attempts_left=attempts,
        target_number=target_number,
    )
    return redirect('play_game', session_id=session.id)
