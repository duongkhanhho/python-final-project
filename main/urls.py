from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, auth_views

router = DefaultRouter()
router.register(r'regions', views.KhuVucViewSet)
router.register(r'countries', views.QuocGiaViewSet)
router.register(r'locations', views.DiaDiemViewSet)
router.register(r'jobs', views.CongViecViewSet)
router.register(r'departments', views.PhongBanViewSet)
router.register(r'employees', views.NhanVienViewSet)
router.register(r'dependents', views.NguoiPhuThuocViewSet)
router.register(r'attendance', views.AttendanceViewSet)
router.register(r'payroll', views.PayrollRecordViewSet)

urlpatterns = [
    # Authentication URLs
    path('auth/register/', auth_views.RegisterView.as_view(), name='register'),
    path('auth/login/', auth_views.LoginView.as_view(), name='login'),
    path('auth/logout/', auth_views.logout_view, name='logout'),
    path('auth/profile/', auth_views.profile_view, name='profile'),
    path('auth/change-password/', auth_views.change_password_view, name='change-password'),
    
    # API URLs
    path('', include(router.urls)),
] 