# api/signal.py

import yfinance as yf
from datetime import datetime
import json
import os
from utils.indicators import calculate_indicators
from utils.ai_filter import ai_filter_signal

def handler(request):
    symbol = "EURUSD=X"
    df = yf.download(tickers=symbol, period="2d", interval="1m")
    signal, confidence = calculate_indicators(df)

    filtered_signal = ai_filter_signal(df, signal, confidence)

    now = datetime.now().strftime("%H:%M")
    
    # Save to history
    log = {
        "time": now,
        "signal": filtered_signal,
        "confidence": confidence
    }

    history_path = os.path.join("data", "history.json")
    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(log)
    with open(history_path, "w") as f:
        json.dump(history[-100:], f, indent=2)  # keep last 100

    return {
        "time": now,
        "signal": filtered_signal,
        "confidence": confidence
    }
