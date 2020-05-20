from django.db import models



class Question(models.Model):
    question_id = models.IntegerField(default=0)
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
    def __str__(self):
        return str(self.userID)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    flash = models.IntegerField(default=0)
    ambient = models.IntegerField(default=0)
    flashTemp = models.IntegerField(default=0)
    flashTempRange = models.IntegerField(default=0)
    ambientTemp =  models.IntegerField(default=0)
    ambientBrightness = models.FloatField(default=0)
    user = models.IntegerField(default=0)
    illuminant = models.IntegerField(default=0)
