import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse

# Helper function for user directories
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Tag Model
class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

# Post Model
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    leaving_from = models.TextField(max_length=100, verbose_name='Leaving_from')
    going_to = models.TextField(max_length=100, verbose_name='Going_to')
    date_time = models.DateTimeField(verbose_name='Date_Time')
    transport_mode = models.TextField(max_length=50, verbose_name='Transport_mode')
    content = models.TextField(max_length=1500, verbose_name='content')
    tags = models.ManyToManyField(Tag, related_name='tags')
    posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('postdetails', args=[str(self.id)])

    def __str__(self):
        return str(self.id)

# Stream Model (This is where the posts will be added for all users)
class Stream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who is viewing the post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)  # The post that appears in the stream
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.post.id}"

# Signal to add the post to the stream of every user
@receiver(post_save, sender=Post)
def add_post_to_stream(sender, instance, **kwargs):
    post = instance
    # Get all users (excluding the one who posted the content)
    all_users = User.objects.exclude(id=post.user.id)
    
    # Create a stream entry for each user
    for user in all_users:
        Stream.objects.create(post=post, user=user, date=post.posted)

@receiver(post_save, sender=User)
def add_existing_posts_to_new_user_stream(sender, instance, created, **kwargs):
    if created:  # Only for new users
        posts = Post.objects.all()
        stream_objects = [
            Stream(user=instance, post=post, date=post.posted) for post in posts
        ]
        try:
            Stream.objects.bulk_create(stream_objects)
            print(f"Stream created for user {instance.username}")
        except Exception as e:
            print(f"Error creating stream for user {instance.username}: {e}")


