from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.



class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name='Contenido')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    image = models.ImageField(upload_to='blog/images/', blank=True, verbose_name='Imagen')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    content = models.TextField(verbose_name='Comentario')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')

    def __str__(self):
        return f'Comentario de {self.author} en {self.post.title}'

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', '👍'),
        ('heart', '❤️'),
        ('smile', '😊'),
    ]
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Asegura que un usuario solo pueda dar una reacción por post
        unique_together = ['post', 'user']


