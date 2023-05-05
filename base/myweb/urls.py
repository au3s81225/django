from django.urls import path
from . import views

urlpatterns = [
    path('', views.Base.as_view(), name='home'),
    path('stock/stock_history_form/', views.Stock.as_view(), name = 'stock_history_form.html'),
    path('stock/stock_history/', views.Stock.as_view(), name = 'stock_history'),
    # path('webcrawler/stock/stock_history_form/', views.WebCrawler.stock_history_form, name = 'stock_history_form'),
    # path('webcrawler/stock/stock_history/', views.WebCrawler.stock_history, name = 'stock_history'),
    
]   