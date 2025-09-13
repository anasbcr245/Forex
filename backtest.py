import numpy as np

def run_backtest(data, capital, risk_percent):
    prices = data["Close"].values
    equity = [capital]
    trades = 0
    wins = 0

    for i in range(20, len(prices)-1, 10):
        entry = prices[i]
        direction = np.random.choice(["BUY", "SELL"])
        sl = entry * (0.99 if direction == "BUY" else 1.01)
        tp = entry * (1.02 if direction == "BUY" else 0.98)

        risk_amount = capital * (risk_percent / 100)
        reward = risk_amount * 2  # 2R Ziel
        trades += 1

        # Simpler Zufall: 50% Treffer
        if np.random.rand() > 0.5:
            capital += reward
            wins += 1
        else:
            capital -= risk_amount
        equity.append(capital)

    return {
        "end_capital": capital,
        "trades": trades,
        "winrate": (wins / trades * 100) if trades else 0,
        "equity_curve": equity
    }
