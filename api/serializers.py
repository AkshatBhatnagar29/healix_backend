from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, StudentProfile, DoctorProfile, StaffProfile, CaretakerProfile, SOSAlert, Hostel,Prescription, PrescribedMedication
from rest_framework.exceptions import ValidationError

# --- Serializer for Student Profile ---
# class StudentProfileSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source='user.get_full_name', read_only=True)
#     username = serializers.CharField(source='user.username', read_only=True)
#     email = serializers.EmailField(source='user.email', read_only=True)
#     caretaker_id = serializers.CharField(source='hostel.caretaker.username', read_only=True, allow_null=True)
#     hostel_name = serializers.CharField(source='hostel.name', allow_null=True, required=False)

#     class Meta:
#         model = StudentProfile
#         fields = [
#             'roll_number', 'name', 'username', 'email', 'date_of_birth',
#             'allergies', 'bmi', 'water_intake', 'sleep_hours',
#             'hostel_name', 'caretaker_id'
#         ]
#         read_only_fields = ['roll_number', 'name', 'username', 'email', 'caretaker_id']

#     def update(self, instance, validated_data):
#     # Handle nested or flat hostel input
#         hostel_data = validated_data.pop('hostel', None)
#         hostel_name = None

#         # If nested { "hostel": {"name": "..."} } provided
#         if hostel_data and 'name' in hostel_data:
#             hostel_name = hostel_data['name']

#         # If flat field provided directly
#         if 'hostel_name' in self.initial_data:
#             hostel_name = self.initial_data['hostel_name']

#         # Update hostel relation
#         if hostel_name:
#             from .models import Hostel
#             try:
#                 hostel_obj = Hostel.objects.get(name__iexact=hostel_name)
#                 instance.hostel = hostel_obj
#             except Hostel.DoesNotExist:
#                 raise ValidationError({"hostel_name": f"Hostel '{hostel_name}' not found."})
#         else:
#             instance.hostel = None

#         # Update remaining normal fields
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()
#         return instance
class StudentProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    caretaker_id = serializers.CharField(source='hostel.caretaker.username', read_only=True, allow_null=True)
    hostel_name = serializers.CharField(source='hostel.name', allow_null=True, required=False)
    caretaker_phone = serializers.CharField(
        source='hostel.caretaker.caretaker_profile.phone_number', 
        read_only=True, 
        allow_null=True # Returns null if no hostel or caretaker is assigned
    )
    
    # Gets the caretaker's full name for display
    caretaker_name = serializers.CharField(
        source='hostel.caretaker.full_name', # Assumes 'full_name' is on your User model
        read_only=True, 
        allow_null=True
    )
    class Meta:
        model = StudentProfile
        fields = [
            'roll_number', 'name', 'username', 'email', 'date_of_birth',
            'allergies', 'bmi', 'water_intake', 'sleep_hours',
            'bp', 'temperature',
            'hostel_name', 'caretaker_id', 'caretaker_name', 'caretaker_phone'
        ]
        read_only_fields = ['roll_number', 'name', 'username', 'email', 'caretaker_id', 'caretaker_name', 'caretaker_phone']

    def update(self, instance, validated_data):
        print("\n==================== STUDENT PROFILE UPDATE LOG ====================")
        print("Initial data received:", self.initial_data)
        print("Validated data (flat):", validated_data)

        hostel_data = validated_data.pop('hostel', None)
        hostel_name = None

        # Nested hostel data
        if hostel_data and 'name' in hostel_data:
            hostel_name = hostel_data['name']
            print(f"Nested hostel name found: {hostel_name}")

        # Flat hostel_name directly in request
        if 'hostel_name' in self.initial_data:
            hostel_name = self.initial_data['hostel_name']
            print(f"Flat hostel name found: {hostel_name}")

        # Update hostel relation
        if hostel_name:
            from .models import Hostel
            try:
                hostel_obj = Hostel.objects.get(name__iexact=hostel_name)
                instance.hostel = hostel_obj
                print(f"✅ Hostel matched and assigned: {hostel_obj.name}")
            except Hostel.DoesNotExist:
                print(f"❌ Hostel not found: {hostel_name}")
                raise ValidationError({"hostel_name": f"Hostel '{hostel_name}' not found."})
        else:
            print("ℹ️ No hostel provided — setting hostel to None")
            instance.hostel = None

        # Update normal fields
        for attr, value in validated_data.items():
            print(f"Updating field {attr} = {value}")
            setattr(instance, attr, value)

        instance.save()
        print(f"✅ Profile saved successfully for user: {instance.user.username}")
        print("====================================================================\n")

        return instance


