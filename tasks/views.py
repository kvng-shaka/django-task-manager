from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash
from django.db.models import Q
from datetime import date

from .models import Task
from .forms import ProfileForm, TaskForm, UserUpdateForm

# Create your views here.

@login_required
def task_list(request):
    # tasks = Task.objects.all().order_by('-created_at')
    # tasks = Task.objects.filter(owner=request.user).order_by('-created_at')
    tasks = Task.objects.filter(owner=request.user)
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')

    if search:
        tasks = tasks.filter(Q(title__icontains=search) | Q(description__icontains=search))

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    tasks = tasks.order_by('-created_at')

    # Dashboard statistics
    user_tasks = Task.objects.filter(owner=request.user)
    total_tasks = user_tasks.count()
    pending_tasks = user_tasks.filter(status='pending').count()
    in_progress_tasks = user_tasks.filter(status='in_progress').count()
    completed_tasks = user_tasks.filter(status='completed').count()

    if total_tasks > 0:
        completion_percentage = round((completed_tasks / total_tasks) * 100)
    else:
        completion_percentage = 0

    today = date.today()

    for task in tasks:
        task.is_overdue = (task.due_date and task.due_date < today and task.status != 'completed')
        if task.due_date:
            if task.due_date == today:
                task.due_label = 'Due today'
            elif task.due_date > today:
                days_remaining = (task.due_date - today).days
                if days_remaining == 1:
                    task.due_label = 'Due tomorrow'
                else:
                    task.due_label = (f'Due in {days_remaining} days')
            else:
                days_overdue = (today - task.due_date).days
                if days_overdue == 1:
                    task.due_label = '1 day overdue'
                else:
                    task.due_label = (f'{days_overdue} days overdue')
        else:
            task.due_label = 'No due date'

    context = {
        'tasks': tasks,'search': search, 'status': status, 'priority': priority, 'total_tasks': total_tasks,
        'pending_tasks': pending_tasks, 'in_progress_tasks': in_progress_tasks, 'completed_tasks': completed_tasks, 'completion_percentage': completion_percentage
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})


@login_required
def task_details(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return redirect('task_detail', pk=task.pk)



def register(request):
    if request.user.is_authenticated:
        return redirect('task_list')  # Redirect authenticated users to the task list
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user =form.save()
            login(request, user)  # Log the user in after successful registration    
            return redirect('task_list') 
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required
def profile(request):
    user_profile = request.user.profile
    return render(request, 'registration/profile.html', {'profile': user_profile})



@login_required
def edit_profile(request):
    user_profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user_profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=user_profile)
        user_form = UserUpdateForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'profile_form': profile_form, 'user_form': user_form})



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})



@login_required
def toggle_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if task.status == 'completed':
        task.status = 'pending'
    else:
        task.status = 'completed'
    task.save()
    return redirect('task_list')