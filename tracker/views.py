# 1. Django Core Imports
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.core.mail import send_mail
from django.db.models import Sum
from django.contrib import messages

# 2. Authentication Imports
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# 3. Local App Imports (Your models and forms)
from .models import Subscription
from .forms import SubscriptionForm

from django.db.models import Sum



def home(request):
    return render(request, 'home.html')

# READ: Display subscriptions on Dashboard
@login_required
def dashboard(request):
    # This fetches all subscriptions that belong to the logged-in user
    user_subs = Subscription.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'subscriptions': user_subs})

# CREATE: Add new subscription

@login_required
def add_subscription(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            
#---------------------------------- Send the email notification
            send_mail(
                'New Subscription Added',
                f'You have added {sub.name} to your tracker for ₹{sub.amount}.',
                'noreply@financeapp.com',
                [request.user.email],
                fail_silently=False,
            )
            return redirect('dashboard')
    else:
        form = SubscriptionForm()
    return render(request, 'add_subscription.html', {'form': form})

# DELETE: Remove a subscription
@login_required
def delete_subscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    subscription.delete()
    return redirect('dashboard')




class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required for login alerts")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
        
def signup(request):
    if request.method == 'POST':
        # Use the custom form we made that includes the email field
        form = ExtendedUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after signup
            login(request, user) 
            messages.success(request, f"Welcome {user.username}! Your account was created.")
            return redirect('dashboard')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)  # Clear the session
        user.delete()    # Remove from database
        messages.success(request, "Account deleted successfully.")
        return redirect('home')
    return redirect('dashboard')




@login_required
def edit_subscription(request, pk):
    # Fetch the subscription or return 404 if not found
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)

    if request.method == "POST":
        # Pass the 'instance' so Django knows to update the existing record
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # Pre-fill the form with the current subscription data
        form = SubscriptionForm(instance=subscription)

    return render(request, 'edit_subscription.html', {'form': form, 'subscription': subscription})


@login_required
def dashboard(request):
    user_subscriptions = Subscription.objects.filter(user=request.user)
    total_spend = user_subscriptions.aggregate(Sum('amount'))['amount__sum'] or 0

    # 📊 Get total amount spent per category for the chart
    category_data = user_subscriptions.values('category').annotate(total=Sum('amount'))
    
    # Extract labels and data points for Chart.js
    labels = [item['category'] for item in category_data]
    data = [float(item['total']) for item in category_data]

    context = {
        'subscriptions': user_subscriptions,
        'total': total_spend,
        'labels': labels, # Send categories to HTML
        'data': data,     # Send amounts to HTML
    }
    return render(request, 'dashboard.html', context)


# @login_required
# def dashboard(request):
#     subscriptions = Subscription.objects.filter(user=request.user)
#     # This calculates the sum of the 'amount' field for all user subscriptions
#     total_monthly = subscriptions.aggregate(Sum('amount'))['amount__sum'] or 0
    
#     return render(request, 'dashboard.html', {
#         'subscriptions': subscriptions,
#         'total': total_monthly
#     })