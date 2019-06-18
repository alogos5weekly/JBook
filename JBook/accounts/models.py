from django.db import models
from django.conf import settings
from django.urls import reverse

#django choice Field
#https://stackoverflow.com/questions/8077840/choicefield-in-django-model
class UserProfile(models.Model):
    BRANCH_CHOICES = (
        ('CS', 'Computer Science & Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('EE', 'Electrical Engineering'),
        ('ECE', 'Electornics & Communication Engineering'),
        ('CE', 'Civil Engineering'),
        ('IT', 'Information Technology'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to="user_profile_images")
    about = models.TextField(blank=True)
    location = models.CharField(max_length=250, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    branch = models.CharField(max_length=3, choices=BRANCH_CHOICES)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.id and self.avatar:
            current_avatar = UserProfile.objects.get(pk=self.id).avatar
            if current_avatar != self.avatar:
                current_avatar.delete()
        super(UserProfile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        target = reverse('accounts:profile', args=[self.user.username])
        return target

    def followers_count(self):
        return Followers.objects.filter(user=self).count()

class Followers(models.Model):
    user = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE)
    follows = models.ForeignKey(UserProfile, related_name='followers', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
