from django.contrib import admin
from django.urls import path
from habitapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('habits/add/', views.add_habit, name='add-habit'),
    path('habits/<int:habit_id>/toggle/', views.toggle_habit_today, name='toggle-habit'),
    
    path('habits/<int:habit_id>/edit/', views.edit_habit, name='edit-habit'),
    path('habits/<int:habit_id>/archive/', views.archive_habit, name='archive-habit'), #Soft delete

    path('habits/archived/', views.archived_habits, name='archived-habits'),
    path('habits/<int:habit_id>/restore/', views.restore_habit, name='restore-habit'),

    path('login/', auth_views.LoginView.as_view(
        template_name='auth/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('register/', views.register, name='register'),
]