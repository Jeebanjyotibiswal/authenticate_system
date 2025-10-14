from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Teacher
from django.contrib.auth.decorators import login_required

# --------- Teacher Register ---------
def teacher_register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        employee_id = request.POST['employee_id']
        department = request.POST['department']
        phone = request.POST['phone']
        age = request.POST['age']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('teacher_register')

        user = User.objects.create_user(username=username, password=password, email=email)
        Teacher.objects.create(
            user=user,
            employee_id=employee_id,
            department=department,
            phone=phone,
            age=age
        )
        messages.success(request, "Teacher registered successfully")
        return redirect('teacher_login')

    return render(request, 'teachers/register.html')


# --------- Teacher Login ---------
def teacher_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('teacher_login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('teacher_login')

    return render(request, 'teachers/login.html')


# # --------- Logout ---------
def teacher_logout(request):
    logout(request)
    return redirect('teacher_login')


# --------- Teacher Dashboard ---------
@login_required
def teacher_dashboard(request):
    return render(request, 'teachers/dashboard.html')



# --------- Password Reset ---------

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def teacher_password_change(request):
    """
    Allow teacher to reset password using their registered email.
    Ensures only users linked to Teacher model can reset here.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        try:
            user = User.objects.get(email=email)
            # Check if user has a Teacher profile
            if not hasattr(user, 'teacher_profile'):
                messages.error(request, "No teacher account found with this email.")
                return render(request, 'teachers/reset_password.html')
        except User.DoesNotExist:
            messages.error(request, "No teacher account found with this email.")
            return render(request, 'teachers/reset_password.html')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif len(password1) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
        else:
            user.set_password(password1)
            user.save()
            messages.success(request, "Password updated successfully! You can now log in.")
            return redirect('teacher_login')

    return render(request, 'teachers/reset_password.html')

