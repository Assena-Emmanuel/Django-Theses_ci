from django.urls import path
from . import views

app_name = "theses_ci"

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:these_id>/', views.detail, name='detail'),
    path('ajoute_these/', views.these_etape1, name='these_etape1'),
    path('ajoute_these/suivant', views.these_etape2, name='these_etape2'),
    path('ajoute_these/precedent', views.precedent, name='precedent'),
    path('ajoute_these/succes', views.succes, name='succes'),
    path('resultat/', views.resultat, name='resultat'),
    # path('resultat/<str:all>', views.resultat_all, name='resultat_all'),
]