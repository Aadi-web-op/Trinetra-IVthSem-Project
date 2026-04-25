from django.urls import path
from . import views

urlpatterns = [
    path('', views.officer_login, name='portal_login'),
    path('admin-security/2fa/', views.Admin2FAView.as_view(), name='admin_2fa'),
    path('admin-security/logout/', views.custom_admin_logout, name='clean_logout'),
    path('logout/', views.officer_logout, name='officer_logout'),
    path('dashboard/', views.officer_dashboard, name='officer_dashboard'),
    path('api/chat/', views.ai_chat_endpoint, name='ai_chat_endpoint'),
    path('api/generate-legal/', views.generate_legal, name='generate_legal'),
    path('ai-lab/', views.ai_lab, name='ai_lab'),
    path('authorize/', views.authorize_ai, name='authorize_ai'),
    path('api/create-case/', views.create_case_endpoint, name='create_case'),
    path('api/chat/status/<str:task_id>/', views.ai_task_status, name='ai_task_status'),
    path('sys/factory_reset/', views.factory_reset, name='factory_reset'),
    path('cases/', views.cases_view, name='cases'),
    path('evidence/', views.evidence_view, name='evidence'),
    path('audit-logs/', views.audit_logs_view, name='audit_logs'),
    path('settings/', views.settings_view, name='settings'),
]
