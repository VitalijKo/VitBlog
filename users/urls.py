from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('profiles/', views.profiles, name='profiles'),
    path('landing/', views.landing_login, name='landingLogin'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('profile/<str:username>/', views.user_profile, name='user-profile'),
    path('follow/<str:username>/', views.toggle_follow, name='follow-unfollow'),
    path('account/', views.user_account, name='account'),
    path('edit-account/', views.edit_account, name='edit-account'),
    path('create-interest/', views.create_interest, name='create-interest'),
    path('update-interest/<slug:interest_slug>/', views.update_interest, name='update-interest'),
    path('delete-interest/<slug:interest_slug>/', views.delete_interest, name='delete-interest'),
    path('interest/<slug:interest_slug>', views.profiles_by_interest, name='interest'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.view_message, name='message'),
    path('create-message/<str:username>/', views.create_message, name='create-message')
]
