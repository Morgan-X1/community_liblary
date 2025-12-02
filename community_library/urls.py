from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views as core_views
from users import views as user_views
from users.forms import UserLoginForm, AdminLoginForm
from inventory import views as inventory_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.landing_page, name='home'),
    path('catalog/', core_views.catalog, name='catalog'),
    path('item/<int:item_id>/', core_views.item_detail, name='item_detail'),
    path('item/<int:item_id>/reserve/', core_views.reserve_item, name='reserve_item'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('admin-dashboard/', core_views.admin_dashboard, name='admin_dashboard'),
    path('my-items/', inventory_views.my_items, name='my_items'),
    path('add-item/', inventory_views.add_item, name='add_item'),
    path('edit-item/<int:item_id>/', inventory_views.edit_item, name='edit_item'),
    path('pending-items/', inventory_views.pending_items, name='pending_items'),
    path('approve-item/<int:item_id>/', inventory_views.approve_item, name='approve_item'),
    
    # Auth URLs
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=UserLoginForm), name='login'),
    path('admin-login/', auth_views.LoginView.as_view(template_name='users/admin_login.html', authentication_form=AdminLoginForm, next_page='admin_dashboard'), name='admin_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', user_views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
