from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Import all your new models here
from .models import (
    User, Hostel, StudentProfile, DoctorProfile, StaffProfile, 
    CaretakerProfile, SOSAlert, Appointment, Prescription, 
    PrescribedMedication, LabReport, DoctorSchedule
)

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'caretaker')
    raw_id_fields = ('caretaker',)

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'hostel', 'bp', 'temperature')
    raw_id_fields = ('user', 'hostel')

class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department')
    raw_id_fields = ('user',)

class CaretakerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'phone_number')
    raw_id_fields = ('user',)

# --- ⭐️ NEW: Appointment Admin ---
class AppointmentAdmin(admin.ModelAdmin):
    # Columns to show in the list
    list_display = ('student', 'doctor', 'appointment_time', 'status', 'created_at')
    
    # Sidebar filters
    list_filter = ('status', 'appointment_time', 'doctor')
    
    # Search bar (Search by student name, roll no, or doctor name)
    search_fields = ('student__username', 'student__first_name', 'doctor__username', 'reason')
    
    # Helper to pick users without loading a massive dropdown
    raw_id_fields = ('student', 'doctor')
    
    # Default ordering (newest appointments first)
    ordering = ('-appointment_time',)

# --- ⭐️ NEW: Doctor Schedule Admin ---
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'doctor')
    raw_id_fields = ('doctor',)

# --- ⭐️ NEW: Prescription Admin (with inline medications) ---
class PrescribedMedicationInline(admin.TabularInline):
    model = PrescribedMedication
    extra = 1

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'student', 'issue_date')
    raw_id_fields = ('doctor', 'student', 'appointment')
    inlines = [PrescribedMedicationInline] # Allows editing meds directly inside the prescription

# --- ⭐️ NEW: Lab Report Admin ---
class LabReportAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'student', 'doctor', 'status', 'ordered_at')
    list_filter = ('status',)
    raw_id_fields = ('student', 'doctor')


# --- Register Models ---
admin.site.register(User, CustomUserAdmin)
admin.site.register(Hostel, HostelAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(CaretakerProfile, CaretakerProfileAdmin)
admin.site.register(DoctorProfile)
admin.site.register(SOSAlert)

# Register the new features
admin.site.register(Appointment, AppointmentAdmin)       # <--- Appointment Table
admin.site.register(DoctorSchedule, DoctorScheduleAdmin) # <--- Schedule Table
admin.site.register(Prescription, PrescriptionAdmin)     # <--- Prescription Table
admin.site.register(LabReport, LabReportAdmin)           # <--- Lab Report Table