# from django.urls import path
# from .views import SignupView, VerifyOtpView, MyTokenObtainPairView
# from rest_framework_simplejwt.views import TokenRefreshView

# urlpatterns = [
#     path('signup/', SignupView.as_view(), name='signup'),
#     path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),

#     path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
#     path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
#     # JWT Authentication Endpoints
#     path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]

from django.urls import path
from .views import (
    SignupView, 
    VerifyOtpView, 
    MyTokenObtainPairView,
    SOSCreateView,
    SOSActiveListView,
    SOSActionView,
    StudentProfileView,
    test_email ,# <-- 1. IMPORT THE NEW VIEW
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Auth
    path('test-email/', test_email),

    path('signup/', SignupView.as_view(), name='signup'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # SOS Feature
    path('sos/trigger/', SOSCreateView.as_view(), name='sos-trigger'),
    path('sos/active/', SOSActiveListView.as_view(), name='sos-active-list'),
    path('sos/<int:pk>/<str:action>/', SOSActionView.as_view(), name='sos-action'),

    # --- 2. ADD THE URL ROUTE FOR THE PROFILE ---
    path('profile/student/', StudentProfileView.as_view(), name='student-profile'),
]

