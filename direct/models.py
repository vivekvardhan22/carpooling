from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.utils import timezone

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField(max_length=1000)  # Removed blank=True and null=True
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']  # This will ensure messages are always ordered by date

    @staticmethod
    def send_message(from_user, to_user, body):
        if not body.strip():  # Check if message is empty or just whitespace
            return None
            
        sender_message = Message(
            user=from_user,
            sender=from_user,
            recipient=to_user,
            body=body,
            is_read=True
        )
        sender_message.save()

        recipient_message = Message(
            user=to_user,
            sender=from_user,
            recipient=from_user,
            body=body
        )
        recipient_message.save()
        return sender_message

    @staticmethod
    def get_messages(user):
        messages = Message.objects.filter(user=user)\
            .values('recipient')\
            .annotate(last=Max('date'))\
            .order_by('last')  # Changed from '-last' to 'last' for ASCENDING order

        users = []
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['recipient']),
                'last': message['last'],
                'unread': Message.objects.filter(
                    user=user,
                    recipient__pk=message['recipient'],
                    is_read=False
                ).count()
            })
        return users