# class StudentProfileSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source='user.get_full_name', read_only=True)
#     username = serializers.CharField(source='user.username', read_only=True)
#     email = serializers.EmailField(source='user.email', read_only=True)
#     caretaker_id = serializers.CharField(source='hostel.caretaker.username', read_only=True, allow_null=True)
#     hostel_name = serializers.CharField(source='hostel.name', allow_null=True, required=False)

#     class Meta:
#         model = StudentProfile
#         fields = [
#             'roll_number', 'name', 'username', 'email', 'date_of_birth',
#             'allergies', 'bmi', 'water_intake', 'sleep_hours',
#             'hostel_name', 'caretaker_id'
#         ]
#         read_only_fields = ['roll_number', 'name', 'username', 'email', 'caretaker_id', 'hostel_name']  # Added 'hostel_name'

#     # Your fixed update() method from before (no changes needed here—it uses initial_data)
#     def update(self, instance, validated_data):
#         print("\n==================== STUDENT PROFILE UPDATE LOG ====================")
#         print("Initial data received:", self.initial_data)
#         print("Validated data (flat):", validated_data)

#         # Extract nested hostel from raw initial_data
#         hostel_data = self.initial_data.get('hostel', None)
#         hostel_name = None

#         if hostel_data and isinstance(hostel_data, dict) and 'name' in hostel_data:
#             hostel_name = hostel_data['name']
#             print(f"Nested hostel name found: {hostel_name}")

#         # Flat fallback (now safer since read-only prevents it from hitting validated_data)
#         if not hostel_name and 'hostel_name' in self.initial_data:
#             hostel_name = self.initial_data['hostel_name']
#             print(f"Flat hostel name found: {hostel_name}")

#         # Update hostel relation
#         if hostel_name:
#             from .models import Hostel
#             try:
#                 hostel_obj = Hostel.objects.get(name__iexact=hostel_name)
#                 instance.hostel = hostel_obj
#                 print(f"✅ Hostel matched and assigned: {hostel_obj.name} (Caretaker: {hostel_obj.caretaker.username if hostel_obj.caretaker else 'None'})")
#             except Hostel.DoesNotExist:
#                 print(f"❌ Hostel not found: {hostel_name}")
#                 raise ValidationError({"hostel": f"Hostel '{hostel_name}' not found."})
#         else:
#             print("ℹ️ No hostel provided — setting hostel to None")
#             instance.hostel = None

#         # Update normal fields
#         for attr, value in validated_data.items():
#             print(f"Updating field {attr} = {value}")
#             setattr(instance, attr, value)

#         instance.save()
#         print(f"✅ Profile saved successfully for user: {instance.user.username}")
#         print("====================================================================\n")

#         return instance

# --- Serializer for Doctor Profile ---
class DoctorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            'username', 'email', 'full_name', 'specialization', 
            'experience', 'profile_picture_url'
        ]
        read_only_fields = ['username', 'email', 'full_name']

# --- Serializer for Caretaker Profile ---
class CaretakerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    hostel_assigned = serializers.SerializerMethodField()

    class Meta:
        model = CaretakerProfile
        fields = [
            'username', 'email', 'full_name',
            'employee_id', 'phone_number', 'hostel_assigned'
        ]
        read_only_fields = ['username', 'email', 'full_name', 'hostel_assigned']

    def get_hostel_assigned(self, obj):
        # obj is CaretakerProfile, obj.user is the User
        hostels = obj.user.hostel_set.all()
        if not hostels.exists():
            return "Not Assigned"
        return ", ".join([hostel.name for hostel in hostels])

# --- Serializer for (Other) Staff Profile ---
class StaffProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = StaffProfile
        fields = ['username', 'email', 'full_name', 'employee_id', 'phone_number', 'department']
        read_only_fields = ['username', 'email', 'full_name']

