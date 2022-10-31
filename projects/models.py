from turtle import title
from django.db import models
import uuid
from django.db.models.deletion import CASCADE
from users.models import Profile
from embed_video.fields import EmbedVideoField
from moviepy.editor import *
import datetime


class Project(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)    
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    trailer = models.FileField(upload_to='videos/', null=True, blank=True)
    featured_image = models.ImageField(null=True, upload_to='images/', blank=True, default="default.jpg")
    link = EmbedVideoField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    age_class = (
        ('G', 'G'),
        ('PG', 'PG'),
        ('PG-13', 'PG-13'),
        ('R', 'R'),
        ('X', 'X'),
    )
    movie_restriction = models.CharField(max_length=5, choices=age_class , default='G')
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=200, blank=True)
    movie_views = models.IntegerField(default=1)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    views_24h = models.IntegerField(default=0, null=True, blank=True)
    secret_tags = models.ManyToManyField('SecretTag', blank=True)
    seasonal = models.BooleanField(default=False, null=True, blank=True)
    episodes = models.ManyToManyField('Episode', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total',]
    
    @property
    def duration(self):
        if self.seasonal:
            seasons = []
            for episode in self.episodes.all():
                if episode.season not in seasons:
                    seasons.append(episode.season)
            
            return '{} Seasons'.format(len(seasons))
        else:
            try:
                video = VideoFileClip(self.video.path)
                duration = video.duration
                #convert the duration into hours, minutes and seconds
                hours = int(duration / 3600)
                minutes = int(duration / 60) % 60
                #return the duration in the format hh:mm:ss
                return '{}h{}m'.format(hours, minutes)

            except:
                return 43
    
    @property
    def intduration(self):
        try:
            video = VideoFileClip(self.video.path)
            duration = video.duration
            return duration

        except:
            return 43
       
    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @classmethod
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()
    
    @property
    def getViews(self):
        now = datetime.datetime.now()
        last_24h = now - datetime.timedelta(seconds=5)

        views = self.movie_views

        model = Views()
        model.project = self
        model.views = views
        model.save()

        projectObj = Views.objects.filter(project=self, created__gte=last_24h).count()
        views_24h = projectObj
        self.views_24h = views_24h
        self.save()

        return self.views_24h
    
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['created']

class SecretTag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name

class Episode(models.Model):
    name = models.CharField(max_length=200)
    season = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    link = EmbedVideoField(null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    number = models.IntegerField(default=1, null=True, blank=True)

    movie_views = models.IntegerField(default=1)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    views_24h = models.IntegerField(default=0, null=True, blank=True)

    @property
    def getViews(self):
        now = datetime.datetime.now()
        last_24h = now - datetime.timedelta(seconds=5)

        views = self.movie_views

        model = Views()
        model.episode = self
        model.views = views
        model.save()

        projectObj = Views.objects.filter(episode=self, created__gte=last_24h).count()
        views_24h = projectObj
        self.views_24h = views_24h
        self.save()

        return self.views_24h

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['created']


    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url
    
    @property
    def duration(self):
        try:
            video = VideoFileClip(self.video.path)
            duration = video.duration
            #convert the duration into hours, minutes and seconds
            hours = int(duration / 3600)
            minutes = int(duration / 60) % 60
            #return the duration in the format hh:mm:ss
            return '{}h{}m'.format(hours, minutes)

        except:
            return 43
    
    @property
    def intduration(self):
        try:
            video = VideoFileClip(self.video.path)
            duration = video.duration
            return duration

        except:
            return 43
    
    @property
    def next_episode(self):
        # get the list of episodes in the same project and order them by number
        episodes = Episode.objects.filter(serie=self.project).order_by('created')
        # get the index of the current episode in the list
        index = episodes.index(self)
        # get the next episode
        next = episodes[index + 1]
        # return the next episode
        return next
    
class Views(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, null=True, blank=True)
    views = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.views


class Watched(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    time = models.IntegerField(default=0, null=True, blank=True)
    completed = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    progress = models.IntegerField(default=0, null=True, blank=True)

    #if progress is more than 95% mark the project as watched

    class Meta:
        unique_together = [['owner', 'project']]
    
    

class WatchedEpisode(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, null=True)
    time = models.IntegerField(default=0, null=True, blank=True)
    completed = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    progress = models.IntegerField(default=0, null=True, blank=True)
        
    class Meta:
        unique_together = [['owner', 'episode']]



class Genre(models.Model):
    genre = models.CharField(max_length=200)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url
        
    def __str__(self):
        return self.genre

class WatchList(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    class Meta:
        unique_together = [['owner', 'project']]

#create a model instance so a user can subscribe to another user
class Subscription(models.Model):
    subscriber = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscriber')
    subscribed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscribed')
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    class Meta:
        unique_together = [['subscriber', 'subscribed']]