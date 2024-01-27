from django.shortcuts import render, redirect
from .forms import TickerInput
from .models import Visitor, Ticker
import requests, json

from django.db import connection
from django.http import JsonResponse

# Create your views here.
def index(request):
    input_text = request.POST.get('visitor_input', None)
    if input_text == None:
        input_text = ''
    else:
        input_text = request.POST.get('visitor_input', "you didn't enter anything")
    
    visitors = Visitor.objects.all()

    context = {
        'visitors': visitors,
        'input_text': input_text
    }
    return render(request, 'index.html', context)


def view_data(request):

    api_res = ''
    entered_ticker = ''
    data_open_close = []
    data_close = []
    tickers = Ticker.objects.all()


    average_open_dsp = 0
    average_close_dsp = 0

    min_open_dsp = 0
    max_close_dsp = 0 
    

    if request.method == 'POST':
        form = TickerInput(request.POST)
        entered_ticker = request.POST['ticker_input'].upper()

        try:
            api_request = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey=P9W97OWLOBN76RBK".format(entered_ticker))

            api_res = api_request.json()['Time Series (Daily)']
            data_open_close = [[x, api_res[x]['1. open'], api_res[x]['4. close']] for x in api_res]
            data_close = [[x, api_res[x]['4. close']] for x in api_res]

            obj, created = Ticker.objects.get_or_create(
                ticker_name=api_request.json()['Meta Data']['2. Symbol'],
                dates=str(list(api_res.keys())),
                price_open=str([api_res[x]['1. open'] for x in api_res]),
                price_high=str([api_res[x]['2. high'] for x in api_res]),
                price_low=str([api_res[x]['3. low'] for x in api_res]),
                price_close=str([api_res[x]['4. close'] for x in api_res]),
                volume=str([api_res[x]['5. volume'] for x in api_res]),

                average_open=sum([float(api_res[x]['1. open']) for x in api_res]) / len([api_res[x]['1. open'] for x in api_res]),
                average_close=sum([float(api_res[x]['4. close']) for x in api_res]) / len([api_res[x]['4. close'] for x in api_res]),
                min_open=min([float(api_res[x]['1. open']) for x in api_res]),
                max_close=max([float(api_res[x]['4. close']) for x in api_res])
            )


        except Exception as e:
            api_res = "Error..."

        current_ticker_obj = Ticker.objects.get(ticker_name=entered_ticker)
        
        average_open_dsp = current_ticker_obj.average_open
        average_close_dsp = current_ticker_obj.average_close

        min_open_dsp = current_ticker_obj.min_open
        max_close_dsp = current_ticker_obj.max_close


        context = {
            'form': form,
            'tickers': tickers,
            'api_res': api_res,
            'data_open_close': data_open_close,
            'data_close': data_close,
            'entered_ticker': entered_ticker,
            'average_open_dsp': average_open_dsp,
            'average_close_dsp': average_close_dsp,
            'min_open_dsp': min_open_dsp,
            'max_close_dsp': max_close_dsp
        }

        return render(request, 'data_page.html', context)
    else:
        form = TickerInput()

    context = {
        'form': form,
        'tickers': tickers,
        'api_res': api_res,
        'data_open_close': data_open_close,
        'data_close': data_close,
        'entered_ticker': entered_ticker,
        'average_open_dsp': average_open_dsp,
        'average_close_dsp': average_close_dsp,
        'min_open_dsp': min_open_dsp,
        'max_close_dsp': max_close_dsp
    }
    return render(request, 'data_page.html', context)

def view_data_tmp(tkr):

    api_request = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey=EVKWQOL8PYGMPDWC".format(tkr))

    if api_request.status_code == 200:
        return api_request.json()['Meta Data']['2.Symbol']
    else:
        return 'Something went wrong...'
    
def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        return JsonResponse({ 'message': 'ok' }, status=200)
    except Exception as ex:
        return JsonResponse({ 'error': str(ex) }, status=500)
    
def metrics_data(request):
    pass