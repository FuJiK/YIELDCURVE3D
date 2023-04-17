import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_cot_data_for_date(date):
    # レポートのURLを指定
    report_url = f'https://www.cftc.gov/files/dea/history/dea_fut_xls_{date}.xls'

    response = requests.get(report_url)
    
    # ファイルが存在しない場合、Noneを返す
    if response.status_code == 404:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # 天然ガスのデータが含まれる行を見つける
    natural_gas_row = soup.find('tr', string='NATURAL GAS - NEW YORK MERCANTILE EXCHANGE')

    # 天然ガスのデータを取得
    columns = natural_gas_row.find_all('td')
    open_interest = int(columns[1].text.replace(',', ''))
    long_positions = int(columns[2].text.replace(',', ''))
    short_positions = int(columns[3].text.replace(',', ''))

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
