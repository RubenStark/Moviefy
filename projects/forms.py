from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Project, Review, Watched

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'movie_restriction', 'language', 'link', 'video',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'featured_image': forms.FileInput(attrs={'class': 'form_gallery-upload', 'placeholder': 'Featured Image', 'id': 'form_gallery-upload'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'movie_restriction': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Movie Restriction'}),
            'language': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Language'}),
            'link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link'}),
            'video': forms.FileInput(attrs={'class': 'form_video-upload', 'placeholder': 'Upload Video'}),
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)


        # self.fields['title'].widget.attrs.update(
        #     {'class': 'input'})

        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }
        widgets = {
            'value': forms.Select(attrs={'class': 'input'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class WatchedForm(ModelForm):
    class Meta:
        model = Watched
        fields = ['time']

class WatchedEpisodeForm(ModelForm):
    class Meta:
        model = Watched
        fields = ['time']
