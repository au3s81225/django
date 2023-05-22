from django import forms
import datetime
import pandas as pd


this_month = datetime.datetime.now().month

class HistoryForm(forms.Form):
    stocknm = forms.CharField(
        label="股票代號",
        widget=forms.TextInput(attrs={
        'class': 'stocknm',
        'placeholder': '請輸入股票代號'
        })
    )

    stockmonth1 = forms.CharField(
        label="月份",
        widget=forms.SelectDateWidget(attrs={
            'class': 'stockmonth1',
        })
    )

    stockmonth2 = forms.CharField(
        label="月份",
        widget=forms.SelectDateWidget(attrs={
            'class': 'stockmonth2',
        })
    )
        # stocknm = self.cleaned_data.get('stocknm')
        # if len(stocknm) < 4 or len(stocknm) >5:
        #     raise forms.ValidationError('股票代號錯誤')
        # return stocknm

class NowStock(forms.Form):
    stocknm = forms.CharField(
        label="股票代號",
        widget=forms.TextInput(attrs={
        'class': 'stocknm',
        'placeholder': '2330 1101'
        })
    )

    # def clean_stocknm(self):
    #     stocknm = self.cleaned_data.get('stocknm')
    #     pass

class CustomizeForm(forms.Form):
    stocknm = forms.CharField(
        label="股票代號",
        widget=forms.TextInput(attrs={
        'class': 'stocknm',
        'placeholder': '2330 1101'
        })
    )