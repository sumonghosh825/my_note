from django.urls import path
from .views import (
    register_view, login_view, logout_view,
    dashboard, profile,
    task_list, board, details, timeline,delete_task,edit_task,add_task
)

urlpatterns = [
    # Authentication
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Main Pages
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),

    # Task-related
    path('task/', task_list, name='task_list'),
    path('board/', board, name='board'),
    path('details/', details, name='details'),
    path('timeline/', timeline, name='timeline'),
    # urls.py



    path('task/delete/<int:task_id>/', delete_task, name='delete_task'),
    path('edit-task/<int:task_id>/', edit_task, name='edit_task'),
    path('task/', add_task, name='add_task'),


]
