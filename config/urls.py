from django.contrib import admin
from django.urls import path
from erp import views as erp_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', erp_views.dashboard, name='dashboard'),
    path('orders/', erp_views.orders_view, name='orders'),
    path('inventory/', erp_views.inventory_view, name='inventory'),
    path('drawings/', erp_views.drawings_view, name='drawings'),
    path('ai/insights/', erp_views.ai_insights_view, name='ai_insights'),

    # 🔐 로그인 / 로그아웃 / 회원가입
    path('login/',  auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),        name='logout'),
    path('signup/', erp_views.signup_view,                                   name='signup'),
]
