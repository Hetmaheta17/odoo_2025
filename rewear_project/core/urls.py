from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.landing_page, name='landing'),
    path('browse/', views.browse_page, name='browse'),
    path('dashboard/', views.dashboard_page, name='dashboard'),
    
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Item management
    path('item/add/', views.add_item, name='add_item'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    
    # Admin Panel (a simple version)
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/approve/<int:item_id>/', views.approve_item, name='approve_item'),
    path('admin-panel/reject/<int:item_id>/', views.reject_item, name='reject_item'),
]