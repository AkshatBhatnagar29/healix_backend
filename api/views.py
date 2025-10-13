# from django.core.mail import send_mail
# from django.utils import timezone
# from rest_framework import status, generics
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .models import User
# from .serializers import UserSerializer, MyTokenObtainPairSerializer
# import random
# from datetime import timedelta

# # --- Helper function to generate and send OTP ---
# def send_otp_email(user):
#     otp = random.randint(100000, 999999)
#     otp_expiry = timezone.now() + timedelta(minutes=10)
    
#     user.otp_code = str(otp)
#     user.otp_expiry = otp_expiry
#     user.save()

#     subject = 'Your Healix Verification Code'
#     message = f'Your one-time password (OTP) for Healix account verification is: {otp}\nThis code will expire in 10 minutes.'
#     from_email = 'your-email@gmail.com' # Configure this in settings.py
    
#     try:
#         send_mail(subject, message, from_email, [user.email])
#     except Exception as e:
#         # In a real app, you would log this error
#         print(f"Error sending email: {e}")


# # --- API Endpoint for User Signup ---
# class SignupView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def perform_create(self, serializer):
#         # Create the user but mark them as inactive until verified
#         user = serializer.save(is_active=False)
#         send_otp_email(user) # Send the verification OTP


# # --- API Endpoint for OTP Verification ---
# class VerifyOtpView(APIView):
#     def post(self, request):
#         data = request.data
#         try:
#             user = User.objects.get(username=data['username'])
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#         # Check if OTP is correct and not expired
#         if user.otp_code == data.get('otp') and timezone.now() < user.otp_expiry:
#             user.is_active = True
#             user.is_email_verified = True
#             user.otp_code = None
#             user.otp_expiry = None
#             user.save()
#             return Response({'message': 'Email verified successfully. You can now log in.'}, status=status.HTTP_200_OK)
        
#         return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)


# # --- Custom Login View using our secure serializer ---
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
# from django.core.mail import send_mail
# from django.utils import timezone
# from rest_framework import status, generics
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .models import User
# from .serializers import UserSerializer, MyTokenObtainPairSerializer
# import random
# from datetime import timedelta
# from django.conf import settings

# from django.contrib.auth import authenticate
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# @api_view(['POST'])
# def login_view(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     # This is the crucial part
#     user = authenticate(username=username, password=password)

#     username = request.data.get('username')
#     password = request.data.get('password')

#     print(f"--- Backend Received ---")
#     print(f"Username: '{username}'")
#     print(f"Password: '{password}'")
#     print(f"------------------------")

#     user = authenticate(username=username, password=password)

#     if user is not None:
#         # User is valid, active, and password is correct
#         # You would generate and return a token here
#         return Response({'message': 'Login Successful!'}, status=status.HTTP_200_OK)
#     else:
#         # Authentication failed
#         return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


# --- Helper function to generate and send OTP ---
# def send_otp_email(user):
#     # Generate 6-digit OTP
#     otp = random.randint(100000, 999999)
#     otp_expiry = timezone.now() + timedelta(minutes=10)

#     # Save OTP and expiry to user
#     user.otp_code = str(otp)
#     user.otp_expiry = otp_expiry
#     user.save()

#     # Email content
#     subject = 'Your Healix Verification Code'
#     message = f'Your OTP for Healix account verification is: {otp}\nThis code expires in 10 minutes.'
#     from_email = settings.DEFAULT_FROM_EMAIL  # Use settings instead of hardcoding
#     recipient_list = [user.email]

#     try:
#         send_mail(subject, message, from_email, recipient_list)
#         print(f"OTP {otp} sent to {user.email}")
#     except Exception as e:
#         print(f"Error sending OTP to {user.email}: {e}")

# # --- Signup API ---
# class SignupView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def perform_create(self, serializer):
#         # Create inactive user
#         user = serializer.save(is_active=False)
#         send_otp_email(user)  # Send OTP after user is saved

# # --- OTP Verification API ---
# class VerifyOtpView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         otp = request.data.get('otp')

#         if not username or not otp:
#             return Response({'error': 'Username and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#         if user.otp_code == otp and timezone.now() < user.otp_expiry:
#             user.is_active = True
#             user.is_email_verified = True
#             user.otp_code = None
#             user.otp_expiry = None
#             user.save()
#             return Response({'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

