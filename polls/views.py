from django.shortcuts import render, redirect
from django.http import HttpResponse
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
import numpy as np
from skimage import img_as_float,color
import matplotlib.pyplot as plt


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
    image = quest.ambientPic
    image = Image.open(image)
    des = int(image.info['Description'])
    matrix = image.info['Comment']
    print(float(image.info['Warning']))
    exp = float(image.info['Warning'])
    print(request.POST)
    if request.method == 'POST':
        if 'back' in request.POST:
            question_list = Question.objects.all()
            context = {'question_list': question_list}
            return render(request, 'polls/index.html', context) 
    # if request.method == 'POST':
    #     if 'check' in request.POST:
    #         print('check')
    #         vote_form = voteForm(data=request.POST)
    #         if vote_form.is_valid():
    #             print(quest)
    #             vote = vote_form.save(commit=False)
    #             vote.question = quest
    #             vote.save()
    #             # print(vote.votes)
    #             image = merge_images(quest.flashPic,quest.ambientPic,vote.edit)
                
    #             print(vote.edit)
    #             quest.chosenPic = image
    #             quest.save()     
        elif 'submit' in request.POST:
            print('submit') 
            # print(changedExp)
            vote = 50
            vote_form = voteForm()
            # obj = quest.choice_set.filter().last()
            # print(obj)
            print('type of')
            print((request.POST['changedExp']))
            # quest.choice_set.create(ambient=request.POST['ambientRange'], flash=request.POST['flashRange'], 
            #     flashTemp=request.POST['flashTempRange'], ambientBrightness= request.POST['changedExp'])
            # quest.save() 
            question_list = Question.objects.all()
            context = {'question_list': question_list}
            return render(request, 'polls/index.html', context)  
        # elif 'back' in request.POST:
        #     question_list = Question.objects.all()
        #     context = {'question_list': question_list}
        #     return render(request, 'polls/index.html', context) 
    #     else:
    #         vote_form = voteForm(data=request.POST)
    #         if vote_form.is_valid():
    #             print(quest)
    #             vote = vote_form.save(commit=False)
    #             vote.question = quest
    #             vote.save()
    #             print(vote.edit)
    #             image = merge_images(quest.flashPic,quest.ambientPic,vote.edit)
    #             quest.chosenPic = image
    #             quest.save() 
                      
    else:
        vote_form = voteForm()
        vote = 50

    return render(request, 'polls/vote.html', {'question': quest, 'vote': vote, 'vote_form':vote_form, 'des': des, 'matrix': matrix, 'exp': exp}) 

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def returnBlend(request, question_id):
    quest = Question.objects.get(pk=question_id)
    edit = request.POST['edit']
    image = merge_images(quest.flashPic,quest.ambientPic,float(edit))
    return HttpResponse(image.read(), content_type="image/jpeg")

def merge_images(field1,field2,opacity):

    image1 = Image.open(field1)
    image2 = Image.open(field2)
    height,width = image1.size
    des = int(image1.info['Description'])
    matrix = image1.info['Comment']
    matrix = list(map(float, matrix.split("     ")))

    image3 = img_as_float(image1)
    image4 = img_as_float(image2)
    blended = image3*opacity/100 + image4* (100-opacity)/100
    # blended = cameraToXYZtoSRGB(blended,matrix, des,image1.size)

    # plt.imshow(blended1)
    # im = (blended * 255 / np.max(blended)).astype('uint8')
    im = cameraToXYZtoSRGB(blended, matrix, des, image1.size)   
    im = color.xyz2rgb(im)
    im = (im * 255 / np.max(im)).astype('uint8')
    im = Image.fromarray(im)

    output = io.BytesIO()
    im.save(output, format='PNG', quality=100)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField',
                                field1.name,
                                'im/jpeg',
                                sys.getsizeof(output), None)

def fixWhitePoint(calibrationIlluminant):
    d65 = [0.9504, 1.0000, 1.0888]
    if (calibrationIlluminant == 17): # code a
        makhraj = [1.0985, 1.0000, 0.3558]
    elif calibrationIlluminant == 19: # code c 
        makhraj = [0.9807, 1.0000, 1.1822]
    elif calibrationIlluminant == 20: # code d55
        makhraj = [0.9568, 1.0000, 0.9214]
    elif calibrationIlluminant == 21: # code d65
        makhraj = d65
    elif calibrationIlluminant == 23: # code d50
        makhraj =  [0.9642, 1.0000, 0.8251]             
    return np.divide(d65,makhraj)


def cameraToXYZtoSRGB(imgFloat, colorMatrix, calibrationIlluminant,size):
    # imgFloat = img_as_float(image)
    XYZtoCamera = np.reshape(colorMatrix,(3,3),order='F')
    XYZtoCamera = np.transpose(XYZtoCamera)
    width, height = size
    
    imf = np.reshape(imgFloat, [width*height, 3], order='F')
    imf = np.transpose(imf)

    imf = np.linalg.lstsq(XYZtoCamera,imf)[0]

    imf = np.transpose(imf)
    imf = np.reshape(imf, [height, width, 3], order='F')
    zarib = fixWhitePoint(calibrationIlluminant)
    imf[:,:,0] = zarib[0] * imf[:,:,0]
    imf[:,:,2] = zarib[2] * imf[:,:,2]
    return imf    
