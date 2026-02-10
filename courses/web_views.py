from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Enrollment

User = get_user_model()

@login_required(login_url="login")
def home_view(request):
    """Bosh sahifa – platforma haqida, aktiv kurslar."""
    courses = Course.objects.filter(is_active=True).select_related('teacher')[:12]
    return render(request, 'courses/home.html', {'courses': courses})

@login_required(login_url="login")
def course_list_view(request):
    """Kurslar sahifasi – barcha kurslar, kartalar, o'qituvchi."""
    courses = Course.objects.filter(is_active=True).select_related('teacher')
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required(login_url="login")
def course_detail_view(request, pk):
    """Kurs detail – nom, tavsif, o'qituvchi, darslar, yozilish / boshqarish."""
    course = get_object_or_404(Course, pk=pk, is_active=True)
    lessons = course.lessons.order_by('order', 'added_at')
    is_teacher = request.user.is_authenticated and getattr(request.user, 'role', None) == 'Teacher'
    is_owner = request.user.is_authenticated and course.teacher_id == request.user.id
    enrolled = False
    if request.user.is_authenticated and request.user.role == 'Student':
        enrolled = Enrollment.objects.filter(student=request.user, course=course, is_active=True).exists()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'is_teacher': is_teacher,
        'is_owner': is_owner,
        'enrolled': enrolled,
    })


@login_required(login_url="login")
def dashboard_view(request):
    """Dashboard – Student: yozilgan kurslar; Teacher: yaratilgan kurslar."""
    user = request.user
    if user.role == 'Student':
        enrollments = Enrollment.objects.filter(student=user, is_active=True).select_related('course', 'course__teacher')
        return render(request, 'courses/dashboard_student.html', {'enrollments': enrollments})
    else:
        courses = Course.objects.filter(teacher=user, is_active=True).prefetch_related('lessons')
        return render(request, 'courses/dashboard_teacher.html', {'courses': courses})


# ——— Auth (template) ———
@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not username or not password:
            messages.error(request, 'Login va parolni kiriting.')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Login yoki parol noto\'g\'ri.')
            return redirect('login')
        login(request, user)
        next_url = request.GET.get('next') or '/dashboard/'
        return redirect(next_url)
    return render(request, 'accounts/login.html')


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        role = request.POST.get('role', 'Student')
        if role not in ('Teacher', 'Student'):
            role = 'Student'
        errors = []
        if not username:
            errors.append('Username kiritilishi shart.')
        if User.objects.filter(username=username).exists():
            errors.append('Bunday username mavjud.')
        if not password or len(password) < 8:
            errors.append('Parol kamida 8 belgidan iborat bo\'lishi kerak.')
        if password != password_confirm:
            errors.append('Parollar mos kelmadi.')
        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'accounts/register.html', {
                'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'role': role
            })
        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name, role=role
        )
        login(request, user)
        messages.success(request, 'Ro\'yxatdan muvaffaqiyatli o\'tdingiz.')
        return redirect('dashboard')
    return render(request, 'accounts/register.html')


@require_http_methods(['GET', 'POST'])
def logout_view(request):
    logout(request)
    messages.info(request, 'Tizimdan chiqdingiz.')
    return redirect('home')


# ——— Teacher: kurs yaratish, tahrirlash ———
@login_required(login_url="login")
@require_http_methods(['GET', 'POST'])
def course_create_view(request):
    if getattr(request.user, 'role', None) != 'Teacher':
        messages.error(request, 'Faqat o\'qituvchi kurs yarata oladi.')
        return redirect('course_list')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        if not name:
            messages.error(request, 'Kurs nomi kiritilishi shart.')
            return render(request, 'courses/course_form.html', {'name': name, 'description': description})
        Course.objects.create(name=name, description=description, teacher=request.user)
        messages.success(request, 'Kurs yaratildi.')
        return redirect('dashboard')
    return render(request, 'courses/course_form.html', {'is_edit': False})


