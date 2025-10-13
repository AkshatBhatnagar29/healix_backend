from django.contrib import admin
from .models import User, StudentProfile, DoctorProfile, StaffProfile, Hostel, SOSAlert, Appointment

# This makes your models visible and editable in the admin panel.

# We can customize how models are displayed. For example, for the User model,
# we can display the role in the list view.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'hostel')
    search_fields = ('user__username', 'roll_number')

class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'phone_number')
    search_fields = ('user__username', 'employee_id')

class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'caretaker')
    search_fields = ('name', 'caretaker__username')

class SOSAlertAdmin(admin.ModelAdmin):
    list_display = ('student', 'status', 'alert_time', 'acknowledged_by')
    list_filter = ('status',)
    search_fields = ('student__username',)


# Register your models here
admin.site.register(User, UserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(DoctorProfile)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(Hostel, HostelAdmin)
admin.site.register(SOSAlert, SOSAlertAdmin)
admin.site.register(Appointment)
