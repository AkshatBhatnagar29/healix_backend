from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import (
    DoctorProfile, StaffProfile, StudentProfile, CaretakerProfile, 
    Hostel, User, SOSAlert,DoctorSchedule, Appointment,Prescription
)
from rest_framework import serializers
# import datetime
from django.db import IntegrityError
# from .serializers import 
from datetime import datetime, timedelta
from .serializers import (
    DoctorProfileSerializer, StaffProfileSerializer, StudentProfileSerializer,
    CaretakerProfileSerializer, UserSerializer, MyTokenObtainPairSerializer, 
    SOSAlertSerializer,AppointmentCreateSerializer, AppointmentListSerializer,PrescriptionDetailSerializer, PrescriptionCreateSerializer, StaffStudentVitalsSerializer,DoctorListSerializer,DoctorScheduleSerializer,UserSerializer
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

# class SignupView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]
#     def perform_create(self, serializer):
#         user = serializer.save(is_active=False) 
#         send_otp_email(user) # Send OTP on signup
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        try:
            # Attempt to save the user (which calls User.objects.create_user)
            user = serializer.save(is_active=False) 
            
            # If successful, send the email
            send_otp_email(user)
            
        except IntegrityError:
            # If the database returns a duplicate key error (for username or email)
            # We raise a DRF ValidationError, which automatically translates to a 
            # 400 Bad Request error response with the correct message.
            
            # Note: This is a general catch. If you only want to check the username:
            raise serializers.ValidationError({"username": "A user with this username already exists."})
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

import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings

# In api/views.py

import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# --- This is the corrected view ---
# In api/views.py

import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# --- THIS IS THE CORRECT VERSION FOR OUR SETUP ---

# In api/views.py

import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# --- THIS IS THE CORRECT VERSION, MATCHING YOUR DOCS ---

@api_view(['POST']) # It MUST be a POST request
@permission_classes([IsAuthenticated])
def get_turn_credentials(request):
    
    # 1. Get the new keys from settings
    TURN_ID = settings.TURN_ID
    TURN_API_TOKEN = settings.TURN_API_TOKEN

    if not TURN_ID or not TURN_API_TOKEN:
        return Response({"error": "TURN keys not configured on server."}, status=500)

    # 2. This is the new, correct API endpoint
    url = f"https://rtc.live.cloudflare.com/v1/turn/keys/{TURN_ID}/credentials/generate-ice-servers"

    # 3. Use the new "Authorization: Bearer" header
    headers = {
        "Authorization": f"Bearer {TURN_API_TOKEN}",
        "Content-Type": "application/json",
    }

    # 4. A POST request is required to set the TTL
    body = {"ttl": 14400} # 4-hour time to live

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status() # Raise an error for bad responses (4xx/5xx)
        
        data = response.json()
        
        # 5. Check for success and return the 'result'
        # The new API returns the iceServers directly, not nested in a 'result' key
        # We just return the whole successful response.
        return Response(data)

    except requests.exceptions.RequestException as e:
        response_text = e.response.text if e.response else "No response"
        return Response({"error": str(e), "response_text": response_text}, status=500)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_slots(request, username, date_str):
    """
    Calculates and returns a list of available 1-hour time slots
    for a specific doctor on a specific date.
    
    Args:
        username (str): The username of the doctor.
        date_str (str): The date in 'YYYY-MM-DD' format.
    """
    
    # 1. Validate the Doctor
    try:
        doctor = User.objects.get(username=username, role='doctor')
    except User.DoesNotExist:
        return Response(
            {"error": "Doctor not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )

    # 2. Validate the Date
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if date < timezone.now().date():
            return Response(
                {"error": "Cannot book appointments in the past."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    except ValueError:
        return Response(
            {"error": "Invalid date format. Use YYYY-MM-DD."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # 3. Find the Doctor's Schedule for that day
    # (1=Monday, 2=Tuesday, ... 7=Sunday)
    day_of_week = date.weekday() + 1 
    
    try:
        schedule = DoctorSchedule.objects.get(
            doctor=doctor, 
            day_of_week=day_of_week
        )
    except DoctorSchedule.DoesNotExist:
        # Doctor does not work on this day
        return Response([], status=status.HTTP_200_OK) 

    # 4. Find all existing 'Upcoming' appointments for that doctor on that day
    existing_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_time__date=date,
        status='Upcoming'
    )
    
    # Create a set of booked times for fast lookup
    # e.g., {datetime.time(10, 0), datetime.time(14, 0)}
    booked_times = {apt.appointment_time.time() for apt in existing_appointments}

    # 5. Generate all possible 1-hour slots and filter out booked ones
    available_slots = []
    slot_duration = timedelta(hours=1)
    
    # Combine the date with the schedule's start time
    current_slot_start = datetime.combine(date, schedule.start_time)
    # Combine the date with the schedule's end time
    end_time_datetime = datetime.combine(date, schedule.end_time)

    while current_slot_start < end_time_datetime:
        # Check if this slot's time is in our 'booked_times' set
        if current_slot_start.time() not in booked_times:
            # Format it nicely for the frontend (e.g., "09:00 AM")
            available_slots.append(current_slot_start.strftime('%I:%M %p'))
        
        # Move to the next slot
        current_slot_start += slot_duration

    return Response(available_slots, status=status.HTTP_200_OK)


class DoctorAppointmentListView(generics.ListAPIView):
    """
    Lists all appointments (upcoming and past) for the
    currently logged-in doctor.
    """
    serializer_class = AppointmentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the currently logged-in user
        user = self.request.user

        if user.role != 'doctor':
            # You can also raise a PermissionDenied error
            return Appointment.objects.none()

        # Return all appointments for this doctor, ordered by time
        # Use 'select_related' for efficiency to avoid N+1 queries
        return Appointment.objects.filter(doctor=user) \
                                .select_related('student') \
                                .order_by('-appointment_time')
class AppointmentCreateView(generics.CreateAPIView):
    """
    Creates a new appointment for the logged-in student.
    Matches: POST /api/appointments/create/
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class PrescriptionCreateView(generics.CreateAPIView):
   
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Check if user is a doctor
        if request.user.role != 'doctor':
            return Response(
                {"error": "Only doctors can issue prescriptions."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if a prescription for this appointment already exists (OneToOne)
        appointment_id = request.data.get('appointment')
        if Prescription.objects.filter(appointment__id=appointment_id).exists():
             return Response(
                {"error": "A prescription for this appointment already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

class StudentPrescriptionListView(generics.ListAPIView):
    """
    Student: Get a list of all their past prescriptions.
    GET /api/prescriptions/student/
    """
    serializer_class = PrescriptionDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only prescriptions for the logged-in student
        return Prescription.objects.filter(student=self.request.user) \
            .select_related('doctor', 'student', 'appointment') \
            .prefetch_related('medications') \
            .order_by('-issue_date')

class AppointmentPrescriptionDetailView(generics.RetrieveAPIView):
    """
    Doctor/Student: Get the prescription for a single appointment.
    GET /api/prescriptions/appointment/<int:appointment_id>/
    """
    serializer_class = PrescriptionDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Prescription.objects.all()
    lookup_field = 'appointment__id'
    lookup_url_kwarg = 'appointment_id'

    def get_object(self):
        # Check permissions
        obj = super().get_object()
        user = self.request.user
        if obj.student == user or obj.doctor == user:
            return obj
        raise permissions.PermissionDenied("You do not have access to this prescription.")
    

# In api/views.py
# ... (Import StudentProfile, DoctorSchedule, DoctorScheduleSerializer, etc.)

class StaffStudentVitalsUpdateView(generics.RetrieveUpdateAPIView):
    """
    Allows staff to retrieve and update a student's vitals.
    RESTRICTION: Access is ONLY allowed if the student has an 'Upcoming' appointment TODAY.
    """
    queryset = StudentProfile.objects.all()
    serializer_class = StaffStudentVitalsSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'user__username' 
    lookup_url_kwarg = 'username'

    def check_permissions(self, request):
        super().check_permissions(request)
        if request.user.role != 'staff':
            self.permission_denied(request, message="Only staff can access this.")

    def get_object(self):
        # 1. Retrieve the StudentProfile using the standard lookup (username)
        # This will raise 404 if the student doesn't exist.
        student_profile = super().get_object()
        
        # 2. Perform the Appointment Check
        student_user = student_profile.user
        today = timezone.now().date()

        has_appointment = Appointment.objects.filter(
            student=student_user,
            status='Upcoming',
            appointment_time__date=today
        ).exists()

        # 3. If no appointment today, deny access entirely (403 Forbidden)
        if not has_appointment:
            raise PermissionDenied(
                "Access Denied: You can only view or update vitals if the student has an appointment scheduled for today."
            )

        return student_profile

# --- ⭐️ ADD THIS NEW VIEW ⭐️ ---
class DoctorListForStaffView(generics.ListAPIView):
    """
    Provides a simple list of all doctors for staff UI.
    """
    queryset = User.objects.filter(role='doctor')
    serializer_class = DoctorListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)
        if request.user.role != 'staff':
            self.permission_denied(request, message="Only staff can access this.")

# --- ⭐️ ADD/RE-ADD THIS VIEW ⭐️ ---
class StaffScheduleUpdateView(generics.CreateAPIView):
    """
    View for Staff to create or update a doctor's schedule for a day.
    """
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != 'staff':
            return Response({"error": "Only staff are authorized to update schedules."}, status=status.HTTP_403_FORBIDDEN)
        
        doctor_username = request.data.get('doctor')
        day_of_week = request.data.get('day_of_week')
        
        try:
            doctor = User.objects.get(username=doctor_username, role='doctor')
        except User.DoesNotExist:
            return Response({"error": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)

        # Use get_or_create to handle updates
        schedule_instance, created = DoctorSchedule.objects.get_or_create(
            doctor=doctor,
            day_of_week=day_of_week,
            defaults={
                'start_time': request.data.get('start_time'), 
                'end_time': request.data.get('end_time')
            }
        )
        
        # If it wasn't created, it means we update it
        if not created:
            serializer = self.get_serializer(schedule_instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(schedule_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AvailableDoctorListView(generics.ListAPIView):
    """
    Lists doctors who are scheduled to work *today*.
    Matches: GET /api/doctors/list-available/
    """
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        # Get today's day of the week 
        # (1=Monday, 7=Sunday to match your model)
        current_day = timezone.now().weekday() + 1 
        
        # Find all doctor IDs scheduled to work today
        scheduled_doctor_ids = DoctorSchedule.objects.filter(
            day_of_week=current_day
        ).values_list('doctor_id', flat=True).distinct()

        # Return the profiles of those doctors
        queryset = DoctorProfile.objects.filter(
            user__id__in=scheduled_doctor_ids
        ).select_related('user')
        
        return queryset