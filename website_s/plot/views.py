from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from .models import InputForm
from ._product_sentiment_analysis import _product_sentiment_analysis
import os

def index(request):
    os.chdir(os.path.dirname(__file__))
    result = None
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form2 = form.save(commit=False)
            psa = _product_sentiment_analysis(form2.K)
            psa.get_recent(form2.I, form2.L)
            result = 'tmp.png'
    else:
        form = InputForm()

    return render(request, 'index_1.html', {'form': form, 'result': result})

def search_and_load(request):
    context = dict()
    return render(request, 'index_1.html', context)

