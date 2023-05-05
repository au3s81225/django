from django.db import models

# Create your models here.


class StockHistory(models.Model):
    # stock_name, stock_num, stock_price, stock_open, stock_highest, stock_lowest, stock_date, turnover
    id = models.AutoField(primary_key=True)
    stock_name = models.CharField(max_length=10)
    stock_num = models.CharField(max_length=10)
    stock_price = models.CharField(max_length=10)
    stock_open = models.CharField(max_length=10)
    stock_highest = models.CharField(max_length=10)
    stock_lowest = models.CharField(max_length=10)
    stock_date = models.CharField(max_length=10)
    turnover = models.CharField(max_length=10)
    class Meta:
        db_table = '2023'
    # def __str__(self):
    #     return f"{self.stock_name} - {self.stock_num} - {self.stock_price}-{self.stock_open}-{self.stock_highest}-{self.stock_lowest}-{self.stock_date}-{self.turnover}"