from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profiles/', views.profiles, name='profiles'),
    path('home/', views.home_login, name='home_login'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('follow/<str:username>/', views.toggle_follow, name='follow'),
    path('account/', views.user_account, name='account'),
    path('edit-account/', views.edit_account, name='edit_account'),
    path('create-interest/', views.create_interest, name='create_interest'),
    path('update-interest/<slug:interest_slug>/', views.update_interest, name='update_interest'),
    path('delete-interest/<slug:interest_slug>/', views.delete_interest, name='delete_interest'),
    path('interest/<slug:interest_slug>', views.profiles_by_interest, name='interest'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.view_message, name='message'),
    path('create-message/<str:username>/', views.create_message, name='create_message')
]
