from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Auth
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('verify-otp/', views.VerifyOtpView.as_view(), name='verify-otp'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profiles
    path('student/profile/', views.StudentProfileView.as_view(), name='student-profile'),
    path('doctor/profile/', views.DoctorProfileView.as_view(), name='doctor-profile'),
    path('staff/profile/', views.StaffProfileView.as_view(), name='staff-profile'),
    path('caretaker/profile/', views.CaretakerProfileView.as_view(), name='caretaker-profile'),
    
    # Doctor Availability
    path('doctor/available/', views.set_doctor_available, name='doctor-available'),
    path('doctor/unavailable/', views.set_doctor_unavailable, name='doctor-unavailable'),
    
    # SOS & Alerts
    path('sos/trigger/', views.SOSCreateView.as_view(), name='sos-trigger'),
    path('sos/active/', views.SOSActiveListView.as_view(), name='sos-active-list'),
    path('sos/details/<str:event_id>/', views.get_sos_details, name='sos-details'),
    path('sos/<int:pk>/<str:action>/', views.SOSActionView.as_view(), name='sos-action'),
    path('create-admin-once/', views.create_admin_once, name='create-admin'),
    path('api/get-turn-credentials/', views.get_turn_credentials, name='get-turn-credentials'),
    # Test & Deprecated
    # path('test-email/', views.test_email, name='test-email'),
    # path('sos/send-email/', views.SendSOSMailView.as_view(), name='send_sos_email_deprecated'),
]

