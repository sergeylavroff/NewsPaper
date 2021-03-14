from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        count = 0
        for a in Post.objects.filter(author = self.id):
            count += a.rating*3
        for c in Comment.objects.filter(user = self.author):
            count += c.rating
        for pc in Comment.objects.filter(user = self.author):
            count += pc.rating
        self.rating = count
        self.save()


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(default='Без текста')
    rating = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    post = 'PT'
    news = 'NW'
    TYPES = [(post,'Статья'),(news,'Новость')]
    type = models.CharField(max_length=2, choices=TYPES, default=post)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    @property
    def preview(self):
        return self.body[:124] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    com_text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()