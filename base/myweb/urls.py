from django.urls import path
from . import views

urlpatterns = [
    path('', views.Base.as_view(), name='home'),
    path('stock/stock_history_form/', views.StockHistoryForm.as_view(), name = 'stock_history_form'),
    path('stock/stock_history/', views.StockHistoryForm.as_view(), name = 'stock_history'),
    path('stock/nowstock_form/', views.NowStockForm.as_view(), name='nowstock_form'),
    path('stock/nowstock/', views.NowStockForm.as_view(), name='nowstock'),
    path('stock/customize/', views.StockCustomize.as_view(), name='customize'),

    
]   