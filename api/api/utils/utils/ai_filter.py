# utils/ai_filter.py

def ai_filter_signal(df, signal, confidence):
    latest = df.iloc[-1]
    candle_range = latest['High'] - latest['Low']
    body_size = abs(latest['Close'] - latest['Open'])

    # Avoid Doji / tiny candles
    if body_size < 0.1 * candle_range:
        return "NO SIGNAL"

    # Avoid low confidence
    if confidence < 85:
        return "NO SIGNAL"

    return signal
