import os
import pandas as pd

_env = os.environ

def main():  
    csv_name1 = _env["KY1_NYUKO"]
    csv_input = pd.read_csv(filepath_or_buffer=csv_name1, encoding="ms932", sep=",")

    # 日付変換
    csv_input["入庫日"] = pd.to_datetime(csv_input["入庫日"], format='%Y/%m/%d')

    # 物品IDで抽出
    print(csv_input[csv_input["物品ID"] == "A025"])

    # Data Type
    print(csv_input.dtypes)

    # 物品IDでグループ化して入庫数の合計値を求める
    print(csv_input.groupby("物品ID")["入庫数"].sum())

    # 物品IDでグループ化して入庫日の最大値を求める
    print(csv_input.groupby("物品ID")["入庫日"].max())

if __name__ == '__main__':  
    main()
