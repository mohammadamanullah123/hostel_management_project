from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import date

from .models import Student, Room, Attendance, HostelRule
from django.contrib.auth.models import User


# ─── Helper ──────────────────────────────────────────────────────────────────

def is_admin_user(user):
    """Check if the given user has admin privileges."""
    return (user.is_staff or
            user.is_superuser or
            (hasattr(user, 'userprofile') and
             getattr(user.userprofile, 'is_hostel_admin', False)))


# ─── Public / Home ───────────────────────────────────────────────────────────

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    context = {
        'total_students': Student.objects.count(),
        'total_rooms': Room.objects.count(),
    }
    return render(request, 'home.html', context)


# ─── Dashboard ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    admin = is_admin_user(request.user)

    if admin:
        total_students = Student.objects.count()
        total_rooms = Room.objects.count()
        available_rooms = Room.objects.filter(status='available').count()
        occupied_rooms = Room.objects.filter(status='occupied').count()
        maintenance_rooms = Room.objects.filter(status='maintenance').count()
        recent_students = Student.objects.all().order_by('-date_joined')[:5]
        recent_attendance = Attendance.objects.all().order_by('-date')[:10]
        total_rules = HostelRule.objects.count()

        # Attendance stats for today
        today = date.today()
        today_present = Attendance.objects.filter(date=today, status='present').count()
        today_absent = Attendance.objects.filter(date=today, status='absent').count()

        context = {
            'is_admin': True,
            'total_students': total_students,
            'total_rooms': total_rooms,
            'available_rooms': available_rooms,
            'occupied_rooms': occupied_rooms,
            'maintenance_rooms': maintenance_rooms,
            'recent_students': recent_students,
            'recent_attendance': recent_attendance,
            'total_rules': total_rules,
            'today_present': today_present,
            'today_absent': today_absent,
        }
        return render(request, 'dashboard.html', context)

    else:
        # Student dashboard
        try:
            student = Student.objects.get(user=request.user)
            attendance = Attendance.objects.filter(student=student).order_by('-date')[:10]
            total_present = Attendance.objects.filter(student=student, status='present').count()
            total_absent = Attendance.objects.filter(student=student, status='absent').count()

            context = {
                'is_admin': False,
                'student': student,
                'attendance': attendance,
                'total_present': total_present,
                'total_absent': total_absent,
                'total_students': Student.objects.count(),
                'total_rooms': Room.objects.count(),
                'available_rooms': Room.objects.filter(status='available').count(),
            }
        except Student.DoesNotExist:
            context = {
                'is_admin': False,
                'student': None,
                'total_students': Student.objects.count(),
                'total_rooms': Room.objects.count(),
                'available_rooms': Room.objects.filter(status='available').count(),
            }

        return render(request, 'dashboard.html', context)


# ─── Student Views ───────────────────────────────────────────────────────────

@login_required
def student_list(request):
    students = Student.objects.select_related('room').all()
    admin = is_admin_user(request.user)
    return render(request, 'students/list.html', {
        'students': students,
        'is_admin': admin,
    })


@login_required
def add_student(request):
    if not is_admin_user(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    rooms = Room.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        roll_no = request.POST.get('roll_no', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        room_id = request.POST.get('room', '')

        # Validation
        if not all([username, name, email, roll_no, password]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'students/form.html', {
                'rooms': rooms, 'form_title': 'Add Student',
                'form_data': request.POST,
            })

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'students/form.html', {
                'rooms': rooms, 'form_title': 'Add Student',
                'form_data': request.POST,
            })

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'students/form.html', {
                'rooms': rooms, 'form_title': 'Add Student',
                'form_data': request.POST,
            })

        user = User.objects.create_user(username=username, email=email, password=password)
        room = Room.objects.get(room_id=room_id) if room_id else None
        Student.objects.create(
            user=user, name=name, email=email,
            roll_no=roll_no, phone=phone if phone else None,
            room=room,
        )
        messages.success(request, f'Student "{name}" added successfully!')
        return redirect('student_list')

    return render(request, 'students/form.html', {
        'rooms': rooms,
        'form_title': 'Add Student',
    })


