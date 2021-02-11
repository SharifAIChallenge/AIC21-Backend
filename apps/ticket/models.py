from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='ticket')
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=10000)

    def __str__(self):
        return '%s %s' % (self.title, self.author.username)


class Reply(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='ticket_replies')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.user
