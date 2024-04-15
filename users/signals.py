from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser


# CustomUser ni save() metodi chaqirilganda ishlaydi
@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail("Welcome to Goodreads clone!",
                  f"Hi, {instance.username}, welcome to Goodreads clone. Enjoy the books and reviews.",
                  'rano.baxromovna@gmail.com',
                  [instance.email]
                  )
