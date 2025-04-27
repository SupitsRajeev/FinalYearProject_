from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # ----------------------------
    # Admin and Authentication
    # ----------------------------
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ----------------------------
    # Landing and Main Redirection
    # ----------------------------
    path('', views.landing_page, name='landing'),
    path('redirect/', views.login_redirect, name='login_redirect'),

    # ----------------------------
    # Department Dashboards
    # ----------------------------
    path('hr/', views.hr_application_view, name='hr_application'),
    path('hr/dashboard/', views.hr_dashboard_view, name='hr_dashboard'),
    path('it_dashboard/', views.it_dashboard_view, name='it_dashboard'),
    path('admin/dashboard/', views.hr_application_view, name='admin_dashboard'),

    # ----------------------------
    # User Management
    # ----------------------------
    path('manage_users/', views.manage_users_view, name='manage_users'),
    path('toggle_user/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('revoke-privilege/<int:user_id>/', views.revoke_privilege_view, name='revoke_privilege'),  # 👈 NEW

    # ----------------------------
    # Privileged Access Request Flow
    # ----------------------------
    path('request-access/', views.request_privilege_view, name='request_access'),
    path('review-requests/', views.review_privilege_requests_view, name='review_privilege_requests'),
    path('approve-request/<int:request_id>/', views.approve_privilege_view, name='approve_privilege'),
   # Session Monitoring View
   path('session-logs/', views.session_logs_view, name='session_logs'),

   path('download-session-logs-pdf/', views.download_session_logs_pdf, name='download_session_logs_pdf'),



]
