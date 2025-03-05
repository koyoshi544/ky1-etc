# 買い物予報 Ver 1.05  2024/03/07
#
# KY1_yosoku.py
#   入庫予定日を算出し、更新データを更新する。
#

import os
import datetime
import pandas as pd

_env = os.environ

def main():
    # 物品マスタを読み込む
    csv1_name = _env['KY1_BUPPIN']
    csv1_input = pd.read_csv(filepath_or_buffer=csv1_name, encoding='utf-8', sep=',')

    # 入庫データを読み込む
    csv2_name = _env['KY1_NYUKO']
    csv2_input = pd.read_csv(filepath_or_buffer=csv2_name, encoding='utf-8', sep=',')

    # 入庫日をdatetime64[ns]型に変換
    csv2_input['入庫日'] = pd.to_datetime(csv2_input['入庫日'], format='%Y/%m/%d')

    # 物品マスタを1行ごとに処理
    for index, row in csv1_input.iterrows():
        # 入庫データを物品IDで抽出
        ext_id = row['物品ID']
        ext_input = csv2_input.query('物品ID == @ext_id')
        print(ext_id)

        # 抽出入庫データがある場合のみ
        if ext_input.empty == False:

            # 入庫日の最小値を求める
            first_date = ext_input['入庫日'].min()
            print('first_date : ',first_date)

            # 入庫日の最大値を求める
            last_date = ext_input['入庫日'].max()
            print('last_date : ',last_date)

            # 最終入庫数を求める
            last_value = ext_input[ext_input['入庫日'] == last_date]['入庫数'].iat[0]
            print('last_value : ',last_value)

            # 入庫数の合計を求める
            total_value = ext_input['入庫数'].sum()
            print('total_value : ',total_value)

            # 在庫期間を求める（最大入庫日-最小入庫日）
            term_day = (last_date - first_date).days
            if term_day == 0:
                term_day = 1
            print('term_day : ',term_day)

            # 1日の使用量を求める（(合計入庫数-最終入庫数)/在庫期間）
            day_use = (total_value - last_value) / term_day
            print('day_use : ',day_use)

            # 平均入庫間隔を求める（入庫数の平均/在庫期間）
            if first_date == last_date:
                interval_day = 0
            else:
                interval_day = int((ext_input['入庫数'].mean()) / day_use)
            print('interval_day : ',interval_day)

            # 次回入庫予測日を求める（最終入庫日+(最終入庫数/1日使用量)
            if first_date == last_date:
                yosoku_date = last_date
            else:
                yosoku_date = last_date + datetime.timedelta(days=(last_value / day_use))
            print('yosoku_date : ',yosoku_date)

            # 物品マスタの入庫予測日と平均入庫間隔を更新
            csv1_input.at[index,'入庫予測日'] = yosoku_date.strftime("%Y/%m/%d")
            csv1_input.at[index,'平均入庫間隔'] = interval_day

        print('==========')

    # 物品マスタを更新データとして書き出す
    csv3_name = _env['KY1_KOSIN']
    csv1_input.to_csv(csv3_name, encoding='utf-8', sep=',', index=False)

if __name__ == '__main__':
    main()

