from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()
    title_en = models.CharField(max_length=50)
    title_fa = models.CharField(max_length=50)
    text_en = models.TextField(max_length=10000)
    text_fa = models.TextField(max_length=10000)
    description_en = models.TextField(max_length=300)
    description_fa = models.TextField(max_length=300)

    def __str__(self):
        return '%s, %s' % (self.title_en, self.title_fa)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='blog_comments')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    shown = models.BooleanField(default=True)
    reply_to = models.ForeignKey(
        'Comment', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'user: {self.user}, post: {str(self.post)}'


class Tag(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='tags')
    name_en = models.CharField(max_length=50)
    name_fa = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return '%s, %s' % (self.name_en, self.name_fa)


class AparatMedia(models.Model):
    aparat_id = models.CharField(max_length=128)
    aparat_src = models.URLField(max_length=512)

    post = models.ForeignKey(
        to=Post,
        related_name='aparats',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'post: {self.post_id}'
