from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# -------------------------------
# REGISTER
# -------------------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
  
    return render(request, 'registration/register.html', {'form': form})



# -------------------------------
# TASK LIST / ADD TASK / csrf.exempt
# -------------------------------
@csrf_exempt
@login_required
def update_deadline(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('id')
        new_deadline = data.get('new_deadline')
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.deadline = new_deadline
            task.save()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
         return JsonResponse({'status': 'fail', 'messages': 'Task not found'})

def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('order') # faqat login foydalanuvchi tasklari
    today = date.today()

    # SEARCH
    query = request.GET.get("q")
    if query:
        tasks = tasks.filter(title__icontains=query)

    # FILTER
    status = request.GET.get("status")
    if status == "completed":
        tasks = tasks.filter(completed=True)
    if status == "pending":
        tasks = tasks.filter(completed=False)

    # ADD TASK
    if request.method == "POST":
        title = request.POST.get("title")
        deadline = request.POST.get("deadline")
        priority = request.POST.get("priority")

        Task.objects.create(
            title=title,
            deadline=deadline if deadline else None,
            priority=priority,
            user=request.user  # muhim: user bilan bog‘lanadi
        )

        return redirect("task_list")

    return render(request, "todo/task_list.html", {
        "tasks": tasks,
        "today": today
    })

# -------------------------------
# EDIT TASK
# -------------------------------
@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)  # faqat o‘z taskini olish

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.deadline = request.POST.get("deadline") or None
        task.priority = request.POST.get("priority")
        task.save()
        return redirect("task_list")

    return render(request, "todo/edit_task.html", {"task": task})

# -------------------------------
# COMPLETE TASK
# -------------------------------
@login_required
def complete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect("task_list")

# -------------------------------
# DELETE TASK
# -------------------------------
@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    return redirect("task_list")

def update_task_order(request):
    if request.method == "POST":
        data = json.loads(request.body)

        for item in data:
            task_id = item["id"]
            order = item["order"]

            task = Task.objects.get(id=task_id)
            task.order = order
            task.save()

        return JsonResponse({"status": "success"}) 
