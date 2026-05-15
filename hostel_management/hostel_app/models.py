from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile for hostel admin role management."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_hostel_admin = models.BooleanField(default=False)
    admin_role_choices = [
        ('super_admin', 'Super Admin'),
        ('hostel_manager', 'Hostel Manager'),
        ('attendance_manager', 'Attendance Manager'),
        ('viewer', 'Viewer')
    ]
    admin_role = models.CharField(max_length=20, choices=admin_role_choices, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.admin_role}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class Room(models.Model):
    """Hostel room with capacity and availability tracking."""
    room_id = models.AutoField(primary_key=True)
    room_no = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    status_choices = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='available')

    def __str__(self):
        return f"Room {self.room_no}"

    def current_occupancy(self):
        return self.student_set.count()

    def is_available(self):
        return self.status == 'available' and self.current_occupancy() < self.capacity


class Student(models.Model):
    """Student record linked to a Django User account."""
    student_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll_no = models.CharField(max_length=15)
    phone = models.CharField(max_length=15, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_joined']


class Attendance(models.Model):
    """Daily attendance record for a student."""
    attendance_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status_choices = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
    status = models.CharField(max_length=10, choices=status_choices)

    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"


class HostelRule(models.Model):
    """Hostel rules and regulations."""
    rule_id = models.AutoField(primary_key=True)
    rule_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rule_text[:50] + "..."

    class Meta:
        ordering = ['-date_created']


# SIGNALS FOR AUTOMATIC USERPROFILE CREATION
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create UserProfile when a new User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Automatically save UserProfile when User is saved"""
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()