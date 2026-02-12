import logging

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import DatabaseError
from django.views.decorators.http import require_http_methods
from .models import User

logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Enhanced login view with better error handling and form validation.
    Supports "Remember me" functionality for persistent login sessions.
    """
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        remember_me = request.POST.get('remember_me')
        
        # Validation
        if not username:
            messages.error(request, "Please enter your username or email.")
            return render(request, 'accounts/login.html')
        
        if not password:
            messages.error(request, "Please enter your password.")
            return render(request, 'accounts/login.html')
        
        # Authenticate user
        try:
            user = authenticate(request, username=username, password=password)
        except DatabaseError:
            logger.exception(
                "Database error during authentication",
                extra={"username": username},
            )
            messages.error(
                request,
                "We're having trouble signing you in right now. Please try again shortly.",
            )
            return render(request, 'accounts/login.html', {'username': username})
        
        if user is not None:
            try:
                login(request, user)

                # Handle "Remember me" - set session to expire at browser close if unchecked
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                else:
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
            except DatabaseError:
                logger.exception(
                    "Database/session error during login",
                    extra={"username": username},
                )
                messages.error(
                    request,
                    "We're having trouble signing you in right now. Please try again shortly.",
                )
                return render(request, 'accounts/login.html', {'username': username})

            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            # Generic error message for security (don't reveal if user exists)
            messages.error(request, "Invalid username/email or password. Please try again.")
            return render(request, 'accounts/login.html', {'username': username})
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    """
    Logout view that clears the user session.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('accounts:login')


def profile_view(request):
    """
    User profile view - accessible only to authenticated users.
    """
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return render(request, 'accounts/profile.html')


def register_view(request):
    """
    User registration view with improved validation.
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        # Validation
        if not username:
            messages.error(request, "Username is required.")
            return render(request, 'accounts/register.html')
        
        if not email:
            messages.error(request, "Email is required.")
            return render(request, 'accounts/register.html')
        
        if not password:
            messages.error(request, "Password is required.")
            return render(request, 'accounts/register.html')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/register.html')
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'accounts/register.html')
        
        # Check if user already exists
        try:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose another.")
                return render(request, 'accounts/register.html')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered. Please use another or log in.")
                return render(request, 'accounts/register.html')
        except DatabaseError:
            logger.exception(
                "Database error while checking registration uniqueness",
                extra={"username": username, "email": email},
            )
            messages.error(
                request,
                "We're unable to process registration right now. Please try again shortly.",
            )
            return render(request, 'accounts/register.html')
        
        # Create user
        try:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('accounts:login')
        except DatabaseError:
            logger.exception(
                "Database error while creating user",
                extra={"username": username, "email": email},
            )
            messages.error(
                request,
                "We're unable to create your account right now. Please try again shortly.",
            )
            return render(request, 'accounts/register.html')
        except Exception:
            logger.exception(
                "Unexpected error while creating user",
                extra={"username": username, "email": email},
            )
            messages.error(
                request,
                "We're unable to create your account right now. Please try again shortly.",
            )
            return render(request, 'accounts/register.html')
    
    return render(request, 'accounts/register.html')
