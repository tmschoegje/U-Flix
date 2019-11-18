from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

app_name = 'uiquery'
urlpatterns = [
    path('', views.index, name='index'),
	path('answer/<int:sessionId>/<int:randomId>/', views.answer, name='answer'),
	path('preparation/<int:sessionId>/', views.preparation, name='preparation'),
	path('<int:sessionId>/<int:randomId>/', views.experiment, name='experiment'),
	path('results', views.results, name='results'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)