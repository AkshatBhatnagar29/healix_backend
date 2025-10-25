# from django.contrib.auth.models import AbstractUser
# from django.db import models

# # 1. User Model: The central hub for all user types.
# # It uses Django's built-in first_name and last_name fields.
# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('student', 'Student'),
#         ('doctor', 'Doctor'),
#         ('staff', 'Staff'),
#     )
    
#     # We remove the custom 'full_name' field from the model.
#     # We will use Django's built-in first_name and last_name fields instead.
    
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
#     # Fields for OTP verification
#     is_email_verified = models.BooleanField(default=False)
#     otp_code = models.CharField(max_length=6, null=True, blank=True)
#     otp_expiry = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return self.username

# # 2. Profile Models: To hold role-specific information.
# class StudentProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student_profile')
#     roll_number = models.CharField(max_length=50, unique=True)
#     hostel_details = models.CharField(max_length=100, blank=True, null=True)
#     date_of_birth = models.DateField(blank=True, null=True)
#     allergies = models.TextField(blank=True, null=True)
#     bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
#     water_intake = models.IntegerField(null=True, blank=True)
#     sleep_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

#     def __str__(self):
#         return self.user.username

# class DoctorProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='doctor_profile')
#     specialization = models.CharField(max_length=100, blank=True, null=True)
#     experience = models.IntegerField(null=True, blank=True)
#     profile_picture_url = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return self.user.username

# # 3. Core Feature Models
# class Appointment(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_student')
#     doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_doctor')
#     appointment_time = models.DateTimeField()
#     reason = models.TextField(blank=True, null=True)
#     status = models.CharField(max_length=20, choices=[('Upcoming', 'Upcoming'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
#     created_at = models.DateTimeField(auto_now_add=True)

# class Prescription(models.Model):
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
#     medication_details = models.JSONField(null=True, blank=True)
#     follow_up_notes = models.TextField(blank=True, null=True)
#     issued_at = models.DateTimeField(auto_now_add=True)

# class LabReport(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lab_reports')
#     doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordered_lab_reports')
#     test_name = models.CharField(max_length=200)
#     status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Ready', 'Ready')])
#     report_file_url = models.CharField(max_length=255, blank=True, null=True)
#     ordered_at = models.DateTimeField(auto_now_add=True)

# class SOSAlert(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     alert_time = models.DateTimeField(auto_now_add=True)
#     location_info = models.CharField(max_length=255, blank=True, null=True)
#     status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Acknowledged', 'Acknowledged'), ('Resolved', 'Resolved')])
#     acknowledged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='acknowledged_alerts')




from django.contrib.auth.models import AbstractUser
from django.db import models

# 1. User Model: The central hub for all user types.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff'), # Caretakers will use this role
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_email_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

# 2. Profile and related Models: To hold role-specific information.

class Hostel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    caretaker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'staff'})

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student_profile')
    roll_number = models.CharField(max_length=50, unique=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True, blank=True) # Link student to a hostel
    date_of_birth = models.DateField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    water_intake = models.IntegerField(null=True, blank=True)
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.user.username

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='doctor_profile')
    specialization = models.CharField(max_length=100, blank=True, null=True)
    experience = models.IntegerField(null=True, blank=True)
    profile_picture_url = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.user.username

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='staff_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


# 3. Core Feature Models
class SOSAlert(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    alert_time = models.DateTimeField(auto_now_add=True)
    location_info = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Acknowledged', 'Acknowledged'), ('Resolved', 'Resolved')], default='Active')
    acknowledged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='acknowledged_alerts', limit_choices_to={'role__in': ['doctor', 'staff']})
    resolved_at = models.DateTimeField(null=True, blank=True)

# ... Other models like Appointment, Prescription, etc. remain the same ...
class Appointment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_student')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_doctor')
    appointment_time = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Upcoming', 'Upcoming'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    created_at = models.DateTimeField(auto_now_add=True)

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medication_details = models.JSONField(null=True, blank=True)
    follow_up_notes = models.TextField(blank=True, null=True)
    issued_at = models.DateTimeField(auto_now_add=True)

class LabReport(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lab_reports')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordered_lab_reports')
    test_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Ready', 'Ready')])
    report_file_url = models.CharField(max_length=255, blank=True, null=True)
    ordered_at = models.DateTimeField(auto_now_add=True)

