from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task
from django.db.models import Q
from datetime import datetime



# Authentication Views
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registered successfully.")
        return redirect('login')

    return render(request, 'authunticate/register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'authunticate/login.html')



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login or homepage after logout



@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


@login_required
def profile(request):
    return render(request, 'profile/profile.html')

# Dashboard/Profile Views
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')





# Task Views
@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        priority = request.POST.get('priority')
        time_period = request.POST.get('time_period')
        due_date = request.POST.get('due_date')
        assigned_to_username = request.POST.get('assigned_to')

        assigned_user = User.objects.filter(username=assigned_to_username).first()

        Task.objects.create(
            title=title,
            category=category,
            priority=priority,
            time_period=time_period,
            due_date=due_date,
            assigned_to=assigned_user,
            created_by=request.user
        )
        return redirect('add_task')

    tasks = Task.objects.filter(created_by=request.user).order_by('-created_at')
    users = User.objects.all()
    return render(request, 'task/list.html', {'tasks': tasks, 'users': users})


@login_required
def board(request):
    return render(request, 'task/board.html')


@login_required
def details(request):
    return render(request, 'task/details.html')


@login_required
def timeline(request):
    return render(request, 'timeline/timeline.html')

# views.py


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_by=request.user)
    task.delete()
    return redirect('add_task')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.category = request.POST['category']
        task.priority = request.POST['priority']
        task.time_period = request.POST['time_period']
        task.due_date = request.POST['due_date']
        assigned_username = request.POST['assigned_to']
        task.assigned_to = get_object_or_404(User, username=assigned_username)
        task.save()
        return redirect('add_task')



@login_required
def task_list(request):
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')  # get category filter
    users = User.objects.all()

    tasks = Task.objects.filter(created_by=request.user)

    if category:
        tasks = tasks.filter(category=category)

    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(priority__icontains=search_query) |
            Q(assigned_to__username__icontains=search_query) |
            Q(assigned_to__first_name__icontains=search_query) |
            Q(assigned_to__last_name__icontains=search_query)
        )

    tasks = tasks.order_by('-created_at')

    return render(request, 'task/list.html', {
        'tasks': tasks,
        'users': users,
        'search_query': search_query,
        'selected_category': category,
    })




@login_required

def timeline_view(request):
    timeline_items = [
        {"title": "Task Completed", "description": "You finished the task 'Submit Report'.", "time": datetime(2025, 5, 9, 14, 30)},
        {"title": "New Task Created", "description": "You created a new task 'Design Homepage'.", "time": datetime(2025, 5, 8, 10, 15)},
        {"title": "Login", "description": "You logged in successfully.", "time": datetime(2025, 5, 7, 9, 0)},
    ]
    return render(request, "timeline.html", {"timeline_items": timeline_items})



@login_required
def profile_view(request):
    return render(request, 'profile.html')  # your current display page

@login_required
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        location = request.POST.get('location')
        languages = request.POST.get('languages')

        user = request.user
        user.username = username
        user.email = email
        user.save()

        # You can store extra fields like location and languages in a custom profile model
        profile = user.profile  # Assuming you extended User with OneToOneField
        profile.location = location
        profile.languages = languages
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')  # redirect back to profile page
    else:
        return render(request, 'profile.html')

