from django.contrib.postgres.search import SearchRank, SearchQuery, SearchVector
from django.db.models import F
from .models import Audio, Video

def search_audio(query):
    audios = Audio.objects.all()
    search_query = SearchQuery(query)
    vector = SearchVector('title', weight='A')+SearchVector('artist', weight='B')+SearchVector('lyrics', weight='C')
    results = (audios.annotate(rank=SearchRank(vector, search_query))).filter(search=search_query).order_by('-rank')
    return results

def search_video(query):
    pass