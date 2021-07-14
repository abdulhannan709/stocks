from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Home")

def charts(request):
        
    # import pandas as pd
    # from pandas_datareader import data as web
    # import plotly.graph_objects as go

    # stock = 'MSFT'
 
    # df = web.DataReader(stock, data_source='yahoo', start='01-01-2019')

    # trace1 = {
    #     'x': df.index,
    #     'open': df.Open,
    #     'close': df.Close,
    #     'high': df.High,
    #     'low': df.Low,
    #     'type': 'candlestick',
    #     'name': 'MSFT',
    #     'showlegend': True
    # }

    # data = [trace1]
    # # Config graph layout
    # layout = go.Layout({
    #     'title': {
    #         'text': 'Microsoft(MSFT) Moving Averages',
    #         'font': {
    #             'size': 15
    #         }
    #     }
    # })
    # return render(request, 'charts.html', {'response': data})
    return render(request, 'charts.html')

def uvolume(request):
    import requests
    import json

    url = "https://twelve-data1.p.rapidapi.com/stocks"

    querystring = {"exchange": "NASDAQ", "format": "json"}

    headers = {
        'x-rapidapi-key': "9c714f9a9fmsh22461f0b6d7e572p1bb1b3jsn9e2c7d195b1c",
        'x-rapidapi-host': "twelve-data1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)

    return render(request, 'unusualvolume.html', {'response': response})