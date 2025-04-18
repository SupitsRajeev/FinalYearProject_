from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #  Landing and Auth
    path('', views.landing_page, name='landing'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    #  Main Dashboard (shared)
    path('hr/', views.hr_application_view, name='hr_application'),

    # 🔐 Login Redirect Handler
    path('redirect/', views.login_redirect, name='login_redirect'),
    path('logout/', views.logout_view, name='logout'),

    #  Role-specific dashboards
    path('hr/dashboard/', views.hr_dashboard_view, name='hr_dashboard'),
    path('it/dashboard/', views.it_dashboard_view, name='it_dashboard'),
    path('admin/dashboard/', views.hr_application_view, name='admin_dashboard'),


    #  No privilege page
    path('no_privilege/', views.no_privilege_fallback, name='no_privilege'),

]
