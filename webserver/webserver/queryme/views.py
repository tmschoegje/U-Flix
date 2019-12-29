from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .query import qry
from .query import mlt

# Create your views here.
def index(request):
	return search(request)
	#HttpResponse("Hello, world. Queryme speaking.")
	
def search(request):
	query = request.GET.get('query', '')
	start = request.GET.get('start', '')
#	if(not start):
#		start = 1
	return JsonResponse({'results': qry(query, start)})

def recommend(request):
	query = request.GET.get('query', '')
	size = request.GET.get('size', '')
	return JsonResponse({'results': mlt(query, size)})