import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from swing import find_swings
from backtest import run_backtest

st.set_page_config(page_title="Forex Scanner & Backtester", layout="wide")

st.title("📊 Forex Scanner & Backtester")
st.markdown("Dieses Tool scannt Währungspaare mit Fibonacci-Levels und testet sie historisch.")

# Seitenmenü
menu = st.sidebar.radio("Navigation", ["Scanner", "Backtest"])

# Scanner
if menu == "Scanner":
    st.header("🔎 Markt Scanner")
    pairs = st.multiselect(
        "Wähle Währungspaare",
        ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X", "USDCHF=X"],
        default=["EURUSD=X", "GBPUSD=X"]
    )

    if st.button("Scannen starten"):
        results = []
        for pair in pairs:
            data = yf.download(pair, period="60d", interval="1h")
            if data.empty:
                continue
            swings = find_swings(data["Close"])
            if not swings:
                continue
            last_swing = swings[-1]

            direction = "BUY" if last_swing["type"] == "low" else "SELL"
            entry = last_swing["price"]
            sl = entry * (0.99 if direction == "BUY" else 1.01)
            tp = entry * (1.02 if direction == "BUY" else 0.98)

            results.append({
                "Pair": pair,
                "Signal": direction,
                "Entry": round(entry, 5),
                "Stop Loss": round(sl, 5),
                "Take Profit": round(tp, 5)
            })

        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)
        else:
            st.warning("Keine Signale gefunden.")

# Backtester
if menu == "Backtest":
    st.header("⏳ Backtest")
    pair = st.selectbox("Währungspaar", ["EURUSD=X", "GBPUSD=X", "USDJPY=X"])
    start_capital = st.number_input("Startkapital (€)", 1000)
    risk_per_trade = st.slider("Risiko pro Trade (%)", 0.5, 5.0, 1.0)

    if st.button("Backtest starten"):
        data = yf.download(pair, period="1y", interval="1h")
        if data.empty:
            st.error("Keine Daten gefunden.")
        else:
            result = run_backtest(data, start_capital, risk_per_trade)
            st.subheader("Ergebnisse")
            st.write(f"Endkapital: {result['end_capital']:.2f} €")
            st.write(f"Anzahl Trades: {result['trades']}")
            st.write(f"Trefferquote: {result['winrate']:.1f}%")

            # Equity-Kurve plotten
            fig, ax = plt.subplots()
            ax.plot(result["equity_curve"])
            ax.set_title("Equity-Kurve")
            st.pyplot(fig)
