from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .management.commands.bot import send_events
from .models import Post


@receiver(post_save, sender=Post)
def send_new_post_notification(sender, instance, created, **kwargs):
    if created:
        new_post = f'''
<b>{instance.name}</b>

{instance.text}
'''
        image = instance.image
        send_events(new_post, image)


@receiver(post_migrate)
def create_demo_user(sender, **kwargs):
    if sender.name == 'vpnbot':
        user_model = get_user_model()
        # Check if a superuser already exists
        if not user_model.objects.filter(is_superuser=True).exists():
            demo_user = user_model.objects.create_user(
                username='root',
                password='RootPassword',
                email='demo@example.com',
                is_active=True,
                is_staff=True,
                is_superuser=True
            )
            demo_user.save()
