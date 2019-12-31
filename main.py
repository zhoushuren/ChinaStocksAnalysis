# -*- coding: utf-8 -*-
from Stock import Stock

def main():
    stock = Stock('20180401', '20190401')
    stock.runBacktest()

if __name__ == '__main__':
    main()