@login_required
def edit_student(request, student_id):
    if not is_admin_user(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    student = get_object_or_404(Student, student_id=student_id)
    rooms = Room.objects.all()

    if request.method == 'POST':
        student.name = request.POST.get('name', '').strip()
        student.email = request.POST.get('email', '').strip()
        student.roll_no = request.POST.get('roll_no', '').strip()
        student.phone = request.POST.get('phone', '').strip() or None
        room_id = request.POST.get('room', '')
        student.room = Room.objects.get(room_id=room_id) if room_id else None
        student.save()

        # Update linked user email
        student.user.email = student.email
        student.user.save()

        messages.success(request, f'Student "{student.name}" updated successfully!')
        return redirect('student_list')

    return render(request, 'students/form.html', {
        'student': student,
        'rooms': rooms,
        'form_title': 'Edit Student',
    })


@login_required
def delete_student(request, student_id):
    if not is_admin_user(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        user = student.user
        student_name = student.name
        student.delete()
        user.delete()
        messages.success(request, f'Student "{student_name}" deleted successfully!')
        return redirect('student_list')

    return render(request, 'students/confirm_delete.html', {'student': student})


# ─── Room Views ──────────────────────────────────────────────────────────────

@login_required
def room_list(request):
    rooms = Room.objects.all()
    admin = is_admin_user(request.user)
    # Annotate each room with its occupants
    for room in rooms:
        room.occupants = room.student_set.all()
        room.occupancy_count = room.student_set.count()
    return render(request, 'rooms/list.html', {
        'rooms': rooms,
        'is_admin': admin,
    })


@login_required
def add_room(request):
    if not is_admin_user(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    if request.method == 'POST':
        room_no = request.POST.get('room_no', '').strip()
        capacity = request.POST.get('capacity', '').strip()
        status = request.POST.get('status', 'available')

        if not all([room_no, capacity]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'rooms/form.html', {
                'form_title': 'Add Room', 'form_data': request.POST,
            })

        if Room.objects.filter(room_no=room_no).exists():
            messages.error(request, f'Room "{room_no}" already exists!')
            return render(request, 'rooms/form.html', {
                'form_title': 'Add Room', 'form_data': request.POST,
            })

        Room.objects.create(room_no=room_no, capacity=int(capacity), status=status)
        messages.success(request, f'Room "{room_no}" created successfully!')
        return redirect('room_list')

    return render(request, 'rooms/form.html', {'form_title': 'Add Room'})


@login_required
def edit_room(request, room_id):
    if not is_admin_user(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    room = get_object_or_404(Room, room_id=room_id)

    if request.method == 'POST':
        room.room_no = request.POST.get('room_no', '').strip()
        room.capacity = int(request.POST.get('capacity', 0))
        room.status = request.POST.get('status', 'available')
        room.save()
        messages.success(request, f'Room "{room.room_no}" updated successfully!')
        return redirect('room_list')

    return render(request, 'rooms/form.html', {
        'room': room,
        'form_title': 'Edit Room',
    })


@login_required
def delete_room(request, room_id):
    if not is_admin_user(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    room = get_object_or_404(Room, room_id=room_id)
    if request.method == 'POST':
        room_no = room.room_no
        room.delete()
        messages.success(request, f'Room "{room_no}" deleted successfully!')
        return redirect('room_list')

    return render(request, 'rooms/confirm_delete.html', {'room': room})


# ─── Attendance Views ────────────────────────────────────────────────────────

@login_required
def attendance_list(request):
    admin = is_admin_user(request.user)

    if admin:
        attendance = Attendance.objects.select_related('student', 'student__room').all().order_by('-date')
        return render(request, 'attendance/list.html', {
            'attendance': attendance,
            'is_admin': True,
        })
    else:
        try:
            student = Student.objects.get(user=request.user)
            attendance = Attendance.objects.filter(student=student).order_by('-date')
            total_present = attendance.filter(status='present').count()
            total_absent = attendance.filter(status='absent').count()
            return render(request, 'attendance/list.html', {
                'attendance': attendance,
                'is_admin': False,
                'total_present': total_present,
                'total_absent': total_absent,
            })
        except Student.DoesNotExist:
            messages.error(request, 'Student profile not found!')
            return redirect('dashboard')


@login_required
def mark_attendance(request):
    if not is_admin_user(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    students = Student.objects.select_related('room').all()
    attendance_date = request.POST.get('date', str(date.today()))

    if request.method == 'POST':
        att_date = request.POST.get('date', str(date.today()))
        present_ids = request.POST.getlist('present')

        marked = 0
        for student in students:
            status = 'present' if str(student.student_id) in present_ids else 'absent'
            obj, created = Attendance.objects.update_or_create(
                student=student,
                date=att_date,
                defaults={'status': status},
            )
            marked += 1

        messages.success(request, f'Attendance marked for {marked} students on {att_date}.')
        return redirect('attendance_list')

    # Pre-fill existing attendance for today
    existing = {}
    today_records = Attendance.objects.filter(date=attendance_date)
    for rec in today_records:
        existing[rec.student_id] = rec.status

    return render(request, 'attendance/mark.html', {
        'students': students,
        'attendance_date': attendance_date,
        'existing': existing,
    })


# ─── Rules Views ─────────────────────────────────────────────────────────────

@login_required
def rules_list(request):
    rules = HostelRule.objects.all()
    admin = is_admin_user(request.user)
    return render(request, 'rules/list.html', {
        'rules': rules,
        'is_admin': admin,
    })


@login_required
def add_rule(request):
    if not is_admin_user(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    if request.method == 'POST':
        rule_text = request.POST.get('rule_text', '').strip()
        if not rule_text:
            messages.error(request, 'Rule text cannot be empty.')
            return render(request, 'rules/form.html', {
                'form_title': 'Add Rule', 'form_data': request.POST,
            })

        HostelRule.objects.create(rule_text=rule_text)
        messages.success(request, 'Rule added successfully!')
        return redirect('rules_list')

    return render(request, 'rules/form.html', {'form_title': 'Add Rule'})


@login_required
def edit_rule(request, rule_id):
    if not is_admin_user(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    rule = get_object_or_404(HostelRule, rule_id=rule_id)

    if request.method == 'POST':
        rule.rule_text = request.POST.get('rule_text', '').strip()
        rule.save()
        messages.success(request, 'Rule updated successfully!')
        return redirect('rules_list')

    return render(request, 'rules/form.html', {
        'rule': rule,
        'form_title': 'Edit Rule',
    })


@login_required
def delete_rule(request, rule_id):
    if not is_admin_user(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    rule = get_object_or_404(HostelRule, rule_id=rule_id)
    if request.method == 'POST':
        rule.delete()
        messages.success(request, 'Rule deleted successfully!')
        return redirect('rules_list')

    return render(request, 'rules/confirm_delete.html', {'rule': rule})