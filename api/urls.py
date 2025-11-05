from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Auth
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('verify-otp/', views.VerifyOtpView.as_view(), name='verify-otp'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('appointments/create/', views.AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointments/doctor/', views.DoctorAppointmentListView.as_view(), name='doctor-appointment-list'),
    # Profiles
    path('student/profile/', views.StudentProfileView.as_view(), name='student-profile'),
    path('doctor/profile/', views.DoctorProfileView.as_view(), name='doctor-profile'),
    path('staff/profile/', views.StaffProfileView.as_view(), name='staff-profile'),
    path('caretaker/profile/', views.CaretakerProfileView.as_view(), name='caretaker-profile'),
    
    # Doctor Availability
    path('doctor/available/', views.set_doctor_available, name='doctor-available'),
    path('doctor/unavailable/', views.set_doctor_unavailable, name='doctor-unavailable'),
    path('doctors/<str:username>/slots/<str:date_str>/', views.get_available_slots, name='get-available-slots'),
    # SOS & Alerts
    path('sos/trigger/', views.SOSCreateView.as_view(), name='sos-trigger'),
    path('sos/active/', views.SOSActiveListView.as_view(), name='sos-active-list'),
    path('sos/details/<str:event_id>/', views.get_sos_details, name='sos-details'),
    path('sos/<int:pk>/<str:action>/', views.SOSActionView.as_view(), name='sos-action'),
    path('create-admin-once/', views.create_admin_once, name='create-admin'),
    path('get-turn-credentials/', views.get_turn_credentials, name='get-turn-credentials'),
    path('prescriptions/create/', views.PrescriptionCreateView.as_view(), name='prescription-create'),
    
    # GET for Student to see their list of prescriptions
    path('prescriptions/student/', views.StudentPrescriptionListView.as_view(), name='student-prescription-list'),
    
    # GET for Doctor/Student to see the prescription for one appointment
    path('prescriptions/appointment/<int:appointment_id>/', views.AppointmentPrescriptionDetailView.as_view(), name='appointment-prescription-detail'),
    # GET/PUT /api/staff/student-vitals/<username>/
    path('staff/student-vitals/<str:username>/', views.StaffStudentVitalsUpdateView.as_view(), name='staff-student-vitals'),
    
    # POST /api/staff/schedule/update/
    path('staff/schedule/update/', views.StaffScheduleUpdateView.as_view(), name='staff-schedule-update'),
    path('doctors/list-available/', views.AvailableDoctorListView.as_view(), name='doctor-list-available'),
    # GET /api/staff/doctors/
    path('staff/doctors/', views.DoctorListForStaffView.as_view(), name='staff-doctor-list'),
]
    # Test & Deprecated
    # path('test-email/', views.test_email, name='test-email'),
    # path('sos/send-email/', views.SendSOSMailView.as_view(), name='send_sos_email_deprecated'),


