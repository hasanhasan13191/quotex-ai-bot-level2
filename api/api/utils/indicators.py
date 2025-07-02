# utils/indicators.py

import pandas as pd

def calculate_indicators(df):
    df['EMA'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
    df['RSI'] = compute_rsi(df['Close'], 14)

    latest = df.iloc[-1]
    ema = latest['EMA']
    rsi = latest['RSI']
    macd = latest['MACD']
    close = latest['Close']

    if ema < close and rsi < 70 and macd > 0:
        return "BUY", 92
    elif ema > close and rsi > 30 and macd < 0:
        return "SELL", 90
    else:
        return "NO SIGNAL", 75

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
