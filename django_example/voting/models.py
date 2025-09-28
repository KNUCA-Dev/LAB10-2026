from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='posters/')

    def __str__(self):
        return self.title

class Vote(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote for {self.movie.title}"