from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Student
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# --------- Student Register ---------
def student_register(request):
    if request.method == "POST":
        register_no = request.POST['register_no']
        name = request.POST['name']
        email = request.POST['email']
        branch = request.POST['branch']
        phone = request.POST['phone']
        parent_phone = request.POST['parent_phone']
        age = request.POST['age']
        password = request.POST['password']

        if User.objects.filter(username=register_no).exists():
            messages.error(request, "Registration number already exists")
            return redirect('student_register')

        user = User.objects.create_user(
            username=register_no,
            password=password,
            email=email,
            first_name=name
        )
        Student.objects.create(
            user=user,
            register_no=register_no,
            branch=branch,
            phone=phone,
            parent_phone=parent_phone,
            age=age
        )
        messages.success(request, "Student registered successfully")
        return redirect('login')

    return render(request, 'students/register.html')


# --------- Login (shared) ---------
def student_login(request):
    if request.method == "POST":
        register_no = request.POST['register_no']  # <-- changed from 'username'
        password = request.POST['password']

        user = authenticate(request, username=register_no, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on role
            if hasattr(user, 'student_profile'):
                return redirect('student_dashboard')
            elif hasattr(user, 'teacher_profile'):
                return redirect('teacher_dashboard')
            else:
                messages.error(request, "No profile found for this user")
                return redirect('login')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'students/login.html')


##--------- Logout ---------##
def logout_view(request):
    logout(request)
    return redirect('login')


# --------- Student Dashboard ---------
@login_required
def student_dashboard(request):
    return render(request, 'students/dashboard.html')

def student_password_change(request):
    return render(request, 'students/reset_password.html')