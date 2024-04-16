from django.shortcuts import render

# Create your views here
from django.shortcuts import render
from .forms import ChallengeForm, PhoneVerification, VerifyCodeForm
from django.shortcuts import redirect
from .models import Challenge, Profile
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .send_message import send_message
from . import utils
from .utils import send_verification_code, verify_code_with_twilio


def index(request):
    return render(request, "tracker/index.html")

# Create your views here.
@login_required(login_url='/members/login_user')
def Dchallenge(request):
    # Retrieve the profile associated with the logged-in user
    profile = request.user.profile
    today = timezone.now().date()
    # Filter challenges based on the retrieved profile
    ch = Challenge.objects.filter(profile=profile,challenge_date=today, status=False)
    ch1 = Challenge.objects.filter(profile=profile, challenge_date=today, status=True)
    return render(request, "tracker/Daily_challenge.html", {
        "ch": ch,
        "ch1":ch1
    })



def aimz(request):
    form = ChallengeForm
    if request.method=="POST":
        form = ChallengeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Challened Added!"))
            return redirect('aimz')     
    return render(request, "tracker/aimz.html", {
        "form": form
    })


def dash(request):
    # Retrieve the profile associated with the logged-in user
    profile = request.user.profile
    # Filter challenges based on the retrieved profile
    ch = Challenge.objects.filter(profile=profile).order_by('challenge_date')
    return render(request, "tracker/dash.html", {
        "ch": ch
    })

def update_challenge(request, challenge_id):
    challenge = Challenge.objects.get(pk=challenge_id)
    form = ChallengeForm(request.user, request.POST or None, instance=challenge)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, ("Challenge Updated!"))
            return redirect('dash')

    return render(request, "tracker/update_challenge.html", {
        "challenge": challenge,
        "form": form
    })


def delete_challenge(request, challenge_id):
    challenge = Challenge.objects.get(pk=challenge_id)
    challenge.delete()
    messages.success(request, ("Challenge Deleted!"))
    return redirect('dash')

def test(request):
    return render(request, "tracker/test.html")

def status(request, challenge_id):
    challenge = Challenge.objects.get(pk=challenge_id)
    challenge.status = not challenge.status
    challenge.save()
    print(challenge.status)
    messages.success(request, ("Congratulations Challenge Completed !"))
    return redirect('Dchallenge')
 
def delete_challenge_index(request, challenge_id):
    challenge = Challenge.objects.get(pk=challenge_id)
    challenge.delete()
    messages.success(request, ("Challenge Deleted!"))
    return redirect('Dchallenge')

def phone_verification(request):
    # Check if the user already has a profile
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('profile')  # Redirect if the user doesn't have a profile

    if request.method == 'POST':
        form = PhoneVerification(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to a page displaying the profile detail
            if send_verification_code(request.user):
                print("code was sent")
                return redirect('verify_code')
    else:
        form = PhoneVerification(instance=profile)
    return render(request, 'tracker/phone_verification.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone_number = request.user.profile.phone_number
            print("mobile number requested")
            
            # Check if the verification code matches the one sent via Twilio
            if verify_code_with_twilio(phone_number, code):
                # Update Profile model to mark verification as successful
                profile = request.user.profile
                profile.is_verified = True
                profile.save()
                messages.success(request, ("You're all set!"))
                print("code was verified with twilio")
                # Redirect to success page or do whatever you want on successful verification
                return redirect('notifications')
            else:
                print("not verified")
                # Handle case where verification code is invalid
                return render(request, 'tracker/verify_code.html', {'form': form, 'error': 'Invalid verification code'})
    else:
        # Send verification code via Twilio only on initial GET request
        send_verification_code(request.user)
        form = VerifyCodeForm()
    
    return render(request, 'tracker/verify_code.html', {'form': form})


def notifications(request):
    if request.method == 'POST':
        # Check if the user's profile is verified
        if request.user.profile.is_verified:
            # Get the user's phone number
            user_phone = request.user.profile.phone_number
            # Call the function to send the message
            send_message(request, user_phone)
            messages.success(request, ("Message sent!"))
            return redirect('notifications')
        else:
            messages.success(request, ("Phone is not verified!"))
    else:
        return render(request, "tracker/notifications.html")