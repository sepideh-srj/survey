from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200, blank=True)
    # matrix = models.CharField(max_length=200, blank=True)
    # matrix = models.IntegerField(blank=True)
    flashPic = models.ImageField(upload_to='images/')
    ambientPic = models.ImageField(upload_to='images/')
    blendedPic = models.ImageField(upload_to='images/') 
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    flash = models.IntegerField(default=0)
    ambient = models.IntegerField(default=0)
    flashTemp = models.IntegerField(default=0)
    ambientTemp =  models.IntegerField(default=0)
    ambientBrightness = models.IntegerField(default=0)

