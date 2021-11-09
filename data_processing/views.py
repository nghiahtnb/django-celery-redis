from django.shortcuts import render
from django.http import HttpResponse
import os

from . import tasks

# Create your views here.
PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))

def demo(request):
    input_dir = os.path.join(PROJECT_PATH, "test_data/input")
    output_dir = os.path.join(PROJECT_PATH, "test_data/output")
    csvs = os.listdir(input_dir)
    csvs = [os.path.join(input_dir, i) for i in csvs if i.endswith(".xlsx")]
    task = tasks.csv_processing.delay(csvs, output_dir)
    return render(request, "data_processing/index.html", {"message": "Start Processing", "task_id": task.task_id})