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
    return render(request, 'index.html')

def charts(request):
    symbol = request.GET.get('sticker')
    start_date = request.GET.get('data_start')
    end_date = request.GET.get('data_end')
    if symbol:
    
        df = web.DataReader(symbol, data_source='yahoo', start=start_date)

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
        fig.write_image("./static/tradify/chart.png")

        return render(request, 'charts.html', {'response': data, 'chart':'True'})
    return render(request, 'charts.html', {'chart':'False'})

def uvolume(request):

    url = "https://twelve-data1.p.rapidapi.com/stocks"

    querystring = {"exchange": "NASDAQ", "format": "json"}

    headers = {
        'x-rapidapi-key': "9c714f9a9fmsh22461f0b6d7e572p1bb1b3jsn9e2c7d195b1c",
        'x-rapidapi-host': "twelve-data1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)

    return render(request, 'unusualvolume.html', {'response': response['data'][1:100]})


def equity(request):
    symbol = request.GET.get('sticker')
    start_date = request.GET.get('data-start')
    strength = request.GET.get('MStrength')

    if symbol:
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"

        querystring = {"symbol":symbol,"region":"US"}

        headers = {
            'x-rapidapi-key': "9c714f9a9fmsh22461f0b6d7e572p1bb1b3jsn9e2c7d195b1c",
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response = json.loads(response.text)

        return render(request, 'equitylevel.html', {'response': response})
    return render(request, 'equitylevel.html')

def help(request):
    return render(request, 'help.html')

def exporttool(request):
    symbol = request.GET.get('sticker')
    start_date = request.GET.get('data-start')

    if symbol:
        df = web.DataReader(symbol, data_source='yahoo', start=start_date)
        writer = ExcelWriter('PythonExport.xlsx')
        df.to_excel(writer,'Sheet1')
        writer.save()
    return render(request, 'exporttool.html')


def download(request):
    print('download')
    file_path = './PythonExport.xlsx'
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
