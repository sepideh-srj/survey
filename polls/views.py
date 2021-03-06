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
from .resources import QuestionResource
import random
import time
from datetime import datetime
notInNext = True
oldtime = 0
# from skimage import img_as_float,color
def home(request):

    if request.method == 'POST':
        if 'start' in request.POST:
            lastUser = User.objects.all().last()
            questions = Question.objects.all()

            ids = []
            # ids2 = []
            for question in questions:
                if question.question_id != 3:
                    ids.append(question.question_id)
                # ids2.append(question.question_id)
            random.shuffle(ids)
            # random.shuffle(ids2)
            # for i in range(len(ids2)):
            #     ids.append(ids2[i])
                # ids2.append(question.question_id)
            print("here")
            print(ids)
            ids.insert(0,3)
            print("here2")
            print(ids)
            print("ccc")
            listToStr = ','.join([str(elem) for elem in ids])
            userID = lastUser.userID +1;
            gender=request.POST['gender']
            print(request.POST['age'])
            
            code = random.randint(1000,10000)  
            print(code)  
            newUser = User(userID = userID,code=code, order= listToStr, pointer=0, gender= gender, age = request.POST['age'], experience = request.POST['experience'])
            newUser.save()
            print(listToStr)
            questions = Question.objects.all()
            question_id = ids[0]
            print(request)
            return redirect("/polls/vote/"+str(userID)+"/"+str(question_id))

    return render(request,'polls/home.html')

# def index(request, num):
#     global randomVar
#     print("index:{}".format(randomVar))
#     # print(num)
#     question_list = Question.objects.all().order_by('?')

#     context = {'question_list': question_list, 'num':num}

    # return render(request, 'polls/index.html', context)


def end(request,userID):
    user = User.objects.get(userID=userID)
    code = user.code
    return render(request, 'polls/end.html', {'code': code})


def process(request):
    quest = Question.objects.get(question_id=14)

    image = quest.ambientPic
    image = Image.open(image)
    des = int(image.info['Description'])
    matrix = image.info['Comment']
    color = float(image.info['Warning'])
    print("warning")
    print(float(image.info['Warning']))
    image = quest.ambientPic
    image = Image.open(image)

    colorAm = image.info['Warning']
    flash = 159
    ambient = 27
    flashTemp = 83
    ambientTemp = 50
    ambientBrightness = 35

    return render(request, 'polls/process.html', {'question': quest,'des': des, 'matrix': matrix, 'flash': flash, 'colorAm': colorAm, 'ambient': ambient, 'flashTemp': flashTemp, 'ambientTemp':ambientTemp, 'ambientBrightness': ambientBrightness, 'color':color})

def vote(request, question_id, userID):
    quest = Question.objects.get(question_id=question_id)
    numberOfPics = Question.objects.count();
    # shuffle = list(range(1,5))
    print("vote: request: ={}".format(request))
    # pointer = pointer +1
    image = quest.flashPic
    image = Image.open(image)
    startTime = datetime.now()
    global notInNext
    global oldtime
    # this.notInNext = notInNext
    print("boolean:{}".format(notInNext))
    if (notInNext):
        oldtime = startTime
        print("time:{}".format(startTime))
        notInNext = False
    des = int(image.info['Description'])
    matrix = image.info['Comment']
    # color =image.info['Warning']
    # image = quest.ambientPic
    # image = Image.open(image)
    # colorAm = image.info['Warning']

    # print(color)
    # print(request.POST)
    user = User.objects.get(userID=userID)

    pointer = user.pointer
    if request.method == 'POST':
        # if 'back' in request.POST:
        #     question_list = Question.objects.all()
        #     context = {'question_list': question_list, 'userID': userID}
        #     return render(request, 'polls/index.html', context)

        if 'next' in request.POST:

            vote_form = voteForm()
            finishTime = datetime.now()
            thisTime = (finishTime - oldtime).total_seconds()
            notInNext = True
            print("this time:{}".format(thisTime))
            print("finish time:{}".format(finishTime))
            print("start time:{}".format(startTime))
            quest.choice_set.create(time = thisTime, questionID = question_id, flash=10*float(request.POST['mixRange']), ambient=220 - 10*float(request.POST['mixRange']),
                flashTempRange=((float(request.POST['flashTempRange'])-30)/36)*100, ambientBrightness= request.POST['changedBrightness'],  flashBrightness= request.POST['changedBrightnessFlash'], flashTemp= float(request.POST['changedColorFlash'])
                ,user = userID, illuminant=des, code = user.code)
            quest.save()
            question_list = Question.objects.all()
            user = User.objects.get(userID=userID)
            pointer = user.pointer
            print("question_id:{}".format(question_id))
            pointer = pointer + 1
            user.pointer = pointer
            user.save()
            order = user.order
            order = order.split(',')
            print("userID:{}".format(userID))
            if (Question.objects.count()== pointer):
                return redirect("/polls/end/"+str(userID))
            question_id = int(order[pointer])
            print("question_id:{}".format(question_id))
            return redirect("/polls/vote/"+str(userID)+"/"+str(question_id))
    vote_form = voteForm()
    print(request)
    return render(request, 'polls/vote.html', {'question': quest, 'question_id': question_id,'vote_form':vote_form, 'des': des, 'matrix': matrix, 'userID': userID, 'pointer':pointer, 'numberOfPics': numberOfPics})

# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
# def returnBlend(request, question_id):
#     quest = Question.objects.get(pk=question_id)
#     edit = request.POST['edit']
#     image = merge_images(quest.flashPic,quest.ambientPic,float(edit))
#     return HttpResponse(image.read(), content_type="image/jpeg")

# def merge_images(field1,field2,opacity):

#     image1 = Image.open(field1)
#     image2 = Image.open(field2)
#     height,width = image1.size
#     des = int(image1.info['Description'])
#     matrix = image1.info['Comment']
#     matrix = list(map(float, matrix.split("     ")))

#     image3 = img_as_float(image1)
#     image4 = img_as_float(image2)
#     blended = image3*opacity/100 + image4* (100-opacity)/100
#     # blended = cameraToXYZtoSRGB(blended,matrix, des,image1.size)

#     # plt.imshow(blended1)
#     # im = (blended * 255 / np.max(blended)).astype('uint8')
#     im = cameraToXYZtoSRGB(blended, matrix, des, image1.size)
#     im = color.xyz2rgb(im)
#     im = (im * 255 / np.max(im)).astype('uint8')
#     im = Image.fromarray(im)

#     output = io.BytesIO()
#     im.save(output, format='PNG', quality=100)
#     output.seek(0)
#     return InMemoryUploadedFile(output, 'ImageField',
#                                 field1.name,
#                                 'im/jpeg',
#                                 sys.getsizeof(output), None)

# def fixWhitePoint(calibrationIlluminant):
#     d65 = [0.9504, 1.0000, 1.0888]
#     if (calibrationIlluminant == 17): # code a
#         makhraj = [1.0985, 1.0000, 0.3558]
#     elif calibrationIlluminant == 19: # code c
#         makhraj = [0.9807, 1.0000, 1.1822]
#     elif calibrationIlluminant == 20: # code d55
#         makhraj = [0.9568, 1.0000, 0.9214]
#     elif calibrationIlluminant == 21: # code d65
#         makhraj = d65
#     elif calibrationIlluminant == 23: # code d50
#         makhraj =  [0.9642, 1.0000, 0.8251]
#     return np.divide(d65,makhraj)


# def cameraToXYZtoSRGB(imgFloat, colorMatrix, calibrationIlluminant,size):
#     # imgFloat = img_as_float(image)
#     XYZtoCamera = np.reshape(colorMatrix,(3,3),order='F')
#     XYZtoCamera = np.transpose(XYZtoCamera)
#     width, height = size

#     imf = np.reshape(imgFloat, [width*height, 3], order='F')
#     imf = np.transpose(imf)

#     imf = np.linalg.lstsq(XYZtoCamera,imf)[0]

#     imf = np.transpose(imf)
#     imf = np.reshape(imf, [height, width, 3], order='F')
#     zarib = fixWhitePoint(calibrationIlluminant)
#     imf[:,:,0] = zarib[0] * imf[:,:,0]
#     imf[:,:,2] = zarib[2] * imf[:,:,2]
#     return imf
# print("id")


# print("sepide")
# randomVar = random.randint(1,50)
# print("main:{}".format(shuffle))

