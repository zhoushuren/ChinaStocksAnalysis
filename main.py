# -*- coding: utf-8 -*-
import tushare as ts
import json
ts.set_token('26cb0ed75c90e7a3c23a176146d7b3b0e15673584fb4c525ee3411ac')

pro = ts.pro_api()

df = pro.namechange(fields='ts_code,name,start_date,end_date,change_reason', start_date='20180401', end_date='20190401')

day = 3 # 前几天的平均值
def main():
    for val in df.values.tolist():
        if val[1][0:2] == 'ST' or val[1][0:1] == '*' and val[4] != '改名':
            getAllPrice(val[0])


# print(df.values.tolist())
def getAllPrice(ts_code):
    df = pro.daily(ts_code=ts_code, start_date='20180401', end_date='20190401')
    list = df.values.tolist()
    getAvgVs6Day(list)

def getAvgVs6Day(list):
    list = list[: :-1]
    # print(list)
    # exit()
    i = 0
    for v in list:
        if i > len(list) - day:
            break
        sub_list = list[i: day+1+i]
        if len(sub_list) < 4:
            break

        total = 0
        for v2 in range(0, len(sub_list) -1):
            total += float(sub_list[v2][9])
        avg_vol = total / day
        if sub_list[-1][9] / avg_vol >= 2:
            # print(sub_list[-1])
            d = sub_list[-1]
            if d[2] >= d[5]:
                # print d



            # print('avg_vol:'+ str(avg_vol))
            # print('last_3day_total:'+ str(total))
            # print(sub_list)
        i += 1

if __name__ == '__main__':
    # main()
    getAllPrice('600321.SH')