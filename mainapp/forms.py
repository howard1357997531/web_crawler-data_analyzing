from dataclasses import field
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    name = forms.CharField(label='姓名')
    code = forms.CharField(label='學號')
    sex_choice = (
        ('男','男'),
        ('女','女')
    )
    sex = forms.ChoiceField(label='性別',choices=sex_choice)
    chinese = forms.IntegerField(label='國文')
    english = forms.IntegerField(label='英文')
    math = forms.IntegerField(label='數學')
    society = forms.IntegerField(label='自然')
    science = forms.IntegerField(label='社會')
    
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['total_score','average_score']
        





