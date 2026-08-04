from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q

from .models import Task
from .forms import TaskForm

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

