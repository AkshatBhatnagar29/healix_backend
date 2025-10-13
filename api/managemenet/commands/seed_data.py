from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# Get the custom User model
User = get_user_model()

class Command(BaseCommand):
    help = 'Creates dummy data for the Healix application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting existing users...')
        # Clear existing users to start fresh (optional, but good for testing)
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write('Creating new users...')

        # --- Create a Dummy Doctor ---
        if not User.objects.filter(username='dr_wilson').exists():
            doctor = User.objects.create_user(
                username='dr_wilson',
                email='doctor@healix.com',
                password='password123',
                first_name='Sarah',
                last_name='Wilson',
                role='doctor',
                is_active=True,
                is_email_verified=True,
                is_staff=True # Allows login to Django admin
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created Doctor: {doctor.username}'))

        # --- Create a Dummy Student ---
        if not User.objects.filter(username='102303158').exists():
            student = User.objects.create_user(
                username='102303158',
                email='student@healix.com',
                password='password123',
                first_name='Akshat',
                last_name='Bhatnagar',
                role='student',
                is_active=True,
                is_email_verified=True
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created Student: {student.username}'))

        # --- Create a Dummy Staff Member ---
        if not User.objects.filter(username='staff_01').exists():
            staff = User.objects.create_user(
                username='staff_01',
                email='staff@healix.com',
                password='password123',
                first_name='John',
                last_name='Smith',
                role='staff',
                is_active=True,
                is_email_verified=True
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created Staff: {staff.username}'))