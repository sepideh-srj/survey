from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question, Choice
from django.urls import reverse
from django.shortcuts import get_object_or_404
import json, io,sys
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import *
from .form import *
from PIL import Image
from django.core.files.images import ImageFile
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def index(request):
    question_list = Question.objects.all()
    for question in question_list:

        image = merge_images(question.flashPic,question.ambientPic,50)
        question.blendedPic = image
        question.chosenPic = image
        question.save()

    context = {'question_list': question_list}
    return render(request, 'polls/index.html', context)

def vote(request, question_id):
    quest = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        if 'check' in request.POST:
            print('check')
            vote_form = voteForm(data=request.POST)
            if vote_form.is_valid():
                print(quest)
                vote = vote_form.save(commit=False)
                vote.question = quest
                vote.save()
                # print(vote.votes)
                image = merge_images(quest.flashPic,quest.ambientPic,vote.edit)
                quest.chosenPic = image
                quest.save()     
        elif 'submit' in request.POST:
            print('submit')
            vote = 50
            vote_form = voteForm()
            obj = quest.choice_set.filter().last()
            print(obj)
            quest.finalchoice_set.create(finalChoice=obj.edit)
            quest.save() 
            question_list = Question.objects.all()
            context = {'question_list': question_list}
            return render(request, 'polls/index.html', context)  
        elif 'back' in request.POST:
            question_list = Question.objects.all()
            context = {'question_list': question_list}
            return render(request, 'polls/index.html', context) 
        else:
            vote_form = voteForm(data=request.POST)
            if vote_form.is_valid():
                print(quest)
                vote = vote_form.save(commit=False)
                vote.question = quest
                vote.save()
                # print(vote.votes)
                image = merge_images(quest.flashPic,quest.ambientPic,vote.edit)
                quest.chosenPic = image
                quest.save() 
                      
    else:
        vote_form = voteForm()
        vote = 50

    return render(request, 'polls/vote.html', {'question': quest, 'vote': vote, 'vote_form':vote_form}) 

def changeImageSize(maxWidth, 
                    maxHeight, 
                    image):
    
    widthRatio  = maxWidth/image.size[0]
    heightRatio = maxHeight/image.size[1]

    newWidth    = int(widthRatio*image.size[0])
    newHeight   = int(heightRatio*image.size[1])

    newImage    = image.resize((newWidth, newHeight))
    return newImage
    
def merge_images(field1,field2,opacity):

    image1 = Image.open(field1)
    image2 = Image.open(field2)
    image3 = changeImageSize(800, 500, image1)
    image4 = changeImageSize(800, 500, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    alphaBlended = Image.blend(image5, image6, alpha=opacity/100)
    alphaBlended = alphaBlended.convert('RGB')
    # image = image.resize((800, 800), Image.ANTIALIAS)
    output = io.BytesIO()
    alphaBlended.save(output, format='JPEG', quality=85)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField',
                                field1.name,
                                'alphaBlended/jpeg',
                                sys.getsizeof(output), None)
