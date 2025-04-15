from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task

@receiver(pre_save, sender=Task)
def notify_task_status_change(sender, instance, **kwargs):
    try:
        old_instance = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        old_instance = None

    if old_instance:
        old_status = old_instance.status
        new_status = instance.status

        if old_status != new_status:
            send_mail(
                f"Изменение статуса задачи: {instance.title}",
                f"Статус вашей задачи изменился с '{old_status}' на '{new_status}'.",
                'no-reply@example.com',
                [instance.owner.email],
                fail_silently=False,
            )