# --- Serializer for User Signup ---
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'full_name', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
        }

    def create(self, validated_data):
        full_name = validated_data.pop('full_name', '')
        first_name = full_name.split(' ')[0]
        last_name = ' '.join(full_name.split(' ')[1:]) if ' ' in full_name else ''

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name,
            role=validated_data['role'],
            is_active=False # Change to True if not using OTP
        )

        role = validated_data['role']
        if role == 'student':
            StudentProfile.objects.create(user=user, roll_number=user.username)
        elif role == 'doctor':
            DoctorProfile.objects.create(user=user)
        elif role == 'caretaker':
            CaretakerProfile.objects.create(user=user, employee_id=user.username)
        elif role == 'staff':
            StaffProfile.objects.create(user=user, employee_id=user.username)

        # send_otp_email(user) # Uncomment to enable OTP
        return user

# --- Serializer for SOS Alerts ---
class SOSAlertSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_roll_number = serializers.CharField(source='student.student_profile.roll_number', read_only=True)
    hostel_name = serializers.CharField(source='student.student_profile.hostel.name', read_only=True, allow_null=True)
    hostel_id = serializers.CharField(source='student.student_profile.hostel.id', read_only=True, allow_null=True)
    caretaker_name = serializers.CharField(source='student.student_profile.hostel.caretaker.get_full_name', read_only=True, allow_null=True)
    caretaker_phone = serializers.CharField(source='student.student_profile.hostel.caretaker.caretaker_profile.phone_number', read_only=True, allow_null=True)
    acknowledged_by_name = serializers.CharField(source='acknowledged_by.get_full_name', read_only=True, allow_null=True)
    caretaker_id = serializers.CharField(source='student.student_profile.hostel.caretaker.username', read_only=True, allow_null=True)
    
    class Meta:
        model = SOSAlert
        fields = [
            'id', 'status', 'alert_time', 'location_info',
            'student_name', 'student_roll_number','hostel_name', 'hostel_id',
            'caretaker_name', 'caretaker_phone', 'acknowledged_by_name','caretaker_id'
        ]
        read_only_fields = [
            'id', 'status', 'alert_time', 'student_name', 'student_roll_number',
            'hostel_name', 'hostel_id', 'caretaker_name', 'caretaker_phone',
            'acknowledged_by_name', 'caretaker_id'
        ]

# --- Serializer for Secure Login ---
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_email_verified:
            raise serializers.ValidationError({
                'detail': 'Email not verified. Please check your email for an OTP.'
            })
        return data

# In api/serializers.py
# Make sure to import Appointment at the top
from .models import Appointment, User # ... and your other models

# In api/serializers.py

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Appointment, DoctorSchedule, User # Import models

# ... (Your other serializers like StudentProfileSerializer, etc.) ...

# --- THIS IS THE APPOINTMENT BOOKING SERIALIZER ---

class AppointmentCreateSerializer(serializers.ModelSerializer):
    """
    Handles the creation of a new appointment.
    The 'student' is set automatically from the logged-in user.
    """
    # Accepts the doctor's username, which is what the Flutter code has (doctor.id)
    doctor = serializers.SlugRelatedField(
        queryset=User.objects.filter(role='doctor'), 
        slug_field='username'
    )
    
    # Automatically sets the student from the logged-in user
    student = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
    
    class Meta:
        model = Appointment
        # 'status' will use the model's default ('Upcoming')
        fields = ['doctor', 'appointment_time', 'reason', 'student'] 
    
    def validate(self, data):
        # 1. Ensure the user booking is a student
        if self.context['request'].user.role != 'student':
             raise ValidationError("Only students can book appointments.")

        # 2. Basic validation to prevent double-booking the *exact* same slot
        doctor = data.get('doctor')
        time = data.get('appointment_time')

        if Appointment.objects.filter(doctor=doctor, appointment_time=time, status='Upcoming').exists():
            raise ValidationError("This time slot is no longer available. Please select another.")

        return data

# --- OTHER SERIALIZERS FOR APPOINTMENT SYSTEM ---

class DoctorScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for managing a doctor's weekly schedule.
    """
    doctor_username = serializers.CharField(source='doctor.username', read_only=True)

    class Meta:
        model = DoctorSchedule
        fields = ['id', 'doctor', 'doctor_username', 'day_of_week', 'start_time', 'end_time']
        read_only_fields = ['doctor_username']

# class AppointmentListSerializer(serializers.ModelSerializer):
#     """
#     Serializer for listing appointments, showing student details.
#     """
#     # Get student's full name from the 'student' (User) object
#     student_name = serializers.CharField(source='student.get_full_name', read_only=True)
#     student_id = serializers.CharField(source='student.username', read_only=True)
    
