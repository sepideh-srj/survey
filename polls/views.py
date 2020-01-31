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
import numpy as np
from skimage import img_as_float,color
import matplotlib.pyplot as plt


def index(request):
    question_list = Question.objects.all()
    for question in question_list:
        # question.flashPic = fixPic(question.flashPic)
        # question.ambientPic = fixPic(question.ambientPic)
        # question. flashPic = resize(question.flashPic)
        # question.ambientPic = resize(question.ambientPic)
        image = merge_images(question.flashPic,question.ambientPic,50)
        # plt.imshow(question.flashPic)
        # plt.show()
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

def resize(image):
    # image = Image.open(image)
    print(image.size[0])
    print(image)
    # widthRatio  = maxWidth/image.size[0]
    # heightRatio = maxHeight/image.size[1]

    # newWidth    = int(widthRatio*image.size[0])
    # newHeight   = int(heightRatio*image.size[1])

    # newImage    = image.resize((newWidth, newHeight))
    return image
    
def merge_images(field1,field2,opacity):

    image1 = Image.open(field1)
    image2 = Image.open(field2)
    image3 = fixPic(image1)
    image4 = fixPic(image2)

    # image3 = changeImageSize(800, 500, image1)
    # image4 = changeImageSize(800, 500, image2)
    # image5 = image3.convert("RGBA")
    # image6 = image4.convert("RGBA")

    blended = image3*opacity/100 + image4* (100-opacity)/100
    blended1 = color.xyz2rgb(blended)
    print(type(blended1))
    # plt.imshow(image3)
    # plt.show()
    # alphaBlended = Image.blend(image3, image4, alpha=opacity/100)
    # alphaBlended = alphaBlended.convert('RGB')
    # image = image.resize((800, 800), Image.ANTIALIAS)
    plt.imshow(blended1)
    im = (blended1 * 255 / np.max(blended1)).astype('uint8')
    im = Image.fromarray(im)


    # plt.show()
    output = io.BytesIO()
    im.save(output, format='PNG', quality=100)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField',
                                field1.name,
                                'im/jpeg',
                                sys.getsizeof(output), None)



def fixPic(img):
    # print(image)
    # img = Image.open(field)
    height,width = img.size
    des = int(img.info['Description'])
    matrix = img.info['Comment']
    matrix = list(map(float, matrix.split("     ")))
    return cameraToXYZtoSRGB(img, matrix, des)

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


def cameraToXYZtoSRGB(image, colorMatrix, calibrationIlluminant):
    imgFloat = img_as_float(image)
    XYZtoCamera = np.reshape(colorMatrix,(3,3),order='F')
    XYZtoCamera = np.transpose(XYZtoCamera)
    width, height = image.size
    
    imf = np.reshape(imgFloat, [width*height, 3], order='F')
    imf = np.transpose(imf)

    imf = np.linalg.lstsq(XYZtoCamera,imf)[0]

    imf = np.transpose(imf)
    imf = np.reshape(imf, [height, width, 3], order='F')
    zarib = fixWhitePoint(calibrationIlluminant)
    imf[:,:,0] = zarib[0] * imf[:,:,0]
    imf[:,:,2] = zarib[2] * imf[:,:,2]
    return imf    
