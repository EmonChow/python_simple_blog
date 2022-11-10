from django.urls import path
from . import views


urlpatterns = [
    path('home', views.home_page, name="home"),
    path('about', views.about_page, name="about"),
    path('contact', views.contact_page, name="contact"),
    path('dashboard', views.dashboard_page, name="dashboard"),
    path('signup', views.signup_page, name="signup"),
    path('login', views.login_page, name="user_login"),
    path('logout', views.user_logout, name="logout"),
    path('add_post', views.add_post, name="add_post"),
    path('update_post/<int:id>/', views.update_post, name="update_post"),
    path('delete_post/<int:id>/', views.delete_post, name="delete_post"),
]
