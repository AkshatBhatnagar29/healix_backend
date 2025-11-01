from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Hostel, StudentProfile, DoctorProfile, StaffProfile, CaretakerProfile, SOSAlert

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    # This will automatically pick up the new ROLE_CHOICES from your model
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
    list_display = ('user', 'roll_number', 'hostel')
    raw_id_fields = ('user', 'hostel')

class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department')
    raw_id_fields = ('user',)

class CaretakerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'phone_number')
    raw_id_fields = ('user',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Hostel, HostelAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(CaretakerProfile, CaretakerProfileAdmin) # <-- ADD THIS
admin.site.register(DoctorProfile)
admin.site.register(SOSAlert)

