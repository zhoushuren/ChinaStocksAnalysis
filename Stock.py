# -*- coding: utf-8 -*-
import tushare as ts

class Stock:
    def __init__(self, start_date, end_date):
        ts.set_token('26cb0ed75c90e7a3c23a176146d7b3b0e15673584fb4c525ee3411ac')
        self.pro = ts.pro_api()
        self.stat_date = start_date
        self.end_date = end_date
        self.day = 3
        self.result = []
        self.fw = open("./result.csv", 'w')
        self.fw.write('rate,date,code')
        self.fw.write("\n")
    def getStStockCode(self):
        df = self.pro.namechange(fields='ts_code,name,start_date,end_date,change_reason', start_date='20180401', end_date='20190401')
        stock = []
        for val in df.values.tolist():
            if val[1][0:2] == 'ST' or val[1][0:1] == '*' and val[4] != u'改名':
                stock.append(val[0])
        return stock

    def getAllPrice(self, ts_code):
        df = self.pro.daily(ts_code=ts_code, start_date='20180401', end_date='20190401')
        list = df.values.tolist()
        return list

    def runBacktest(self):
        stCodeList = self.getStStockCode()
        for code in stCodeList:
            price = self.getAllPrice(code)
            self.computs(price)
            # print '---1 stock end---'

    def computs(self, list):
        list = list[::-1]
        tmp = 0
        for key, value in enumerate(list):
            tmp += value[9]
            if key >= self.day - 1:
                avg_vol = tmp / self.day
                if key == len(list) - 1:
                    break
                # print avg_vol
                if list[key+1][9] / avg_vol >= 2:
                    if list[key + 1][2] <= list[key+1][5]:
                        t_close = value[5]
                        t2_close = list[key+1][5]
                        amount = (t2_close / t_close) - 1
                        # print 'rate:' + str(amount) + '---date:' + list[key+1][1] + '---code:' +list[key+1][0]
                        self.fw.write(str(amount) + ',' + list[key+1][1] + ',' + list[key+1][0])
                        self.fw.write("\n")
                tmp -= list[key - (self.day-1)][9]