# # --- Custom Login API ---
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer









# from django.utils import timezone
# from rest_framework import status, generics, permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .models import User, SOSAlert
# from .serializers import UserSerializer, MyTokenObtainPairSerializer, SOSAlertSerializer
import random
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, SOSAlert, StudentProfile
from .serializers import UserSerializer, MyTokenObtainPairSerializer, SOSAlertSerializer, StudentProfileSerializer

# --- NEW: View for Student to manage their own profile ---
class StudentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # This ensures a user can only ever access their own profile
        return self.request.user.student_profile
# --- Authentication and User Management Views (largely unchanged) ---

def send_otp_email(user):
    otp = random.randint(100000, 999999)
    otp_expiry = timezone.now() + timedelta(minutes=10)

    # Save OTP and expiry to user
    user.otp_code = str(otp)
    user.otp_expiry = otp_expiry
    user.save()

    # Email content
    subject = 'Your Healix Verification Code'
    message = f'Your OTP for Healix account verification is: {otp}\nThis code expires in 10 minutes.'
    from_email = settings.DEFAULT_FROM_EMAIL  # Use settings instead of hardcoding
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        print(f"OTP {otp} sent to {user.email}")
    
    except Exception as e:
        print(f"Error sending OTP to {user.email}: {e}")
    pass 

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Create inactive user
        user = serializer.save(is_active=False)
        send_otp_email(user)
    pass

class VerifyOtpView(APIView):
    def post(self, request):
        username = request.data.get('username')
        otp = request.data.get('otp')

        if not username or not otp:
            return Response({'error': 'Username and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp_code == otp and timezone.now() < user.otp_expiry:
            user.is_active = True
            user.is_email_verified = True
            user.otp_code = None
            user.otp_expiry = None
            user.save()
            return Response({'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

    pass

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# --- SOS Feature API Views (NEW) ---

class SOSCreateView(generics.CreateAPIView):
    """
    Allows a student to trigger an SOS alert.
    POST /api/sos/trigger/
    Body: {"location_info": "Hostel A, Room 205"}
    """
    serializer_class = SOSAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Check if the user already has an active alert
        if SOSAlert.objects.filter(student=self.request.user, status__in=['Active', 'Acknowledged']).exists():
            raise serializer.ValidationError("You already have an active emergency alert.")
        
        # Associate the alert with the currently logged-in student
        serializer.save(student=self.request.user)

class SOSActiveListView(generics.ListAPIView):
    """
    Lists active and acknowledged SOS alerts.
    - Doctors see all alerts.
    - Staff/Caretakers see alerts only from students in their assigned hostel.
    - Students see only their own alert.
    GET /api/sos/active/
    """
    serializer_class = SOSAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = SOSAlert.objects.filter(status__in=['Active', 'Acknowledged']).order_by('-alert_time')

        if user.role == 'staff':
            return queryset.filter(student__student_profile__hostel__caretaker=user)
        elif user.role == 'student':
            return queryset.filter(student=user)
        
        # Doctors see all alerts
        return queryset

class SOSActionView(APIView):
    """
    A single view to handle Acknowledge and Resolve actions on an SOS alert.
    POST /api/sos/{id}/acknowledge/
    POST /api/sos/{id}/resolve/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, action):
        try:
            alert = SOSAlert.objects.get(pk=pk)
        except SOSAlert.DoesNotExist:
            return Response({'error': 'Alert not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if action == 'acknowledge':
            if user.role not in ['doctor', 'staff']:
                return Response({'error': 'You are not authorized to acknowledge alerts.'}, status=status.HTTP_403_FORBIDDEN)
            if alert.status != 'Active':
                 return Response({'error': 'This alert has already been acknowledged or resolved.'}, status=status.HTTP_400_BAD_REQUEST)
            
            alert.status = 'Acknowledged'
            alert.acknowledged_by = user
            alert.save()
            return Response(SOSAlertSerializer(alert).data, status=status.HTTP_200_OK)

        elif action == 'resolve':
            if alert.student != user:
                return Response({'error': 'You can only resolve your own alerts.'}, status=status.HTTP_403_FORBIDDEN)

            alert.status = 'Resolved'
            alert.resolved_at = timezone.now()
            alert.save()
            return Response(SOSAlertSerializer(alert).data, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
    
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
