from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=45, unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=45)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'email', 'password']

    def __str__(self):
        return f'@{self.username}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='posts/')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f'{self.title} by {self.author}'
class Liked(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, related_name='posts_liked', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='liked_by', on_delete=models.CASCADE)

class Collection(models.Model):
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post, related_name='posts')

    def __str__(self):
        return f'{self.title} by {self.author}'

class Comment(models.Model):
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'comment to post \'{self.post}\' by {self.author}'

class Gallery(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    time_open = models.DateTimeField()
    time_close = models.DateTimeField()
    limit_visitors = models.IntegerField(null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='galleries')
    posts = models.ManyToManyField(Post, related_name='galleries')

    class Meta:
        verbose_name_plural = 'galleries'

    def __str__(self):
        return f'gallery {self.title} by {self.author}'

class Visitors(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)

    visitors = models.ForeignKey(User, related_name='go_to', on_delete=models.CASCADE)
    galleries = models.ForeignKey(Gallery, related_name='places', on_delete=models.CASCADE)
