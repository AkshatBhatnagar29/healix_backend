from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, StudentProfile, DoctorProfile, StaffProfile, CaretakerProfile, SOSAlert, Hostel
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

    class Meta:
        model = StudentProfile
        fields = [
            'roll_number', 'name', 'username', 'email', 'date_of_birth',
            'allergies', 'bmi', 'water_intake', 'sleep_hours',
            'hostel_name', 'caretaker_id'
        ]
        read_only_fields = ['roll_number', 'name', 'username', 'email', 'caretaker_id']

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

