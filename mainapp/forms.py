from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    name = forms.CharField(label='姓名')
    code = forms.CharField(label='學號')
    sex_choice = (
        ('男', '男'),
        ('女', '女')
    )
    sex = forms.ChoiceField(label='性別', choices=sex_choice)
    chinese = forms.IntegerField(label='國文', min_value=0, max_value=100)
    english = forms.IntegerField(label='英文', min_value=0, max_value=100)
    math = forms.IntegerField(label='數學', min_value=0, max_value=100)
    society = forms.IntegerField(label='社會', min_value=0, max_value=100)
    science = forms.IntegerField(label='自然', min_value=0, max_value=100)

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['total_score', 'average_score']
