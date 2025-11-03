from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import (
    DoctorProfile, StaffProfile, StudentProfile, CaretakerProfile, 
    Hostel, User, SOSAlert
)
from .serializers import (
    DoctorProfileSerializer, StaffProfileSerializer, StudentProfileSerializer,
    CaretakerProfileSerializer, UserSerializer, MyTokenObtainPairSerializer, 
    SOSAlertSerializer
)
from channels.layers import get_channel_layer
from django.views.decorators.csrf import csrf_exempt
import os
import random
import requests
import json
import django_redis
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny

# --- Redis Helper ---
def get_redis_connection():
    return django_redis.get_redis_connection("default")

# --- Profile Views ---
class DoctorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        if self.request.user.role != 'doctor':
            raise permissions.PermissionDenied("You are not authorized.")
        profile, created = DoctorProfile.objects.get_or_create(user=self.request.user)
        return profile

class StudentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user.student_profile

class StaffProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StaffProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        if self.request.user.role != 'staff':
            raise permissions.PermissionDenied("You are not authorized.")
        profile, created = StaffProfile.objects.get_or_create(user=self.request.user)
        return profile

class CaretakerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CaretakerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        if self.request.user.role != 'caretaker':
            raise permissions.PermissionDenied("You are not authorized.")
        profile, created = CaretakerProfile.objects.get_or_create(user=self.request.user)
        return profile

# --- Auth Views ---
def send_otp_email(user):
    otp = random.randint(100000, 999999)
    otp_expiry = timezone.now() + timedelta(minutes=10)
    user.otp_code = str(otp)
    user.otp_expiry = otp_expiry
    user.save()

    subject = "Your Healix Verification Code"
    message = f"Your OTP for Healix account verification is: {otp}\nThis code expires in 10 minutes."
    
    # NOTE: Add RESEND_API_KEY and DEFAULT_FROM_EMAIL to your settings
    resend_api_key = os.getenv('RESEND_API_KEY', settings.RESEND_API_KEY)
    from_email = os.getenv('DEFAULT_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {resend_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "from": from_email,
                "to": [user.email],
                "subject": subject,
                "text": message,
            },
        )
        if response.status_code in [200, 202]:
            print(f"✅ OTP {otp} sent successfully to {user.email}")
        else:
            print(f"❌ Failed to send OTP. Response: {response.text}")
    except Exception as e:
        print(f"⚠️ Error sending OTP to {user.email}: {e}")

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        user = serializer.save(is_active=False) 
        send_otp_email(user) # Send OTP on signup

class VerifyOtpView(APIView):
    permission_classes = [AllowAny]
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

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

