import requests
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_cot_data_for_date(date):
    # レポートのURLを指定
    report_url = f'https://www.cftc.gov/files/dea/history/dea_fut_xls_{date}.xls'

    response = requests.get(report_url)

    # ファイルが存在しない場合、Noneを返す
    if response.status_code != 200:
        return None

    # CFTCのファイルはExcel形式なので、BeautifulSoupではなくpandasで読み込む
    df = pd.read_excel(BytesIO(response.content), header=None)

    # 対象行を検索
    row = df[df.iloc[:, 0] == 'NATURAL GAS - NEW YORK MERCANTILE EXCHANGE']
    if row.empty:
        return None

    open_interest = int(row.iloc[0, 1])
    long_positions = int(row.iloc[0, 2])
    short_positions = int(row.iloc[0, 3])

    return open_interest, long_positions, short_positions

# 過去一年分の日付リストを作成
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
date_list = pd.date_range(start=start_date, end=end_date, freq='W-FRI')

# データを取得し、データフレームに格納
data = []
for date in date_list:
    cot_data = get_cot_data_for_date(date.strftime('%Y%m%d'))
    if cot_data is not None:
        data.append([date, *cot_data])

cot_df = pd.DataFrame(data, columns=['Date', 'Open Interest', 'Long Positions', 'Short Positions'])

# データをプロット
plt.figure(figsize=(12, 6))
plt.plot(cot_df['Date'], cot_df['Open Interest'], label='Open Interest')
plt.plot(cot_df['Date'], cot_df['Long Positions'], label='Long Positions')
plt.plot(cot_df['Date'], cot_df['Short Positions'], label='Short Positions')

plt.xlabel('Date')
plt.ylabel('Positions')
plt.title('COT Report - Natural Gas Futures')
plt.legend()
plt.grid()
plt.show()
