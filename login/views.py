from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        role     = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')
        room     = request.POST.get('room')

        user = authenticate(username=username, password=password)

        if user:
            if role == 'student':
                if user.last_name == room:
                    login(request, user)
                    return redirect('student_dashboard')
                else:
                    return render(request, 'login/login.html', {
                        'error': 'Room number incorrect'
                    })

            elif role == 'warden':
                if user.is_staff:
                    login(request, user)
                    return redirect('warden_home')  # ← changed
                else:
                    return render(request, 'login/login.html', {
                        'error': 'You are not a warden'
                    })

        else:
            return render(request, 'login/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')