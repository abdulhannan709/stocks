from django.http import HttpResponse, Http404
from django.shortcuts import render
import pandas as pd
from pandas_datareader import data as web
import plotly.graph_objects as go
from pandas import ExcelWriter
import os
from django.conf import settings
import requests
import json


def index(request):
    return HttpResponse("Home")

def charts(request):
    stock = 'MSFT'
 
    df = web.DataReader(stock, data_source='yahoo', start='01-01-2019')

    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': 'MSFT',
        'showlegend': True
    }
    # Calculate and define moving average of 30 periods
    avg_30 = df.Close.rolling(window=30, min_periods=1).mean()

    # Calculate and define moving average of 50 periods
    avg_50 = df.Close.rolling(window=50, min_periods=1).mean()
    trace2 = {
        'x': df.index,
        'y': avg_30,
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'blue'
                },
        'name': 'Moving Average of 30 periods'
    }

    trace3 = {
        'x': df.index,
        'y': avg_50,
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'red'
        },
        'name': 'Moving Average of 50 periods'
    }
    data = [trace1, trace2]
    # Config graph layout
    layout = go.Layout({
        'title': {
            'text': 'BBAS3 - BRASIL ON',
            'font': {
                'size': 15
            }
        }
    })
    fig = go.Figure(data=data, layout=layout)
    fig.write_html("./BBAS3-web.html")
    fig.show()

    return render(request, 'charts.html', {'response': data})

def uvolume(request):

    url = "https://twelve-data1.p.rapidapi.com/stocks"

    querystring = {"exchange": "NASDAQ", "format": "json"}

    headers = {
        'x-rapidapi-key': "9c714f9a9fmsh22461f0b6d7e572p1bb1b3jsn9e2c7d195b1c",
        'x-rapidapi-host': "twelve-data1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)

    return render(request, 'unusualvolume.html', {'response': response})


def equity(request):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"

    querystring = {"symbol":"AMRN","region":"US"}

    headers = {
        'x-rapidapi-key': "9c714f9a9fmsh22461f0b6d7e572p1bb1b3jsn9e2c7d195b1c",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)

    print(response)
    return render(request, 'equitylevel.html', {'response': response})

def help(request):
    return render(request, 'help.html')

def exporttool(request):

    stock = 'MSFT'
    df = web.DataReader(stock, data_source='yahoo', start='01-01-2019')
    writer = ExcelWriter('PythonExport.xlsx')
    df.to_excel(writer,'Sheet1')
    writer.save()
    return render(request, 'exporttool.html')



def download(request, path):
    # file_path = os.path.join(settings.MEDIA_ROOT, path)
    # if os.path.exists(''):
    print('download')
    file_path = './PythonExport.xlsx'
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
    raise Http404
