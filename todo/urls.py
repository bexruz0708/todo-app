from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns =[
    path ('', views.task_list, name ='task_list'),
    path('register/', views.register, name='register'),
    path('complete/<int:id>/', views.complete_task, name='complete'),
    path('delete/<int:id>/', views.delete_task, name='delete'),
    path("edit/<int:id>/", views.edit_task, name="edit_task"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("update-order/", views.update_task_order, name="update_task_order"),
   
    path('update-deadline/', views.update_deadline, name='update_deadline'),
]