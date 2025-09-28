from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from .models import Movie, Vote

def index(request):
    movies = Movie.objects.annotate(votes_count=Count('votes')).all()
    return render(request, 'voting/index.html', {'movies': movies})

def vote(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie = get_object_or_404(Movie, pk=movie_id)
        Vote.objects.create(movie=movie)
        votes_count = movie.votes.count()
        return JsonResponse({'votes_count': votes_count, 'movie_id': movie_id})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def results(request):
    # Використовуємо annotate для ефективного підрахунку голосів
    movies_with_votes = Movie.objects.annotate(votes_count=Count('votes')).order_by('-votes_count')
    return render(request, 'voting/results.html', {'votes_data': movies_with_votes})