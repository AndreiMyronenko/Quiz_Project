from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Quiz, Question

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class QuizForm(forms.ModelForm):
    
    class Meta:
        model = Quiz
        fields = {'title', 'topic', 'description', 'number_of_questions', 'image', 'time'} 
    

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()
    image = forms.ImageField()