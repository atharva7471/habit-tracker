from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from datetime import date, timedelta
from django.http import JsonResponse
from collections import defaultdict
from .forms import HabitForm
from .models import Habit, HabitLog
from .utils import calculate_streaks

# Create your views here.
@login_required
def dashboard(request):
    habits = Habit.objects.filter(
        user=request.user,
        is_active=True
    )
    today = date.today()
    completed_today_count = 0
    best_streak_overall = 0

    start_date = today - timedelta(days=90)
    # calendar data
    calendar_data = defaultdict(int)
    
    logs = HabitLog.objects.filter(
        habit__user=request.user,
        completed=True,
        date__gte=start_date,
        date__lte=today
    )
    
    for log in logs:
        calendar_data[log.date] += 1
    
    for habit in habits:
        habit.is_done_today = HabitLog.objects.filter(
            habit=habit,
            date=today,
            completed=True
        ).exists()
        
        if habit.is_done_today:
            completed_today_count += 1
            
         # streak calculation
        completed_dates = list(
            HabitLog.objects.filter(
                habit=habit,
                completed=True
            ).values_list('date', flat=True)
        )
        completed_dates.sort(reverse=True)
        habit.current_streak, habit.best_streak = calculate_streaks(completed_dates)
        best_streak_overall = max(best_streak_overall, habit.best_streak)
    
    # generate last 90 days (oldest → newest)
    date_list = [
        start_date + timedelta(days=i)
        for i in range((today - start_date).days + 1)
    ]

    context = {
        'habits': habits,
        'total_habits': habits.count(),
        'completed_today': completed_today_count,
        'best_streak_overall': best_streak_overall,
        'calendar_data': dict(calendar_data),
        'date_list': date_list
    }

    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == 'POST':
        for field in form.fields.values():
            field.widget.attrs['class'] = (
            'w-full px-3 py-2 border rounded '
            'focus:outline-none focus:ring focus:border-indigo-400'
        )

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form': form})

@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, 'Habit added successfully!')
            return redirect('dashboard')
    else:
        form = HabitForm()

    return render(request, 'habits/add_habit.html', {'form': form})

@login_required
def toggle_habit_today(request, habit_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    habit = get_object_or_404(
        Habit,
        id=habit_id,
        user=request.user,
        is_active=True
    )

    today = date.today()

    habit_log, _ = HabitLog.objects.get_or_create(
        habit=habit,
        date=today
    )

    habit_log.completed = not habit_log.completed
    habit_log.save()

    return JsonResponse({
        'completed': habit_log.completed
    })
    
@login_required
def edit_habit(request, habit_id):
    habit = get_object_or_404(
        Habit,
        id=habit_id,
        user=request.user,
        is_active=True
    )

    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Habit updated successfully!')
            return redirect('dashboard')
    else:
        form = HabitForm(instance=habit)

    return render(request, 'habits/edit_habit.html', {
        'form': form,
        'habit': habit
    })

#Soft delete
@login_required
def archive_habit(request, habit_id):
    habit = get_object_or_404(
        Habit,
        id=habit_id,
        user=request.user,
        is_active=True
    )

    if request.method == 'POST':
        habit.is_active = False
        habit.save()
        messages.success(request, 'Habit archived.')
    
    return redirect('dashboard')

@login_required
def archived_habits(request):
    habits = Habit.objects.filter(
        user=request.user,
        is_active=False
    ).order_by('-created_at')

    return render(request, 'habits/archived_habits.html', {
        'habits': habits
    })
    
@login_required
def restore_habit(request, habit_id):
    habit = get_object_or_404(
        Habit,
        id=habit_id,
        user=request.user,
        is_active=False
    )

    if request.method == 'POST':
        habit.is_active = True
        habit.save()
        messages.success(request, 'Habit restored successfully!')

    return redirect('archived-habits')
