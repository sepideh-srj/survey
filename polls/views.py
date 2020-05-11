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


# from skimage import img_as_float,color
def home(request):
  
    if request.method == 'POST':
        if 'start' in request.POST:
            lastUser = User.objects.all().last()
            questions = Question.objects.all()

            ids = []
            for question in questions:
                if question.question_id != 101 and question.question_id != 102 and question.question_id != 103 and question.question_id!=104:
                    print("here")
                    ids.append(question.question_id)
            print("here2")
            print(ids)
            random.shuffle(ids)    
            listToStr = ','.join([str(elem) for elem in ids]) 
            userID = lastUser.userID +1;
            newUser = User(userID = userID, order= listToStr, pointer=0)
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


def end(request):

    return render(request, 'polls/end.html')


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
    numberOfPics = Question.objects.count()-4;
    # shuffle = list(range(1,5))
    print("vote: request: ={}".format(request))
    # pointer = pointer +1
    image = quest.flashPic
    image = Image.open(image)

    des = int(image.info['Description'])
    matrix = image.info['Comment']
    color =image.info['Warning']
    image = quest.ambientPic
    image = Image.open(image)

    # if (question_id==2 or question_id==13 or question_id==18 or question_id==19 or question_id==30 or question_id==32):
    #     color = 4500
    # if (question_id==26 or question_id==27 or question_id==31):
    #     color = 5500
    # if (question_id == 34):
    #     color = 4846;
    color = 5500;
    if question_id==18 or question_id==13 or question_id==19:
        color = 4015;
    colorAm = image.info['Warning']

    print(color)
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
            quest.choice_set.create(ambient=request.POST['ambientRange'], flash=request.POST['flashRange'],
                flashTemp=float(request.POST['flashTempRange']), ambientBrightness= request.POST['changedBrightness'],  ambientTemp= request.POST['changedColor'], user = userID)
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
            if (Question.objects.count()-4 == pointer):
                return redirect("/polls/end/")
            question_id = int(order[pointer])
            print("question_id:{}".format(question_id))
            return redirect("/polls/vote/"+str(userID)+"/"+str(question_id))
    vote_form = voteForm()
    print(request)
    return render(request, 'polls/vote.html', {'question': quest, 'question_id': question_id,'vote_form':vote_form, 'des': des, 'color': color, 'colorAm': colorAm, 'matrix': matrix, 'userID': userID, 'pointer':pointer, 'numberOfPics': numberOfPics})

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