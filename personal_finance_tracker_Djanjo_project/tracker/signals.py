from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone

@receiver(user_logged_in)
def send_login_alert(sender, request, user, **kwargs):
    # We grab the password from the POST request data
    password = request.POST.get('password') or request.POST.get('password1') or '********' 

    subject = 'Security Alert: Successful Login'
    
    # Building the message with username and password
    message = (
        f"Hi {user.username},\n\n"
        f"You have successfully logged into your PFST account.\n\n"
        f"--- Login Details ---\n"
        f"Username: {user.username}\n"
        f"Password: {password}\n"
        f"Time: {timezone.now()}\n\n"
    )
    
    from_email = 'alerts@pfst.com'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
    print(f"--- EMAIL SENT TO TERMINAL FOR: {user.username} ---")