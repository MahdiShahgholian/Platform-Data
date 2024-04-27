from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import CsvForm
from .models import Csv
import h2o
from h2o.automl import H2OAutoML
import pandas as pd
import os
from django.conf import settings


def services_view(request):
    return render(request, 'services/index.html')

def ml_view(request):
    return render(request, 'services/machine_learning.html')

def arka_view(request):
    return render(request, 'services/arka.html')


def import_view(request):
    if request.method == "POST":
        form = CsvForm(request.POST, request.FILES)
        if form.is_valid():
            csv_instance = form.save(commit=False)
            csv_instance.user = request.user  
            csv_instance.save()
            msg = 'Successful'
            return redirect('/services/machine_learning/success_upload')
    else:
        form = CsvForm()
    context = {'form': form}
    return render(request, 'services/import.html', context)
'''
from django.forms.widgets import Table, TableHead, TableBody, Row, Cell

def html_table_from_df(df, table_name):
    # Define table head
    table_head = TableHead(cells=[Cell(str(column)) for column in df.columns])
    
    # Define table rows
    table_rows = []
    for index, row in df.iterrows():
        table_rows.append(Row(cells=[Cell(str(value)) for value in row]))
    
    # Define table body
    table_body = TableBody(rows=table_rows)
    
    # Define table
    table = Table(head=table_head, body=table_body, name=table_name)
    
    # Convert table to HTML string
    html_table = str(table)
    
    return html_table
'''

def train_view(request):
    if request.method == 'POST':
        file = os.path.join(settings.MEDIA_ROOT, request.POST.get('dataset'))
        df = pd.read_csv(file)
        column_names = df.columns.tolist()
        range = [1,2,3,4,5,6,7,8,9,10]
        context = {'user_csvs': Csv.objects.filter(user=request.user), 'column_names': column_names, 'range': range}
        if (request.POST.get('column_names') != None) & (request.POST.get('number') != None):
            h2o.init()  # شروع H2O
            h2o_df = h2o.H2OFrame(df)
            y = request.POST.get('column_names')
            #h2o_df[y] = h2o_df[selected_column].asfactor()  
            aml = H2OAutoML(max_models=int(request.POST.get('number')), seed=1)
            aml.train(y=y, training_frame=h2o_df)
            
            # دریافت نتایج
            leaderboard = aml.leaderboard
            results = leaderboard.as_data_frame()
            
            table = results
            # برگرداندن نتایج به صورت JSON
            return render(request, 'services/leaderboard.html', {'leaderboard': table})
        
        return render(request, 'services/train.html', context)
        
    else:
        user_csvs = Csv.objects.filter(user=request.user)
        range = [1,2,3,4,5,6,7,8,9,10]
        context = {'user_csvs': user_csvs, 'range': range}
        
        return render(request, 'services/train.html', context)


def success_upload_view (request):
    return render(request, 'services/success_upload.html')