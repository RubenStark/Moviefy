from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name="projects"),
    path('projects-search/', views.projectsSearch, name="projectsSearch"),
    path('movies/', views.movies, name="movies"),
    path('series/', views.series, name="series"),
    path('shorts/', views.shorts, name="shorts"),
    path('project/<str:pk>/', views.project, name="project"),
    path('episode/<str:pk>/', views.episode, name="episode"),
    path('projectDetails/<str:pk>/', views.projectDetails, name="projectDetails"),
    path('serieDetails/<str:pk>/', views.serieDetails, name="serieDetails"),
    path('create-project/', views.createProject, name="create-project"),
    path('create-serie/', views.createSerie, name="create-serie"),
    path('update-project/<str:pk>/', views.updateProject, name="update-project"),
    path('delete-project/<str:pk>/', views.deleteProject, name="delete-project"),
    path('genre/<str:genre>/', views.genre, name="genre"),
    path('genres/', views.genres, name="genres"),
    path('subscribe/<str:pk>/', views.subscribe, name="subscribe"),
    path('subscribe2/<str:pk>/', views.subscribe2, name="subscribe2"),
    path('coming-soon/', views.comingSoon, name="coming-soon"),
    
]
