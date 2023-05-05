from django.shortcuts import render
import json
import pandas as pd
from .forms import HistoryForm
from sqlalchemy import create_engine, text
from django.views.generic.base import View, TemplateView
from .models import StockHistory


class Base(View):
    def get(self, request):
        return render(request, 'home.html')
    # def home(self, request, *args, **kwargs):
    #     template_name = "home.html'"
    #     return render(request, self.template_name)

class Stock(View):
    def get(self, request):
        form = HistoryForm()
        return render(request, 'stock_history_form.html', {'form': form})
    
    def post(self, request):
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
            context = {'stock_history': df.to_html()}
            json_records = df.to_json(orient='records')
            data = []
            data = json.loads(json_records)
            return render(request, 'stock_history.html', context={'d' : data})
        else:
            return render(request, 'stock_history_form.html', {'form': form})
    
    def stock_today(request):
        pass
    # def weather(request):
    #     return render(request, 'weather.html')
    
    # def stock(request):
    #     return render(request, 'stock.html')
    
    
    # def stock_history_form(request):
    #     if request.method == 'POST':
    #         form = HistoryForm(request.POST)
    #         if form.is_valid(): #表單提交後的邏輯
    #             stocknm = form.cleaned_data['stocknm']
    #             stockmonth1 = form.cleaned_data['stockmonth1'].replace('/', '-')#yyyy-mm-dd
    #             stockmonth2 = form.cleaned_data['stockmonth2'].replace('/', '-') 
    #             sql = f"SELECT * FROM `{stockmonth1[0:4]}` WHERE `stock_num` LIKE '{stocknm}.%' AND `stock_date` BETWEEN '{stockmonth1}' AND '{stockmonth2}'"
    #             df = database('root', '123456', 'localhost', 'stock').readmysql(sql=sql).sort_values(by='stock_date', ascending=False)
    #             # context = {
    #             #     'df' : df.to_html()
    #             # }
    #             json_records = df.to_json(orient='records')
    #             data = []
    #             data = json.loads(json_records)
    #             context = {'d' : data}

    #             return render(request, 'stock_history.html', context=context)
    #     else:
    #         form = HistoryForm()
    #         return render(request, 'stock_history_form.html', {'form': form})


class GetStock():
    def get_data(self, request):
        
        url = 'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch='
        return render(request)
        

class database():
    def __init__(self, user, password, host, db):
        self.user = user
        self.password = password
        self.host = host
        self.db = db
    
    def inmysql(self, data, tablename, if_exists='replace'):
        engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db}")
        data.to_sql(name = tablename, con = engine, if_exists= if_exists, index = False)
        print('in mysql')

    def readmysql(self, sql):
        engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db}")
        df = pd.read_sql(sql=text(sql), con=engine.connect())
        return df


