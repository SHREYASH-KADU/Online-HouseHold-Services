from django.urls import path,re_path
from . import views #manually added

urlpatterns = [
    path('', views.index, name='index'),
    path('service/<slug:slug>/', views.services, name='services'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<slug:service_slug>/<int:worker_id>', views.serviceDetails, name='serviceDetail'),
    path('<slug:service_slug>/<int:worker_id>/payment', views.payment, name='payment'),
    path('success', views.last, name='last')
]