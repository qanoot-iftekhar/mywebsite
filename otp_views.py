"""
OTP Authentication Views
Add these to main/views.py
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import EmailOTP, PhoneOTP
import json


@require_http_methods(["POST"])
def request_email_otp(request):
    """Request OTP for email login"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
        
        # Generate OTP
        otp_code = EmailOTP.generate_otp()
        
        # Delete old OTPs for this email
        EmailOTP.objects.filter(email=email).delete()
        
        # Create new OTP
        email_otp = EmailOTP.objects.create(
            email=email,
            otp=otp_code
        )
        
        # Send OTP email
        subject = 'Your Login OTP - PROJECT'
        message = f'''
Hello,

Your One-Time Password (OTP) for logging into PROJECT is:

{otp_code}

This OTP is valid for 5 minutes.

If you didn't request this, please ignore this email.

Best regards,
PROJECT Team
        '''
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            return JsonResponse({
                'success': True,
                'message': 'OTP sent to your email'
            })
        except Exception as e:
            print(f"Email send error: {e}")
            return JsonResponse({
                'error': 'Failed to send OTP email'
            }, status=500)
            
    except Exception as e:
        print(f"Request OTP error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def verify_email_otp(request):
    """Verify OTP and log in user"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        otp_code = data.get('otp', '').strip()
        
        if not email or not otp_code:
            return JsonResponse({
                'error': 'Email and OTP are required'
            }, status=400)
        
        # Get latest OTP for this email
        try:
            email_otp = EmailOTP.objects.filter(
                email=email,
                otp=otp_code
            ).latest('created_at')
        except EmailOTP.DoesNotExist:
            return JsonResponse({
                'error': 'Invalid OTP'
            }, status=400)
        
        # Validate OTP
        if not email_otp.is_valid():
            return JsonResponse({
                'error': 'OTP has expired or already been used'
            }, status=400)
        
        # Mark as verified
        email_otp.is_verified = True
        email_otp.save()
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0] + str(User.objects.count()),
            }
        )
        
        if created:
            user.set_unusable_password()  # No password login
            user.save()
        
        # Log in user
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        return JsonResponse({
            'success': True,
            'message': 'Login successful',
            'redirect': '/'
        })
        
    except Exception as e:
        print(f"Verify OTP error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def login_with_otp(request):
    """OTP login page"""
    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'login_otp.html')
