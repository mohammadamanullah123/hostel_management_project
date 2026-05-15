from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room, Student, Attendance, HostelRule

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_no', 'capacity', 'status', 'current_occupancy']
    list_filter = ['status', 'capacity']
    search_fields = ['room_no']
    list_editable = ['status']
    ordering = ['room_no']
    
    def current_occupancy(self, obj):
        return obj.student_set.count()
    current_occupancy.short_description = 'Current Students'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'email', 'roll_no', 'room', 'date_joined']
    list_filter = ['room', 'date_joined']
    search_fields = ['name', 'email', 'roll_no']
    list_select_related = ['room']
    raw_id_fields = ['user', 'room']
    ordering = ['-date_joined']
    
    fields = ['user', 'name', 'email',  'roll_no', 'room']
    readonly_fields = ['date_joined'] 

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'marked_on']
    list_filter = ['status', 'date']
    search_fields = ['student__name','student__roll_no']
    date_hierarchy = 'date'
    ordering = ['-date', 'student']
    
    def marked_on(self, obj):
        return obj.date.strftime('%b %d, %Y')
    marked_on.short_description = 'Marked Date'

@admin.register(HostelRule)
class HostelRuleAdmin(admin.ModelAdmin):
    list_display = ['rule_id', 'rule_preview', 'date_created']
    search_fields = ['rule_text']
    ordering = ['-date_created']
    
    def rule_preview(self, obj):
        return obj.rule_text[:100] + "..." if len(obj.rule_text) > 100 else obj.rule_text
    rule_preview.short_description = 'Rule'