@login_required(login_url="login")
@require_http_methods(['GET', 'POST'])
def course_edit_view(request, pk):
    course = get_object_or_404(Course, pk=pk, is_active=True)
    if course.teacher_id != request.user.id:
        messages.error(request, 'Faqat kurs egasi tahrirlay oladi.')
        return redirect('course_detail', pk=pk)
    if request.method == 'POST':
        course.name = request.POST.get('name', '').strip() or course.name
        course.description = request.POST.get('description', '')
        course.save()
        messages.success(request, 'Kurs yangilandi.')
        return redirect('course_detail', pk=pk)
    return render(request, 'courses/course_form.html', {'course': course, 'is_edit': True})


# ——— Teacher: dars qo'shish, tahrirlash, o'chirish ———
@login_required(login_url="login")
@require_http_methods(['GET', 'POST'])
def lesson_add_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id, is_active=True)
    if course.teacher_id != request.user.id:
        messages.error(request, 'Faqat kurs egasi dars qo\'sha oladi.')
        return redirect('course_detail', pk=course_id)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '')
        order = request.POST.get('order') or 0
        try:
            order = int(order)
        except ValueError:
            order = 0
        if not title:
            messages.error(request, 'Dars nomi kiritilishi shart.')
            return render(request, 'courses/lesson_form.html', {'course': course, 'title': title, 'content': content, 'order': order})
        Lesson.objects.create(course=course, title=title, content=content, order=order)
        messages.success(request, 'Dars qo\'shildi.')
        return redirect('course_detail', pk=course_id)
    return render(request, 'courses/lesson_form.html', {'course': course, 'is_edit': False})


@login_required(login_url="login")
@require_http_methods(['GET', 'POST'])
def lesson_edit_view(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if lesson.course.teacher_id != request.user.id:
        messages.error(request, 'Faqat kurs egasi darsni tahrirlay oladi.')
        return redirect('course_detail', pk=lesson.course_id)
    if request.method == 'POST':
        lesson.title = request.POST.get('title', '').strip() or lesson.title
        lesson.content = request.POST.get('content', '')
        try:
            lesson.order = int(request.POST.get('order', lesson.order))
        except ValueError:
            pass
        lesson.save()
        messages.success(request, 'Dars yangilandi.')
        return redirect('course_detail', pk=lesson.course_id)
    return render(request, 'courses/lesson_form.html', {'lesson': lesson, 'course': lesson.course, 'is_edit': True})


@login_required(login_url="login")
@require_http_methods(['POST'])
def lesson_delete_view(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if lesson.course.teacher_id != request.user.id:
        messages.error(request, 'Faqat kurs egasi darsni o\'chiroladi.')
        return redirect('course_detail', pk=lesson.course_id)
    course_id = lesson.course_id
    lesson.delete()
    messages.success(request, 'Dars o\'chirildi.')
    return redirect('course_detail', pk=course_id)


# ——— Student: kursga yozilish, kursdan chiqish ———
@login_required(login_url="login")
@require_http_methods(['POST'])
def enroll_view(request, course_id):
    if getattr(request.user, 'role', None) != 'Student':
        messages.error(request, 'Faqat talaba kursga yozilishi mumkin.')
        return redirect('course_detail', pk=course_id)
    course = get_object_or_404(Course, pk=course_id, is_active=True)
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        enrollment = Enrollment.objects.get(student=request.user, course=course)
        if enrollment.is_active:
            messages.info(request, 'Siz allaqachon ushbu kursga yozilgansiz.')
        else:
            tg = request.POST.get("tg")
            phone = request.POST.get("phone")
            enrollment.is_active = True
            enrollment.phone = phone
            enrollment.tg = tg
            enrollment.save()
            messages.success(request, 'Qayta yozildingiz.')
    else:
        tg = request.POST.get("tg")
        phone = request.POST.get("phone")
        Enrollment.objects.create(student=request.user, course=course, phone=phone, tg=tg)
        messages.success(request, 'Kursga muvaffaqiyatli yozildingiz.')
    return redirect('course_detail', pk=course_id)


@login_required(login_url="login")
@require_http_methods(['POST'])
def leave_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
    if enrollment:
        enrollment.is_active = False
        enrollment.save()
        messages.success(request, 'Kursdan chiqdingiz.')
    return redirect('course_detail', pk=course_id)

def course_students(request, pk):
    enrolments = Enrollment.objects.filter(course_id=pk)
    context = {
        "object_list": enrolments
    }
    return render(request, "course_student.html", context)