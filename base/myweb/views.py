from django.shortcuts import render, redirect
import json, requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from .forms import HistoryForm
from .forms import NowStock
from .forms import CustomizeForm
from django.views.generic.base import View, TemplateView
from .models import StockHistory
from django.urls import reverse

class Base(View):
    def get(self, request):
        return render(request, 'home.html')

class StockHistoryForm(View):
    def get(self, request):
        form = HistoryForm()
        return render(request, 'stock_history_form.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = HistoryForm(request.POST)
        if form.is_valid():
            stocknm = form.cleaned_data['stocknm']
            stockmonth1 = form.cleaned_data['stockmonth1']
            stockmonth2 = form.cleaned_data['stockmonth2']
            stockmonth1 = form.cleaned_data['stockmonth1'].replace('/', '-')
            stockmonth2 = form.cleaned_data['stockmonth2'].replace('/', '-')
            stock_history = StockHistory.objects.filter(
                stock_num__contains=stocknm + '.', stock_date__range=(stockmonth1, stockmonth2)
                ).using('stockdb').values_list(
                'stock_name', 'stock_num', 'stock_price', 'stock_open', 'stock_highest', 'stock_lowest', 'stock_date', 'turnover'
                ).all()
            stock_history = list(stock_history)
            df = pd.DataFrame(stock_history, columns=['stock_name', 'stock_num', 'stock_price', 'stock_open', 'stock_highest', 'stock_lowest', 'stock_date', 'turnover'])
            df = df.sort_values(by='stock_date', ascending=False)
            json_records = df.to_json(orient='records')
            data = []
            data = json.loads(json_records)
            return render(request, 'stock_history.html', context={'d' : data})
        else:
            return render(request, 'stock_history_form.html', {'form': form})

class NowStockForm(View):
    def get(self, reqest):
        form = NowStock()
        return render(reqest, 'nowstock_form.html', {'form': form})
    
    def post(self, request):
        if request.method == 'POST':
            form = NowStock(request.POST)
        if form.is_valid():
            stocknm = form.cleaned_data['stocknm'].split(' ')
            def not_empty(lis):
                return lis and lis.strip()
            stocknm = list(filter(not_empty, stocknm))
            df, notfindlist = self.get_data(stocknm)
            json_records = df.to_json(orient='records')
            data = []
            data = json.loads(json_records)
            return render(request, 'nowstock.html', context={'d' : data, 'n' : notfindlist})
        else:
            return render(request, 'nowstock.html', {'form': form})
    def get_data(self, nms):
        MainList = [['stock_name', 'stock_num', 'stock_price', 'stock_open', 'stock_highest', 'stock_lowest', 'stock_date','turnover', 'time']]
        notfindlist = []
        for x in range(len(nms)):
            web = requests.get(f'https://isin.twse.com.tw/isin/class_main.jsp?owncode={nms[x]}&stockname=&isincode=&market=&issuetype=&industry_code=&Page=1&chklike=Y')
            soup = bs(web.text, 'lxml')
            if soup.select('tr+ tr td:nth-child(5)'):
                data = soup.select('tr+ tr td:nth-child(5)')[0].text.strip()
            else:
                notfindlist.append(nms[x])
                continue
            if data == '上市':
                id = 'tse'
            else:
                id = 'otc'
            nm = id + f'_{nms[x]}.tw'
            web = requests.get(f'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={nm}')
            datas = web.json()
            # MainList = [['stock_name', 'stock_num', 'stock_price', 'stock_open', 'stock_highest', 'stock_lowest', 'stock_date','turnover']]
            for data in datas['msgArray']:
                datatoday = f"{data['d'][:4:]}-{data['d'][4:6]}-{data['d'][6:]}"
                if data['ex'] == 'tse':
                    num = data['c'] + '.TW'
                else:
                    num = data['c'] + '.TWO'
                InList = [data['n'], num, data['z'], data['o'], data['h'], data['l'], datatoday, data['v'], data['t']]
                MainList.append(InList)
        df = pd.DataFrame(MainList[1:], columns=MainList[0])
        df.iloc[:,2:6] = round(df.iloc[:,2:6].astype(float), 2)
        df.iloc[:,2:6] = df.iloc[:,2:6].astype(str)
        return df, notfindlist
    
        
class StockCustomize(View):
    def get(self, reqest):
        form = CustomizeForm()
        return render(reqest, 'customize.html', {'form' : form})
    
    def post(self, request):
        pass

