from itertools import count
import profile
import re
from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.test import tag
from .models import Episode, Project, Tag, Watched, Views, Genre, WatchedEpisode, WatchList, Subscription, Review
from .forms import ProjectForm, ReviewForm, WatchedForm, WatchedEpisodeForm
from .utils import searchProjects, paginateProjects 
from moviepy.editor import VideoFileClip
import datetime
from django.http import JsonResponse
import json
from django.utils import timezone
from django.urls import reverse
from users.models import Profile

def projects(request):
    
    genres = Genre.objects.all()
    projects = Project.objects.all()
    toptens = Project.objects.order_by('-vote_ratio', '-vote_total')[:10]
    topviews = Project.objects.order_by('-movie_views', '-vote_ratio')[:15]
    topfirst = topviews.filter()[:1]
    #get the second object from the topviews list
    topsecond = topviews.filter()[1:2]
    #create a variable trending to store the projects from the model Views
    trending = Project.objects.order_by('-views_24h')[:15]
    

    if request.user.is_authenticated:
                
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data_from_post = json.load(request)['project']

            watchList = WatchList()
            watchList.project = Project.objects.get(id=data_from_post)
            watchList.owner = request.user.profile
            watchList.save()
            print('user added a movie:', data_from_post)
        
        #get all the projects on WatchList
        watchList = WatchList.objects.filter(owner=request.user.profile)
        list = []
        for i in watchList:
            list.append(i.project)

        watched = Watched.objects.filter(owner=request.user.profile)
        #get the projects stored in watched
        watched_progress = []
        watched_projects = []
        for i in watched:
            if i.completed == False:
                watched_projects.append(i.project)
                watched_progress.append(i)
        
        #get the tagas of the watched_projects
        watched_tags = []  
        for i in watched_projects:
            for j in i.tags.all():
                watched_tags.append(j)
        #get the projects that have the same tags as the watched_projects
        similar_projects = []
        for i in watched_tags:
            for j in i.project_set.all():
                similar_projects.append(j)
                #if the user has already watched the project, remove it from the list
                if j in watched_projects:
                    similar_projects.remove(j)

        #get the subscriptions of the 
        subscriber = request.user.profile
        subs = Subscription.objects.filter(subscriber=subscriber)
        #create a list to store the projects of the subscriptions
        subscribed = []
        #for each subscription in the list
        for i in subs:
            #get the project of the subscription
            subscribed.append(i.subscribed)
            #get the projects of the subscriptions
        
        subscriptions = []
        
        for i in subscribed:
            subsprojects = i.project_set.all()
            for j in subsprojects:
                subscriptions.append(j)
                #if the project is already in watched projects
                if j in watched_projects:
                    #delete the project
                    subscriptions.remove(j)
    else:
        watched_projects = []
        watched_progress = []
        similar_projects = []
        list             = []
        subscriptions    = []
    
    series = Project.objects.filter(seasonal=True)
    
    
    context = {
        'projects': projects, 'toptens': toptens, 'topviews': topviews, 'topfirst': topfirst,
        'topsecond': topsecond, 'trending': trending , 'watched_projects': watched_projects,
        'genres': genres, 'similar_projects': similar_projects, 'watched_progress': watched_progress,
        'list': list, 'subscriptions': subscriptions, 'series': series
        }

    
    return render(request, 'projects/projects.html', context)

def projectsSearch(request):

    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 9)
    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range}

    return render(request, 'projects/projects-search.html', context)

def genre(request, genre):

    genre = genre
    genre = genre.upper()
    projects = Project.objects.filter(genre__contains=genre)
    
    context = {'projects': projects, 'genre': genre}
    return render(request, 'projects/genre.html', context)

def genres(request):
    genres = Genre.objects.all()
    context = {'genres': genres}
    return render(request, 'projects/genres.html', context)
    

def movies(request):
    projects = Project.objects.filter(title__contains='One')

    context = {'projects': projects,}
    return render(request, 'projects/movies.html', context)


def series(request):
    
    context = {}
    return render(request, 'projects/series.html', context)

def shorts(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)

    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/shorts.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = WatchedForm()

    if request.user.is_authenticated:
        if Watched.objects.filter(project=projectObj, owner=request.user.profile).exists():
            get_time = Watched.objects.get(project=projectObj, owner=request.user.profile)
            if get_time.completed == True:
                startTime = 0
            else:
                startTime = get_time.time
        else:
            startTime = 0
    else:
        startTime = 0
    
    #if request method is ajax 
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_from_post = json.load(request)['time']
        print(data_from_post)

        #if user is logged in
        if request.user.is_authenticated:
            #if user has watched this project before
            if Watched.objects.filter(project=projectObj, owner=request.user.profile).exists():
                watched = Watched.objects.get(project=projectObj, owner=request.user.profile)
                watched.time = data_from_post
                progress = startTime / watched.project.intduration * 100
                if progress > 95:
                    watched.completed = True
                else:
                    watched.completed = False
                watched.progress = progress
                watched.save()
            #if user has not watched this project before
            else:
                watched = Watched()
                watched.project = projectObj
                watched.owner = request.user.profile
                watched.time = data_from_post
                watched.save()
            
            return JsonResponse({'time': data_from_post})
    
    projectObj.movie_views = projectObj.movie_views + 1
    projectObj.save()

    object = Views.objects.filter(project=projectObj)
    #delete the object if it was created more than 10 seconds ago
    for i in object:
        now = timezone.now()
        if i.created < now - datetime.timedelta(seconds=10):
            i.delete()

    return render(request, 'projects/single-project2.html', {'project': projectObj, 'form': form, 'startTime': startTime,})

