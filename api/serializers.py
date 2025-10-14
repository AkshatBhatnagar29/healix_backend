# from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from .models import User, StudentProfile, DoctorProfile

# # --- Serializer for User Signup ---
# class UserSerializer(serializers.ModelSerializer):
#     # We add a write_only full_name field to accept it from the frontend
#     full_name = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         # The fields now reflect the database schema: first_name and last_name
#         fields = ['id', 'username', 'email', 'password', 'role', 'full_name', 'first_name', 'last_name']
#         extra_kwargs = {
#             'password': {'write_only': True},
#             # Make first_name and last_name read-only as we will set them in the create method
#             'first_name': {'read_only': True},
#             'last_name': {'read_only': True},
#         }

#     def create(self, validated_data):
#         # This method is called when a new user signs up
        
#         # Split the incoming full_name into first and last names
#         full_name = validated_data.get('full_name', '')
#         first_name = full_name.split(' ')[0]
#         last_name = ' '.join(full_name.split(' ')[1:]) if ' ' in full_name else ''

#         # Create the main User object using the correct fields
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password'],
#             first_name=first_name, # Use the split first_name
#             last_name=last_name,   # Use the split last_name
#             role=validated_data['role'],
#             is_active=False # User is inactive until their email is verified
#         )

#         # Now, create the corresponding profile based on the selected role
#         if validated_data['role'] == 'student':
#             # For a student, the username (Student ID) is used as the roll number
#             StudentProfile.objects.create(user=user, roll_number=user.username)
#         elif validated_data['role'] == 'doctor':
#             DoctorProfile.objects.create(user=user)
#         # Add a similar block for 'staff' if you create a StaffProfile model

#         return user

# # --- Serializer for Secure Login ---
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         # Add custom claims to the token (data you want to be easily accessible on the frontend)
#         token['username'] = user.username
#         token['role'] = user.role
#         return token

#     def validate(self, attrs):
#         # Default validation first
#         data = super().validate(attrs)
        
#         # Add our custom security check
#         if not self.user.is_email_verified:
#             raise serializers.ValidationError({
#                 'detail': 'Email not verified. Please check your email for an OTP to activate your account.'
#             })
            
#         return data






from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, StudentProfile, DoctorProfile, StaffProfile, SOSAlert

# --- NEW: Serializer for Student Profile ---
class StudentProfileSerializer(serializers.ModelSerializer):
    # Add user-related fields from the linked User model
    name = serializers.CharField(source='user.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'name',
            'username',
            'email',
            'roll_number',
            'hostel_details',
            'date_of_birth',
            'allergies',
            'bmi',
            'water_intake',
            'sleep_hours'
        ]
        read_only_fields = ['roll_number', 'name', 'username', 'email']

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
        full_name = validated_data.get('full_name', '')
        first_name = full_name.split(' ')[0]
        last_name = ' '.join(full_name.split(' ')[1:]) if ' ' in full_name else ''

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name,
            role=validated_data['role'],
            is_active=False
        )

        role = validated_data['role']
        if role == 'student':
            StudentProfile.objects.create(user=user, roll_number=user.username)
        elif role == 'doctor':
            DoctorProfile.objects.create(user=user)
        elif role == 'staff':
            StaffProfile.objects.create(user=user, employee_id=user.username)

        return user

# --- SOS Alert Serializer (NEW) ---
# This serializer is designed to give the frontend all the info it needs in one call.
class SOSAlertSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_roll_number = serializers.CharField(source='student.student_profile.roll_number', read_only=True)
    hostel_name = serializers.CharField(source='student.student_profile.hostel.name', read_only=True)
    caretaker_name = serializers.CharField(source='student.student_profile.hostel.caretaker.get_full_name', read_only=True)
    caretaker_phone = serializers.CharField(source='student.student_profile.hostel.caretaker.staff_profile.phone_number', read_only=True)
    acknowledged_by_name = serializers.CharField(source='acknowledged_by.get_full_name', read_only=True)

    class Meta:
        model = SOSAlert
        fields = [
            'id', 'status', 'alert_time', 'location_info',
            'student_name', 'student_roll_number', 'hostel_name',
            'caretaker_name', 'caretaker_phone', 'acknowledged_by_name'
        ]

# --- Serializer for Secure Login ---
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['role'] = user.role # This is crucial for role-based navigation on the frontend
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_email_verified:
            raise serializers.ValidationError({
                'detail': 'Email not verified. Please check your email for an OTP.'
            })
        return data