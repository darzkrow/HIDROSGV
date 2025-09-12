from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def session_blocked_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        return redirect('login')
    return render(request, 'dashboard/session_blocked.html')
