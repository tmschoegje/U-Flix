from .models import Query, Result, InterviewSession, typeOrder, RandomisationOrder, Answer
import numpy as np 

def printResults(answers):
	seconds = []
	selecteds = []
	likerts = []
	for answer in answers:
		if answer.manual_id != 0:
			likerts.append(answer.likert)
		seconds.append(answer.answeringTimeS)
		selecteds.append(answer.numSelected)
	print('likert')
	print(np.mean(likerts))
	print('seconds')
	print(np.mean(seconds))
	print('selecteds')
	print(np.mean(selecteds))
	
	
#avg per search engine:
#1. get all questions per search engine
as1 = []
as2 = []
as3 = []
for order in RandomisationOrder.objects.filter(searchtype=0)
	ans = Answer.objects.filter(randomisationId=order.manual_id, presentedId = presentOrder)
	as1.append(ans.question)

printResults(as1)
	
#for order in RandomisationOrder.objects.filter(searchtype=0)
#	qs2.append(order.question)
#for order in RandomisationOrder.objects.filter(searchtype=2)
#	qs3.append(order.question)

#for ans in Answer.objects.filter(=""):


#get an answer: need orderId and 