def episode(request, pk):
    projectObj = Episode.objects.get(id=pk)
    form = WatchedEpisodeForm()

    if request.user.is_authenticated:
        if WatchedEpisode.objects.filter(episode=projectObj, owner=request.user.profile).exists():
            get_time = WatchedEpisode.objects.get(episode=projectObj, owner=request.user.profile)
            startTime = get_time.time
            print(startTime)
        else:
            startTime = 0
    else:
        startTime = 0
    
    #if request method is ajax 
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_from_post = json.load(request)['time']
        print(data_from_post)

        #if user is logged in
        if request.user.is_authenticated:
            #if user has watched this project before
            if WatchedEpisode.objects.filter(episode=projectObj, owner=request.user.profile).exists():
                watched = WatchedEpisode.objects.get(episode=projectObj, owner=request.user.profile)
                watched.time = data_from_post
                percentage = watched.time / projectObj.duration * 100
                projectObj.progress = percentage
                projectObj.save()
                if percentage >= 95:
                    watched.completed = True
                else:
                    watched.completed = False
                watched.save()

            #if user has not watched this project before
            else:
                watched = WatchedEpisode()
                watched.episode = projectObj
                watched.owner = request.user.profile
                watched.time = data_from_post
                watched.save()
            
            return JsonResponse({'time': data_from_post})
    
    projectObj.movie_views = projectObj.movie_views + 1
    projectObj.save()

    object = Views.objects.filter(episode=projectObj)
    #delete the object if it was created more than 10 seconds ago
    for i in object:
        now = timezone.now()
        if i.created < now - datetime.timedelta(seconds=10):
            i.delete()
    
    

    context = {'project': projectObj, 'form': form, 'startTime': startTime,}
    return render(request, 'projects/single-episode.html', context)

def projectDetails(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('projectDetails', pk=projectObj.id)
    
    #check if there are existing reviews
    if projectObj.review_set.all().count() > 0:
        reviews_exist = True
    else:
        reviews_exist = False
    
    #get movies that have the same tags as the project up to 10
    similar_movies = Project.objects.filter(tags__in=projectObj.tags.all())[:10]

    #get if the user is alreade subscribed 
    if request.user.is_authenticated:
        if Subscription.objects.filter(subscribed=projectObj.owner, subscriber=request.user.profile).exists():
            subscribed = True
        else: 
            subscribed = False
        
    else:
        subscribed = False

    return render(request, 'projects/projectDetails.html', {'project': projectObj, 'form': form, 'reviews_exist': reviews_exist, 'similar_movies': similar_movies, 'subscribed': subscribed,})


def subscribe(request, pk):

    project = Project.objects.get(id=pk)

    if request.method == 'POST':
        if Subscription.objects.filter(subscribed=project.owner, subscriber=request.user.profile).exists():
            #delete the subscription
            subscription = Subscription.objects.get(subscribed=project.owner, subscriber=request.user.profile)
            subscription.delete()
        
        else:
            sub = Subscription
            sub.objects.create(subscriber=request.user.profile, subscribed=project.owner)

    return redirect('projectDetails', pk=project.id)

def subscribe2(request, pk):

    profile = Profile.objects.get(id=pk)

    if request.method == 'POST':
        if Subscription.objects.filter(subscribed=profile, subscriber=request.user.profile).exists():
            #delete the subscription
            subscription = Subscription.objects.get(subscribed=profile, subscriber=request.user.profile)
            subscription.delete()

        else:
            sub = Subscription
            sub.objects.create(subscriber=request.user.profile, subscribed=profile)

    return redirect('user-profile', pk=profile.id)


def serieDetails(request, pk):
    serieObj = Project.objects.get(id=pk)

    #get all the episodes of the serie
    episodes = serieObj.episodes.all()

    #get the season count from the episodes
    seasons = []
    for episode in episodes:
        if episode.season not in seasons:
            seasons.append(episode.season)

    form = ReviewForm()
    episodes_total = len(episodes)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.serie = serieObj
        review.owner = request.user.profile
        review.save()

        serieObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=serieObj.id)
    
    if request.user.is_authenticated:
        #get the episodes that the user watched
        watchedEpisodes = []
        for episode in episodes:
            if WatchedEpisode.objects.filter(episode=episode, owner=request.user.profile).exists():
                watched = WatchedEpisode.objects.get(episode=episode, owner=request.user.profile)
                watchedEpisodes.append(watched)
            else:
                print(episode, 'Not watched')
        
        for episode in episodes:
            if WatchedEpisode.objects.filter(episode=episode, owner=request.user.profile).exists():
                watched = WatchedEpisode.objects.get(episode=episode, owner=request.user.profile)
                if watched.completed == False:
                    currentEpisode = watched.episode.id
                    break
            else:
                currentEpisode = episode.id
                break
    else:
        watchedEpisodes = []
        currentEpisode = episodes[0].id


    context = {'serie': serieObj, 'form': form, 'episodes': episodes, 
    'episodes_total': episodes_total, 'seasons': seasons, 'watchedEpisodes': watchedEpisodes, 'currentEpisode': currentEpisode,}

    return render(request, 'projects/serieDetails.html', context)


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def createSerie(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form}
    return render(request, "projects/serie_form.html", context)

@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    context = {'form': form, 'project': project}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete_template.html', context)


def comingSoon(request):
    return render(request, 'projects/coming_soon.html')

