from django.urls import path
from .views import *

app_name = 'services'

urlpatterns = [
    path('', services_view, name = 'index'),
    path('/machine_learning', ml_view, name = 'machine_learning'),
    path('/machine_learning/import', import_view, name = 'import'),
    path('/machine_learning/train', train_view, name = 'train'),
    path('/machine_learning/success_upload', success_upload_view, name = 'success_upload'),

]