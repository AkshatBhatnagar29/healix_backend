



from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    # ... (Your existing UserManager is fine) ...
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        # Your superuser should probably have a role, e.g., 'staff'
        extra_fields.setdefault('role', 'staff') 
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    # --- THIS IS THE FIX ---
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('doctor', 'Doctor'),
        ('caretaker', 'Caretaker'), # New distinct role
        ('staff', 'Staff'),       # For other staff (lab, pharmacy)
    )
    # --- END FIX ---
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_email_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class Hostel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # --- THIS IS THE FIX ---
    # Now it *only* accepts users with the 'caretaker' role
    caretaker = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'role': 'caretaker'}, # Changed from 'staff'
        related_name='hostel_set' # Use 'hostel_set' to get hostels from a user
    )
    # --- END FIX ---

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student_profile', limit_choices_to={'role': 'student'})
    roll_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    allergies = models.TextField(blank=True, null=True)
    bmi = models.FloatField(null=True, blank=True)
    water_intake = models.FloatField(null=True, blank=True)
    sleep_hours = models.FloatField(null=True, blank=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='doctor_profile', limit_choices_to={'role': 'doctor'})
    specialization = models.CharField(max_length=100, blank=True, null=True)
    experience = models.PositiveIntegerField(null=True, blank=True)
    profile_picture_url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

# --- NEW MODEL for Caretakers ---
class CaretakerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='caretaker_profile', limit_choices_to={'role': 'caretaker'})
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

# --- RENAMED from StaffProfile ---
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='staff_profile', limit_choices_to={'role': 'staff'})
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True) # e.g., "Pharmacy"

    def __str__(self):
        return self.user.username

class SOSAlert(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    alert_time = models.DateTimeField(auto_now_add=True)
    location_info = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Acknowledged', 'Acknowledged'), ('Resolved', 'Resolved')], default='Active')
    
    
    acknowledged_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='acknowledged_alerts', 
        limit_choices_to={'role__in': ['doctor', 'staff', 'caretaker']} 
    )
    
    
    resolved_at = models.DateTimeField(null=True, blank=True)
class Appointment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_student')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_doctor')
    appointment_time = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Upcoming', 'Upcoming'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    created_at = models.DateTimeField(auto_now_add=True)

# In api/models.py
# ... (at the end, after your other models like DoctorSchedule, etc.)

class Prescription(models.Model):
    """
    Represents a single prescription event, linked to an appointment.
    This acts as a "folder" for all medications prescribed during that visit.
    """
    # Link to the specific appointment
    appointment = models.OneToOneField(
        Appointment, 
        on_delete=models.CASCADE, 
        related_name='prescription'
    )
    # The doctor who issued it (denormalized for easy lookup)
    doctor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='issued_prescriptions',
        limit_choices_to={'role': 'doctor'}
    )
    # The student who received it (denormalized for easy lookup)
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        limit_choices_to={'role': 'student'}
    )
    # General notes from the doctor
    general_notes = models.TextField(blank=True, null=True)
    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.student.username} from {self.issue_date.date()}"

class PrescribedMedication(models.Model):
    """
    Represents a single medication line item within a Prescription.
    """
    prescription = models.ForeignKey(
        Prescription, 
        on_delete=models.CASCADE, 
        related_name='medications'
    )
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100, blank=True, help_text="e.g., 500mg or 1 tablet")
    frequency = models.CharField(max_length=100, blank=True, help_text="e.g., Twice a day")
    duration = models.CharField(max_length=100, blank=True, help_text="e.g., 7 days")

    def __str__(self):
        return f"{self.name} ({self.dosage})"

class LabReport(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lab_reports')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordered_lab_reports')
    test_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Ready', 'Ready')])
    report_file_url = models.CharField(max_length=255, blank=True, null=True)
    ordered_at = models.DateTimeField(auto_now_add=True)

class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'doctor'},
        related_name='schedule'
    )
    day_of_week = models.IntegerField(
        choices=[
            (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), 
            (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        # A doctor can only have one entry for a specific day
        unique_together = ('doctor', 'day_of_week')

    def __str__(self):
        return f"{self.doctor.username} - {self.get_day_of_week_display()}"
