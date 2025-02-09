import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

# --- 사용자 설정 ---
# 예시 리밸런싱 날짜 (원하는 날짜로 변경)
rebalance_date_str = "2023-10-02"  
rebalance_date = datetime.strptime(rebalance_date_str, "%Y-%m-%d").date()

# S&P500 종목 리스트 (Wikipedia에서 읽어옴)
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
tables = pd.read_html(url, header=0)
sp500_df = tables[0]
tickers = sp500_df['Symbol'].tolist()

# 결과 저장용 리스트
results = []

# --- 각 종목별 데이터 처리 ---
for ticker in tickers:
    try:
        # 충분한 데이터를 확보하기 위해 (60일 이동평균 + 전일 데이터) 시작일을 넉넉히 잡음
        start_date = rebalance_date - timedelta(days=100)  # buffer 기간
        end_date = rebalance_date + timedelta(days=1)
        
        # yfinance로 데이터 다운로드 (시가, 고가, 저가, 종가 포함)
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if df.empty:
            continue
        
        # 날짜 정보를 datetime.date 형태로 변환
        dates = df.index.date
        
        # 리밸런싱 당일 데이터가 존재하는지 확인
        if rebalance_date not in dates:
            continue
        
        # 리밸런싱 당일 이전의 마지막 거래일 찾기
        previous_dates = [d for d in dates if d < rebalance_date]
        if not previous_dates:
            continue
        prev_date = max(previous_dates)
        
        # 리밸런싱 당일과 전일의 데이터 추출
        prev_data = df[df.index.date == prev_date].iloc[-1]
        rebalance_data = df[df.index.date == rebalance_date].iloc[-1]
        
        # --- 60일 이동평균선 및 기울기 계산 ---
        # 전일 기준까지의 데이터를 사용 (이동평균 계산을 위해 충분한 기간 필요)
        df_before = df[df.index.date <= prev_date].copy()
        if len(df_before) < 60:
            continue  # 데이터 부족 시 skip
        
        # 60일 이동평균선 (종가 기준)
        df_before['60_MA'] = df_before['Close'].rolling(window=60).mean()
        ma_series = df_before['60_MA'].dropna()
        if len(ma_series) < 60:
            continue
        
        # 마지막 60개 값에 대해 선형 회귀로 기울기 계산
        last_60 = ma_series.tail(60)
        x = np.arange(len(last_60))
        y = last_60.values
        slope, _ = np.polyfit(x, y, 1)
        
        # 기울기가 양수인 종목만 선택
        if slope > 0:
            # "전일 종가에 매수, 당일 종가에 매도" 했을 때 수익률 계산
            return_rate = (rebalance_data['Close'] / prev_data['Close']) - 1
            
            results.append({
                'Ticker': ticker,
                'Prev_Date': prev_date,
                'Rebalance_Date': rebalance_date,
                'Prev_Open': prev_data['Open'],
                'Prev_High': prev_data['High'],
                'Prev_Low': prev_data['Low'],
                'Prev_Close': prev_data['Close'],
                'Rebalance_Open': rebalance_data['Open'],
                'Rebalance_High': rebalance_data['High'],
                'Rebalance_Low': rebalance_data['Low'],
                'Rebalance_Close': rebalance_data['Close'],
                '60_MA_Slope': slope,
                'Return': return_rate
            })
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

# --- 결과 출력 ---
result_df = pd.DataFrame(results)
print(result_df)
