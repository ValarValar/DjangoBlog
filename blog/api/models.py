from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    subscriptions = models.ManyToManyField(
        User,
        related_name='subscribers',
        symmetrical=False,
        blank=True,
)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, )
    instance.profile.save()


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=200)
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class UserPostRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_relation')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='user_relation')
    seen = models.BooleanField(default=False)
