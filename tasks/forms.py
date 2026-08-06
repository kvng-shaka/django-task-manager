from django import forms
from .models import Task, Profile
from django.contrib.auth.models import User



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your task...', 'rows': 5}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us a little about yourself...', 'rows': 5}),
        }



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


