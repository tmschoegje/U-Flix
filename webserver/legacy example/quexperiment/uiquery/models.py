from django.db import models

class typeOrder(models.Model):
	order = models.CharField(max_length=200)
	
	def __str__(self):
		return str(self.order)

#id added automatically
class InterviewSession(models.Model):
	randomOrder = models.ForeignKey(typeOrder, on_delete=models.CASCADE)
	organisationPart = models.CharField(max_length=200, default="")
	email = models.CharField(max_length=200, default="")
	#orderId = models.ForeignKey(RandomisationOrder, on_delete=models.CASCADE)
	
	def __str__(self):
		return str(self.randomOrder + " " + str(self.email))

#10 total
class Query(models.Model):
	manual_id = models.IntegerField(default=-1)
	question = models.CharField(max_length=200)
	query = models.CharField(max_length=200)
	
	def __str__(self):
		return str(self.question)

#1 html chunk per query
class Result(models.Model):
	query = models.ForeignKey(Query, on_delete=models.CASCADE)
	engine = models.IntegerField(default=-1)
	html = models.CharField(max_length=400)
	
	def __str__(self):
		return "engineId " + str(self.engine) + " abs qId " + str(self.query.manual_id)
	
# Create your models here.
# filter, fakefilter, nofilter order
class RandomisationOrder(models.Model):
	manual_id = models.IntegerField(default=-1)
	question = models.ForeignKey(Query, on_delete=models.CASCADE)
	presentOrder = models.IntegerField(default=-1)
	searchtype = models.IntegerField(default=-1)
	typeOrder = models.IntegerField(default=-1)
	
	def __str__(self):
		return "randomId " + str(self.manual_id) + " presentId " + str(self.presentOrder) + " abs qId " + str(self.question.manual_id) + " engineId " + str(self.searchtype)
	
#absolute id added automatically
class Answer(models.Model):
	randomisationId = models.IntegerField(default=-1)
	presentedId = models.IntegerField(default=-1)
	binarySelections = models.CharField(max_length=200)
	numSelected = models.IntegerField(default=-1)
	likert = models.IntegerField(default=-1)
	answeringTimeS = models.IntegerField(default=-1)
	
	def __str__(self):
		return "randomId " + str(self.randomisationId) + " presentId " + str(self.presentedId) + ' numselected ' + str(self.numSelected)
	