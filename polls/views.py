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
from datetime import datetime
from django.contrib import messages 

notInNext = True
oldtime = 0

# from skimage import img_as_float,color
def home(request):

	if request.method == 'POST':
		if 'start' in request.POST:
			lastUser = User.objects.all().last()
			questions = Question.objects.all()
			allIDs = [[116,103], [118,101], [56,51], [3,114], [4,20], [132,59], [60,135],[134,136],[121,131],[122,141]]
			allIDs =  [[116,103]]
			rows = len(allIDs)
			index = [0,1]
			thisIDs = []
			for i in range(rows):
				rand = random.choice(index)
				thisIDs.append(allIDs[i][rand]) 
			print(thisIDs)	
			ids = []
			ids2 = []
			ids3 = []
			ids4 = []
			ids5 = []
			ids6 = []
			x = [1,2]
			for question in questions:
				if question.question_id in thisIDs:
					question.choiceSet = 0

					question.flash = 0
					question.temp = 0
					question.firstSet = False
					question.save()
					ids.append(question.question_id)
		

			for question in questions:
				if question.question_id in thisIDs:
					ids2.append(question.question_id) 
			for question in questions:
				if question.question_id in thisIDs:
					ids3.append(question.question_id) 
			for question in questions:
				if question.question_id in thisIDs:
					ids4.append(question.question_id) 
			for question in questions:
				if question.question_id in thisIDs:
					ids5.append(question.question_id)           
			for question in questions:
				if question.question_id in thisIDs:
					ids6.append(question.question_id) 

			random.shuffle(ids)
			random.shuffle(ids2)
			random.shuffle(ids3)
			random.shuffle(ids4)
			random.shuffle(ids5)
			random.shuffle(ids6)

			for i in range(len(ids2)):
				ids.append(ids2[i])
			for i in range(len(ids2)):
				ids.append(ids3[i])
			for i in range(len(ids2)):
				ids.append(ids4[i])
			for i in range(len(ids2)):
				ids.append(ids5[i]) 
			for i in range(len(ids2)):
				ids.append(ids6[i])   
	   
			print("here")
			print(ids)
			# ids.insert(0,3)
			print("here2")
			print(ids)
			print("ccc")
			listToStr = ','.join([str(elem) for elem in ids])
			print(listToStr)
			userID = lastUser.userID +1;
			gender=request.POST['gender']
			print(gender)
			code = random.randint(1000,10000)  
			print(code)  
			numberOfPics = rows*6;
			newUser = User(userID = userID,code=code, numberOfPics = numberOfPics, order= listToStr, setNum = 1, pointer=0, gender= gender, age = request.POST['age'], experience = request.POST['experience'])
			newUser.save()
			for question in questions:
				rand = random.choice(x)
				newUser.questuser_set.create(question_id = question.question_id, choiceSet = 0, setNum = rand,firstSet = False, secondSet = False, flash = 0, temp= 0)
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
	setNum = quest.set
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

	return render(request, 'polls/process.html', {'question': quest,'set': setNum,'des': des, 'matrix': matrix, 'flash': flash, 'colorAm': colorAm, 'ambient': ambient, 'flashTemp': flashTemp, 'ambientTemp':ambientTemp, 'ambientBrightness': ambientBrightness, 'color':color})

