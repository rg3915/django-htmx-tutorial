from django.db import models
from django.urls import reverse_lazy


class Book(models.Model):
    title = models.CharField('título', max_length=100, unique=True)
    author = models.CharField('autor', max_length=100, null=True, blank=True)
    like = models.BooleanField(null=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'livro'
        verbose_name_plural = 'livros'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('bookstore:book_detail', kwargs={'pk': self.pk})
