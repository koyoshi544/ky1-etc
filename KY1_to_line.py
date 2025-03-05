import os
import json
import io
import csv
import boto3
import datetime
import urllib.request
_env = os.environ

def lambda_handler(event, context):
    bucket_name = _env["S3BUCKT"]
    file_name = _env["CSVFILE"]
    
    # 今日の日付を求める
    now = datetime.datetime.now()
    now_date = now.strftime("%Y/%m/%d")
    # now_date = "2020/12/29"
    # print(now_date)
    
    # S3上のCSVファイルを読み込み
    # 
    reader = csv.DictReader(get_s3file(bucket_name, file_name))
    
    # 1行ごとに処理
    for row in reader:
        yosoku_date = row["入庫予測日"]
        if now_date == yosoku_date[0:10]:
            if row["単位"] == "やること":
                line_mess = "\r\nもうすぐ " + row["名称"] + "のタイミングです。"
            else:
                line_mess = "\r\nそろそろ " + row["名称"] + "を買うタイミングです。"
            sendNoticeToLine(line_mess)
            # print(line_mess)

# LINEに出力 1
def sendNoticeToLine(line_mess):
    _url = 'https://notify-api.line.me/api/notify'
    _data = {
      "message": line_mess
    }
    _header = {
      "Authorization": "Bearer " + _env["LINE_ACCESS_TOKEN"]
    }

    # print(_data)
    sendRequest(_url, _data, _header)

# LINEに出力 2
def sendRequest(_url, _data, _header):
    _data = urllib.parse.urlencode(_data).encode("utf-8")
    _req = urllib.request.Request(_url, _data, _header, "POST")
    try:
        with urllib.request.urlopen(_req) as _res:
            _body = _res.read()
            print(_body)
    except urllib.error.HTTPError as _err:
        print("HTTPError: " + str(_err.code))
        print(_err)
    except urllib.error.URLError as _err:
        print("HTTPError: " + _err.reason)
        print(_err)

#S3から読み込み
def get_s3file(bucket_name, key):
    s3 = boto3.resource('s3')
    s3obj = s3.Object(bucket_name, key).get()
    return io.TextIOWrapper(io.BytesIO(s3obj['Body'].read()))