#     # Format the time for easier use on the frontend
#     appointment_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

#     class Meta:
#         model = Appointment
#         fields = [
#             'id', 
#             'student_name', 
#             'student_id',
#             'appointment_time', 
#             'reason', 
#             'status'
#         ]
class AppointmentListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_id = serializers.CharField(source='student.username', read_only=True)
    
    # --- ADD THESE TWO FIELDS ---
    student_bp = serializers.CharField(source='student.student_profile.bp', read_only=True, allow_null=True)
    student_temp = serializers.FloatField(source='student.student_profile.temperature', read_only=True, allow_null=True)
    # ----------------------------

    appointment_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Appointment
        fields = [
            'id', 
            'student_name', 
            'student_id',
            'student_bp',    # <--- Include in fields
            'student_temp',  # <--- Include in fields
            'appointment_time', 
            'reason', 
            'status'
        ]
class PrescribedMedicationSerializer(serializers.ModelSerializer):
    """ Serializer for a single line of medication """
    class Meta:
        model = PrescribedMedication
        fields = ['id', 'name', 'dosage', 'frequency', 'duration']
        read_only_fields = ['id']

class PrescriptionDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing a prescription with all its medications.
    """
    # Use the serializer above to show a nested list of medications
    medications = PrescribedMedicationSerializer(many=True, read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    appointment_time = serializers.DateTimeField(source='appointment.appointment_time', read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id', 'appointment', 'doctor', 'student', 'issue_date', 'general_notes', 
            'medications', 'doctor_name', 'student_name', 'appointment_time'
        ]

class PrescriptionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for CREATING a prescription.
    Accepts a nested list of medications.
    """
    # This 'write-only' field accepts a list of medication objects
    medications = PrescribedMedicationSerializer(many=True, write_only=True)
    
    class Meta:
        model = Prescription
        fields = ['id', 'appointment', 'general_notes', 'medications']

    def create(self, validated_data):
        # Pop the nested medication data
        medications_data = validated_data.pop('medications')
        
        # Get the appointment object
        appointment = validated_data.get('appointment')
        
        # Manually set the doctor and student from the appointment
        validated_data['doctor'] = appointment.doctor
        validated_data['student'] = appointment.student
        
        # Create the main Prescription "folder"
        prescription = Prescription.objects.create(**validated_data)
        
        # Create each PrescribedMedication object and link it to the prescription
        for med_data in medications_data:
            PrescribedMedication.objects.create(prescription=prescription, **med_data)
            
        return prescription
    
# In api/serializers.py
# ... (Import StudentProfile, User, and DoctorSchedule at the top)

# --- ⭐️ ADD THIS NEW SERIALIZER ⭐️ ---
class StaffStudentVitalsSerializer(serializers.ModelSerializer):
    """
    Serializer for Staff to update a student's vitals.
    We only expose the fields staff should be able to edit.
    """
    class Meta:
        model = StudentProfile
        fields = ['bmi', 'water_intake', 'sleep_hours','bp', 'temperature']

# --- ⭐️ ADD THIS NEW SERIALIZER ⭐️ ---
class DoctorListSerializer(serializers.ModelSerializer):
    """
    A simple serializer to list doctors for a dropdown menu.
    """
    full_name = serializers.CharField(source='get_full_name')
    class Meta:
        model = User
        fields = ['username', 'full_name']

# --- ⭐️ ADD/RE-ADD THIS SERIALIZER ⭐️ ---
class DoctorScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for managing a doctor's weekly schedule.
    """
    doctor_username = serializers.CharField(source='doctor.username', read_only=True)
    
    # We need 'doctor' to be a writeable username field
    doctor = serializers.SlugRelatedField(
        queryset=User.objects.filter(role='doctor'),
        slug_field='username'
    )

    class Meta:
        model = DoctorSchedule
        fields = ['id', 'doctor', 'doctor_username', 'day_of_week', 'start_time', 'end_time']
        read_only_fields = ['id', 'doctor_username']