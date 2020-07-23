from django.db import models



class Question(models.Model):
    question_id = models.IntegerField(default=0)
    choiceSet = models.IntegerField(default=0)
    setNum = models.IntegerField(default=0)
    # matrix = models.CharField(max_length=200, blank=True)
    # matrix = models.IntegerField(blank=True)
    flashPic = models.ImageField(upload_to='images/')
    ambientPic = models.ImageField(upload_to='images/')
    # blendedPic = models.ImageField(upload_to='images/') 
    def __str__(self):
        return str(self.question_id)


class User(models.Model):
    userID = models.IntegerField(default=0)
    pointer = models.IntegerField(default=0, blank=True)
    order = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=10, default='')
    age = models.CharField(max_length=30, default='')
    experience = models.CharField(max_length=100, default='')
    code = models.IntegerField(default=0)
    setNum = models.IntegerField(default=1)
    def __str__(self):
        return str(self.userID)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    questionID = models.IntegerField(default=0)
    setNum = models.IntegerField(default=1)
    choice = models.IntegerField(default=0)
    user = models.IntegerField(default=0)
    flash = models.IntegerField(default=0)
    temp = models.IntegerField(default=0)  
    time = models.IntegerField(default=0)
    tempNum = models.IntegerField(default=0)