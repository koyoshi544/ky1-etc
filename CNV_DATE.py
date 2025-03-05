import os
import datetime
import pandas as pd

_env = os.environ

def main():  
    csv1_name = './TestData01.csv'
    csv1_input = pd.read_csv(filepath_or_buffer=csv1_name, encoding='utf-8', sep=',')
    print(csv1_input)

    # 1行ずつ処理
    for index, row in csv1_input.iterrows():

        # 日付変換
        ext_date = row['日付']
        print(type(ext_date),ext_date)
        after_date = CNV_DATE(row['日付'])
        if after_date.year == 1:
            print('日付エラー！！')
        else:
            print(type(after_date),after_date)

# 日付っぽい文字列を日付に変換する（和暦非対応）
# 
def CNV_DATE(str_date):
    s_format = ['%Y/%m/%d','%Y.%m.%d','%Y年%m月%d日','%Y-%m-%d',
        '%y/%m/%d','%y.%m.%d','%y年%m月%d日','%y-%m-%d',
        '%m/%d','%m.%d','%m月%d日','%m-%d']
    rtn_date = datetime.datetime(1, 1, 1)
    for fm in s_format:
        try:
            rtn_date = datetime.datetime.strptime(str_date, fm)
            break
        except ValueError:
            continue
    # 年が1900だったら、今年の年で補完する（年が省略された場合の対応）
    if rtn_date.year == 1900:
        rtn_date = rtn_date.replace(year = datetime.datetime.now().year)
    # 入力日付が「今日」だったら、今日の日付で補完する（特別対応）
    if str_date == '今日':
        rtn_date = datetime.date.today()
    # 入力日付が「昨日」だったら、昨日の日付で補完する（特別対応）
    if str_date == '昨日':
        rtn_date = datetime.date.today()
        rtn_date = rtn_date - datetime.timedelta(days=1)
    return rtn_date

if __name__ == '__main__':  
    main()
