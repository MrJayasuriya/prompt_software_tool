from django.db import models

# Create your models here.
class Chat(models.Model):
    user_input = models.TextField()
    response = models.TextField()
    prompt_used = models.TextField(null=True, blank=True)
    system_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_input
