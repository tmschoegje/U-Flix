from django.contrib import admin
from .models import Query, Result, InterviewSession, typeOrder, RandomisationOrder, Answer

# Register your models here.
admin.site.register(Query)
admin.site.register(Result)
admin.site.register(Answer)
admin.site.register(RandomisationOrder)
admin.site.register(InterviewSession)
admin.site.register(typeOrder)