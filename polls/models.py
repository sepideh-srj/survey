from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200, blank=True)
    flashPic = models.ImageField(upload_to='images/')
    ambientPic = models.ImageField(upload_to='images/')
    blendedPic = models.ImageField(upload_to='images/', blank=True, null=True) 
    chosenPic = models.ImageField(upload_to='images/', blank=True, null=True) 
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    edit = models.IntegerField(default=0)
    def __str__(self):
        return str(self.edit)

class FinalChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    finalChoice = models.IntegerField(default=0)
    def __str__(self):
        return str(self.finalChoice)

