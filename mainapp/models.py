from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=150,null=False,blank=False)
    code = models.CharField(max_length=150,null=False,blank=False)
    sex_choice = (
        ('男','男'),
        ('女','女')
    )
    sex = models.CharField(max_length=150,choices=sex_choice,default='男')
    chinese = models.IntegerField(default=0)
    english = models.IntegerField(default=0)
    math = models.IntegerField(default=0)
    society = models.IntegerField(default=0)
    science = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)

    def save(self,*args,**kwargs):
        self.total_score = self.chinese + self.english + self.math + self.society + self.science
        self.average_score = round((self.total_score)/5,1)
        super(Student,self).save(*args,**kwargs)

    def __str__(self):
        return self.name