def vote(request, question_id, userID):
	user = User.objects.get(userID=userID)
	questions = user.questuser_set.all()

	quest = questions.get(question_id=question_id)
	mainQuest = Question.objects.get(question_id=question_id)
	# shuffle = list(range(1,5))
	print("vote: request: ={}".format(request))
	print("choiceset: {}".format(quest.choiceSet))
	# pointer = pointer +1
	image = mainQuest.flashPic
	image = Image.open(image)
	choiceSet = quest.choiceSet
	setNum = quest.setNum
	print(choiceSet)
	des = int(image.info['Description'])
	matrix = image.info['Comment']
	global notInNext
	global oldtime
	# color =image.info['Warning']
	# image = quest.ambientPic
	# image = Image.open(image)
	# colorAm = image.info['Warning']
	startTime = datetime.now()
	if (notInNext):
		oldtime = startTime
		print("time:{}".format(startTime))
		notInNext = False
	# print(color)
	# print(request.POST)
	user = User.objects.get(userID=userID)
	pointer = user.pointer
	setNum = quest.setNum
	print("setNum:{}".format(setNum))
	print("goNext:{}".format(request.POST.get('goNext')))
	if request.method == 'POST':
		# if 'back' in request.POST:
		#     question_list = Question.objects.all()
		#     context = {'question_list': question_list, 'userID': userID}
		#     return render(request, 'polls/index.html', context)\
		if (request.POST['goNext'] == "0"):
			print("goNext")
			messages.error(request, "Please choose one of the options")
			return redirect("/polls/vote/"+str(userID)+"/"+str(question_id)) 
		elif 'next' in request.POST:
			oldFlash = int(request.POST['flashBrightness'])
			vote_form = voteForm()
			# quest.choice_set.create(questionID = question_id, flash=request.POST['mixRange'], ambient=220 - int(request.POST['mixRange']),
			#     flashTempRange=((float(request.POST['flashTempRange'])-30)/36)*100, ambientBrightness= request.POST['changedBrightness'],  flashBrightness= request.POST['changedBrightnessFlash'], flashTemp= float(request.POST['changedColorFlash'])
			#     ,user = userID, illuminant=des)
			quest.save()
			choice = request.POST['choice']
			print("choice:{}".format(choice))
			if quest.setNum == 1:
				# more ambient
				if quest.firstSet == False:
					if choice == "1":
						quest.choiceSet = 1
					elif choice == "2":
						#more flash
						print("here")
						quest.choiceSet = 2
					elif choice == "3":
						# none
						quest.choiceSet = 3
					quest.setNum = 2
					quest.firstSet = True
				elif quest.firstSet == True:
					quest.setNum = 3
					if (choice == "1" and quest.choiceSet == 2):
						#more flash
						quest.choiceSet = 2
					elif (choice == "2" and quest.choiceSet == 1):
						#more ambient
						print("here")
						quest.choiceSet = 1
					elif (choice == "3" and quest.choiceSet == 3) :
						# none
						print("here4")
						quest.choiceSet = 3
						
					else:
						quest.choiceSet = 4
						print("why am i here")
						order = user.order
						print(order)
						order = order.split(',')
						intOrder = []
						for num in order:
							intOrder.append(int(num))
						print(quest.question_id)    
						indices = [i for i, x in enumerate(intOrder) if x == quest.question_id]
						for index in indices:
							if index > pointer:
								del intOrder[index]
								break
						print("after removal {}".format(intOrder))
						# order.append(quest.question_id)
						newOrder = ','.join([str(elem) for elem in intOrder])
						print(newOrder)
						user.order = newOrder
						numberOfPics = user.numberOfPics
						user.numberOfPics = numberOfPics -1
						user.save()
						print("numberOfPics {}".format(user.numberOfPics))
						quest.setNum = -1
						oldFlash = 110        
			elif quest.setNum == -1:
				if (quest.secondSet == False):
					if choice == "1":
						# temp 42
						quest.choiceSet = -1
					elif choice == "2":
						#temp 54
						quest.choiceSet = -2
					elif choice == "3":
						quest.choiceSet = -3
					quest.setNum = -2
					quest.secondSet = True 
				elif (quest.secondSet == True):
					if (choice == "1" and quest.choiceSet == -2):
						#temp 54
						quest.choiceSet = -2
					elif (choice == "2" and quest.choiceSet == -1):
						#temp 42
						quest.choiceSet = -1
					elif (choice == "3" and quest.choiceSet == -3) :
						print("here4")
						quest.choiceSet = -3
					else:
						quest.choiceSet = -4
						order = user.order
						print(order)
						order = order.split(',')
						intOrder = []
						for num in order:
							intOrder.append(int(num))
						print(quest.question_id)    
						indices = [i for i, x in enumerate(intOrder) if x == quest.question_id]
						for index in indices:
							if index > pointer:
								del intOrder[index]
								break
						print("after removal {}".format(intOrder))
						# order.append(quest.question_id)
						newOrder = ','.join([str(elem) for elem in intOrder])
						print(newOrder)
						user.order = newOrder
						numberOfPics = user.numberOfPics
						user.numberOfPics = numberOfPics -1
						user.save()
						print("numberOfPics {}".format(user.numberOfPics))
					quest.setNum = -3



			elif quest.setNum == 2:
				if (quest.firstSet == False):
					quest.firstSet = True
					quest.setNum = 1
					if choice == "1":
						quest.choiceSet = 1
					elif choice == "2":
						#more flash
						print("here")
						quest.choiceSet = 2
					elif choice == "3":
						# none
						quest.choiceSet = 3
				elif (quest.firstSet == True):
					quest.setNum = 3
					if (choice == "1" and quest.choiceSet == 2):
						quest.choiceSet = 1
					elif (choice == "2" and quest.choiceSet == 1):
						quest.choiceSet = 2
					elif (choice == "3" and quest.choiceSet == 3) :
						quest.choiceSet = 3
						
					else:
						quest.choiceSet = 4
						order = user.order
						print(order)
						order = order.split(',')
						intOrder = []
						for num in order:
							intOrder.append(int(num))
						print(quest.question_id)    
						indices = [i for i, x in enumerate(intOrder) if x == quest.question_id]
						print(quest.question_id)  
						for index in indices:
							if index > pointer:
								del intOrder[index]
								break
						print("after removal {}".format(intOrder))
						# order.append(quest.question_id)
						newOrder = ','.join([str(elem) for elem in intOrder])
						print(newOrder)
						user.order = newOrder
						numberOfPics = user.numberOfPics
						user.numberOfPics = numberOfPics -1
						user.save()
						print("numberOfPics {}".format(user.numberOfPics))
						quest.setNum = -1
						oldFlash = 110

   
				print("choice:{}".format(choice))
				print("quest.choiceSet:{}".format(quest.choiceSet))
			elif quest.setNum == -2:
				if (quest.secondSet == False):
					quest.setNum = -1
					quest.secondSet = True
					if choice == "1":
						quest.choiceSet = -1
					elif choice == "2":
						#more flash
						print("here")
						quest.choiceSet = -2
					elif choice == "3":
						# none
						quest.choiceSet = -3

				elif (quest.secondSet == True):
					if (choice == "1" and quest.choiceSet == -2):
						#temp 54
						quest.choiceSet = -1
					elif (choice == "2" and quest.choiceSet == -1):
						#temp 42
						quest.choiceSet = -2
					elif (choice == "3" and quest.choiceSet == -3) :
						print("here4")
						quest.choiceSet = -3
					else:
						quest.choiceSet = -4
						order = user.order
						print(order)
						order = order.split(',')
						intOrder = []
						for num in order:
							intOrder.append(int(num))
						print(quest.question_id)    
						indices = [i for i, x in enumerate(intOrder) if x == quest.question_id]
						for index in indices:
							if index > pointer:
								del intOrder[index]
								break
						print("after removal {}".format(intOrder))
						# order.append(quest.question_id)
						newOrder = ','.join([str(elem) for elem in intOrder])
						print(newOrder)
						user.order = newOrder
						numberOfPics = user.numberOfPics
						user.numberOfPics = numberOfPics -1
						print("numberOfPics {}".format(user.numberOfPics))
						user.save()
					quest.setNum = -3

			elif quest.setNum == 3:
				print("quest set num is 3")
				if (choice == "1"):
					quest.choiceSet = 1
				elif (choice == "2"):
					quest.choiceset = 2
				elif (choice == "3"):
					quest.choiceSet = 3
				else:
					quest.choiceSet = 4    
				# if (choice= "1")
				#     quest.choiceSet = 1
				x = [-1,-2]
				rand = random.choice(x)
				print(rand)
				quest.setNum = rand



			quest.save()
			print("choiceset:{}".format(quest.choiceSet))
			finishTime = datetime.now()
			thisTime = (finishTime - oldtime).total_seconds()
			notInNext = True
			print("flashBrightness:{}".format(request.POST['flashBrightness']))
			quest.choice_set.create(user = userID, code = user.code, time= thisTime, questionID = question_id, choice = request.POST['choice'], setNum = setNum, flash=int(request.POST['flashBrightness']), tempNum=request.POST['flashTemp'], temp = request.POST['changedColorFlash'])
			question_list = Question.objects.all()
			quest.flash = oldFlash
			quest.temp = int(request.POST['flashTemp'])
			quest.save()
			user = User.objects.get(userID=userID)
			pointer = user.pointer
			['141', '20', '56', '3', '135', '103', '136', '118', '121', '103', '141', '118', '56', '3', '20', '135', '121', '136', '103', '56', '3', '20', '136', '20', '141', '103', '136', '56', '135', '121', '118', '3', '118', '20', '56', '3', '121', '141', '103', '135', '136', '135', '136', '20', '121', '118']
			pointer = pointer + 1
			user.pointer = pointer
			user.save()
			order = user.order.split(',')
			print("userID:{}".format(userID))
			if (user.numberOfPics == pointer):
				return redirect("/polls/end/"+str(userID))
			# print("number:{}".format(numberOfPics))  
			print("order:{}".format(order))  
			question_id = int(order[pointer])
			print("question_id:{}".format(question_id))
			return redirect("/polls/vote/"+str(userID)+"/"+str(question_id)) 
	vote_form = voteForm()
	print(request)

	return render(request, 'polls/vote.html', {'mainQuest': mainQuest,'question': quest, 'question_id': question_id,'vote_form':vote_form, 'des': des, 'matrix': matrix, 'userID': userID, 'pointer':pointer, 'choiceSet': choiceSet, 'setNum': setNum, 'oldFlash':quest.flash, 'oldTemp':quest.temp})

