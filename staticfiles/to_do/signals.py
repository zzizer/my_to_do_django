from .models import UserProfile
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=UserProfile)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our To Do Web-App!'
        message = 'Dear {},\n\nThank you for signing up for our App!'.format(instance.username)
        from_email = 'no-reply@toDoWebApp.com'
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
