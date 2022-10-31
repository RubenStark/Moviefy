from django.contrib import admin

# Register your models here.
from .models import Project, Views, Review, Tag, Episode, Watched, Genre, WatchedEpisode, SecretTag, WatchList, Subscription

admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Episode)
admin.site.register(Watched)
admin.site.register(Views)
admin.site.register(Genre)
admin.site.register(WatchedEpisode)
admin.site.register(SecretTag)
admin.site.register(WatchList)
admin.site.register(Subscription)