# --- Doctor Availability Views ---
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_doctor_available(request):
    if request.user.role != 'doctor':
         return Response({"error": "Only doctors can set availability"}, status=status.HTTP_403_FORBIDDEN)
    doctor_id = request.user.id
    redis_conn = get_redis_connection()
    redis_conn.sadd("available_doctors", doctor_id)
    return Response({"status": "available"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_doctor_unavailable(request):
    if request.user.role != 'doctor':
         return Response({"error": "Only doctors can set availability"}, status=status.HTTP_403_FORBIDDEN)
    doctor_id = request.user.id
    redis_conn = get_redis_connection()
    redis_conn.srem("available_doctors", doctor_id)
    return Response({"status": "unavailable"}, status=status.HTTP_200_OK)

# --- SOS Alert Views ---
class SOSCreateView(generics.CreateAPIView):
    serializer_class = SOSAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if SOSAlert.objects.filter(student=self.request.user, status__in=['Active', 'Acknowledged']).exists():
            raise ValidationError("You already have an active emergency alert.")
        
        alert = serializer.save(student=self.request.user)

        try:
            redis_conn = get_redis_connection()
            profile_data = self.request.data.get('profile')
            if not profile_data:
                print("⚠️ WARNING: SOS request missing 'profile' data. Falling back to DB query.")
                profile_data = StudentProfileSerializer(self.request.user.student_profile).data

            sos_data = {
                "sql_alert_id": alert.id,
                "student_id": self.request.user.id,
                "student_username": self.request.user.username,
                "profile": profile_data,
                "location_info": alert.location_info,
                "alert_time": alert.alert_time.isoformat(),
            }
            sos_event_id = f"sos:{alert.id}"
            redis_conn.set(sos_event_id, json.dumps(sos_data), ex=3600)

            channel_layer = get_channel_layer()
            
            # 1. Notify ALL doctors
            doctor_message = { "type": "sos_notification", "message": { "sos_event_id": sos_event_id } }
            async_to_sync(channel_layer.group_send)("doctors_sos_group", doctor_message)

            # 2. Notify the SPECIFIC caretaker
            try:
                student_profile = self.request.user.student_profile
                if student_profile.hostel and student_profile.hostel.caretaker:
                    caretaker_user = student_profile.hostel.caretaker
                    
                    if caretaker_user.role == 'caretaker': # Check role
                        caretaker_group_name = f"caretaker_{caretaker_user.id}"
                        student_id_to_call = self.request.user.username
                        
                        print(f"Sending SOS to Caretaker: {caretaker_user.username} in group {caretaker_group_name}")
                        caretaker_message = {
                            "type": "sos_notification",
                            "message": {
                                "sos_event_id": sos_event_id,
                                "student_id_to_call": student_id_to_call,
                                "student_name": self.request.user.get_full_name(),
                                "location_info": alert.location_info
                            }
                        }
                        async_to_sync(channel_layer.group_send)(caretaker_group_name, caretaker_message)
                    else:
                        print(f"User {caretaker_user.username} is assigned to hostel but is not a 'caretaker'.")
                else:
                    print(f"Student {self.request.user.username} has no hostel or caretaker assigned.")
            except Exception as e:
                print(f"⚠️ Error sending to caretaker: {e}")
        except Exception as e:
            print(f"⚠️ Redis/Channels Error in SOSCreateView: {e}")
        
        self.send_sos_email_alert(alert, self.request.user)

    def send_sos_email_alert(self, alert, student):
        recipients = ['akshatbhatnagar797@gmail.com', 'sakshamsingh601@gmail.com'] # Example
        resend_api_key = os.getenv('RESEND_API_KEY', settings.RESEND_API_KEY)
        from_email = os.getenv('DEFAULT_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)
        
        if not resend_api_key or not from_email:
            print("⚠️ Resend API key or From Email not set, skipping email.")
            return

        headers = { "Authorization": f"Bearer {resend_api_key}", "Content-Type": "application/json" }
        email_body = (
            f"URGENT SOS ALERT!\n\n"
            f"Student Name: {student.first_name} {student.last_name}\n"
            f"Username/ID: {student.username}\n"
            f"Location: {alert.location_info}\n\n"
            f"Please respond immediately."
        )
        payload = {
            "from": from_email,
            "to": recipients,
            "subject": f"URGENT: SOS Alert from {student.username}",
            "text": email_body
        }
        try:
            requests.post("https://api.resend.com/emails", json=payload, headers=headers, timeout=2.5)
            print(f"✅ SOS Email for alert {alert.id} sent.")
        except Exception as e:
            print(f"⚠️ SOS Email failed to send: {e}")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sos_details(request, event_id):
    if request.user.role not in ['doctor', 'staff', 'caretaker']:
         return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    try:
        redis_conn = get_redis_connection()
        cached_data = redis_conn.get(event_id)
        if not cached_data:
            sql_id = event_id.split(':')[-1]
            alert = SOSAlert.objects.get(id=sql_id)
            profile_data = StudentProfileSerializer(alert.student.student_profile).data
            sos_data = {
                "sql_alert_id": alert.id,
                "student_id": alert.student.id,
                "student_username": alert.student.username,
                "profile": profile_data,
                "location_info": alert.location_info,
                "alert_time": alert.alert_time.isoformat(),
            }
            return Response(sos_data, status=status.HTTP_200_OK)
        sos_data = json.loads(cached_data)
        return Response(sos_data, status=status.HTTP_200_OK)
    except SOSAlert.DoesNotExist:
        return Response({"error": "SOS event not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SOSActiveListView(generics.ListAPIView):
    serializer_class = SOSAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = SOSAlert.objects.filter(status__in=['Active', 'Acknowledged']).order_by('-alert_time')

        if user.role == 'caretaker':
            user_hostels = user.hostel_set.all()
            if not user_hostels.exists():
                return SOSAlert.objects.none()
            return queryset.filter(student__student_profile__hostel__in=user_hostels)
        elif user.role == 'staff':
            return SOSAlert.objects.none() # Other staff see no alerts
        elif user.role == 'student':
            return queryset.filter(student=user)
        # Doctors see all
        return queryset

class SOSActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, action):
        try:
            alert = SOSAlert.objects.get(pk=pk)
        except SOSAlert.DoesNotExist:
            return Response({'error': 'Alert not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if action == 'acknowledge':
            if user.role not in ['doctor', 'staff', 'caretaker']:
                return Response({'error': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
            if alert.status != 'Active':
                 return Response({'error': 'Alert already handled.'}, status=status.HTTP_400_BAD_REQUEST)
            alert.status = 'Acknowledged'
            alert.acknowledged_by = user
            alert.save()
            return Response(SOSAlertSerializer(alert).data, status=status.HTTP_200_OK)

        elif action == 'resolve':
            if user.role not in ['doctor', 'staff', 'caretaker'] and alert.student != user:
                return Response({'error': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
            alert.status = 'Resolved'
            alert.resolved_at = timezone.now()
            alert.save()
            return Response(SOSAlertSerializer(alert).data, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny]) # Make it public
def create_admin_once(request):
    """
    A temporary, one-time-use view to create a superuser on Render.
    VISIT THIS URL ONCE, THEN DELETE THIS VIEW AND ITS URL.
    """
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword123')
            return Response(
                {"success": "Superuser 'admin' created with password 'adminpassword123'. NOW DELETE THIS URL AND VIEW."},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": "Admin user 'admin' already exists."},
                status=status.HTTP_200_OK
            )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
import os, requests

@csrf_exempt
@require_POST
def get_turn_credentials(request):
    # Validate Bearer token from header
    auth = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth.startswith('Bearer '):
        return JsonResponse({'error': 'Missing bearer token'}, status=401)
    token_key = auth.split(' ', 1)[1]
    try:
        token = AccessToken(token_key)
        user_id = token.get('user_id')  # optional: can lookup user if needed
    except (TokenError, InvalidToken) as e:
        return JsonResponse({'error': 'Invalid/expired token'}, status=401)

    CLOUDFLARE_ACCOUNT_ID = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
    CLOUDFLARE_API_TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN')
    if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_API_TOKEN:
        return JsonResponse({"error": "Cloudflare credentials not configured on server."}, status=500)

    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/webrtc/credentials"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json",
    }
    body = {"ttl": 14400}  # 4 hours

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data.get('success'):
            return JsonResponse({"error": "Failed to get credentials from Cloudflare"}, status=500)
        result = data['result']
        # return the exact shape Flutter expects
        return JsonResponse({
            "iceServers": result.get("iceServers", []),
            "iceTransportPolicy": result.get("iceTransportPolicy", "all"),
        })
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
