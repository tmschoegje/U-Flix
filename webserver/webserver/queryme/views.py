from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .query import qry

# Create your views here.
def index(request):
	query = request.GET.get('query', '')
	start = request.GET.get('start', '')
	if(not start):
		start = 1
	#print(start)
	#print('HELPP HLEP')

	return JsonResponse({'results': qry(query, start)})
#	{'results':'this is a list of stuff'})
	#HttpResponse("Hello, world. Queryme speaking.")