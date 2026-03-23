from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from weather_logic import (
    STATES,
    TRANSITION_MATRIX,
    daily_probabilities,
    monte_carlo_summary,
    simulate_chain,
    steady_state_distribution,
)

ASSET_DIR = Path(__file__).parent / "assets"
ICON_MAP = {
    "Sunny": ASSET_DIR / "sunny.svg",
    "Cloudy": ASSET_DIR / "cloudy.svg",
    "Rain": ASSET_DIR / "rain.svg",
}

st.set_page_config(page_title="Markov Chain Weather Forecast", page_icon="🌦️", layout="wide")


def load_svg(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def percent(value: float) -> str:
    return f"{value:.1f}%"


def hero_card(state: str) -> str:
    svg = load_svg(ICON_MAP[state])
    return f"""
    <div style="
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.05);
        height: 100%;
    ">
        <div style="height:120px; display:flex; align-items:center; justify-content:center; margin-bottom:8px;">{svg}</div>
        <div style="font-size: 1.05rem; font-weight: 700;">{state}</div>
    </div>
    """


st.title("🌦️ Markov Chain Weather Forecast Website")
st.caption(
    "A local website for presenting your Markov chain project with weather icons, simulation outputs, and probability-based forecasts."
)

with st.container():
    c1, c2, c3 = st.columns(3)
    for col, state in zip((c1, c2, c3), STATES):
        with col:
            st.markdown(hero_card(state), unsafe_allow_html=True)

with st.sidebar:
    st.header("Forecast Controls")
    start_state = st.selectbox("Starting weather", STATES, index=0)
    days = st.slider("Forecast length (days)", min_value=3, max_value=30, value=10)
    simulations = st.slider("Monte Carlo simulations", min_value=100, max_value=10000, value=3000, step=100)
    run_forecast = st.button("Run forecast", use_container_width=True)

st.subheader("How the model works")
st.write(
    "This project uses a Markov chain, which means tomorrow's weather depends only on today's weather. "
    "The matrix below stores the transition probabilities from one weather state to the next."
)

matrix_df = pd.DataFrame(TRANSITION_MATRIX, index=STATES, columns=STATES)
st.dataframe(matrix_df.style.format("{:.2f}"), use_container_width=True)

if run_forecast:
    chain = simulate_chain(start_state, days)
    daily_probs = daily_probabilities(start_state, days)
    summary = monte_carlo_summary(start_state, days, simulations)
    steady = steady_state_distribution()

    daily_table = pd.DataFrame(daily_probs, columns=STATES)
    daily_table.insert(0, "Day", list(range(1, days + 1)))
    daily_table.insert(1, "Most Likely Weather", daily_table[STATES].idxmax(axis=1))

    st.subheader("Sample simulated forecast")
    sample_cols = st.columns(len(chain))
    for idx, weather in enumerate(chain):
        with sample_cols[idx]:
            st.image(str(ICON_MAP[weather]), width=70)
            st.markdown(f"**Day {idx + 1}**")
            st.write(weather)

    st.subheader("Prediction forecast with percentages")
    last_day = daily_table.iloc[-1]
    m1, m2, m3 = st.columns(3)
    for col, state in zip((m1, m2, m3), STATES):
        with col:
            st.metric(label=f"Day {days} chance of {state}", value=percent(last_day[state] * 100))

    st.write("**Daily probability table**")
    st.dataframe(
        daily_table.style.format({state: "{:.1%}" for state in STATES}),
        use_container_width=True,
    )

    st.subheader("Monte Carlo results")
    mc1, mc2, mc3 = st.columns(3)
    for col, state in zip((mc1, mc2, mc3), STATES):
        with col:
            st.metric(
                label=f"Ending on {state}",
                value=percent(summary["end_state_percents"][state]),
                help=f"Percent of {simulations:,} simulations that ended in {state} on Day {days}.",
            )

    bar_df = pd.DataFrame(
        {
            "Weather": STATES,
            "End of Forecast %": [summary["end_state_percents"][state] for state in STATES],
            "Long-Run %": [summary["long_run_percents"][state] for state in STATES],
            "Steady State %": [value * 100 for value in steady],
        }
    )

    st.write("**Simulation summary table**")
    st.dataframe(
        bar_df.style.format({
            "End of Forecast %": "{:.1f}%",
            "Long-Run %": "{:.1f}%",
            "Steady State %": "{:.1f}%",
        }),
        use_container_width=True,
    )

    fig1, ax1 = plt.subplots(figsize=(8, 4.5))
    ax1.plot(daily_table["Day"], daily_table["Sunny"] * 100, marker="o", label="Sunny")
    ax1.plot(daily_table["Day"], daily_table["Cloudy"] * 100, marker="o", label="Cloudy")
    ax1.plot(daily_table["Day"], daily_table["Rain"] * 100, marker="o", label="Rain")
    ax1.set_xlabel("Day")
    ax1.set_ylabel("Probability (%)")
    ax1.set_title("Forecast probabilities by day")
    ax1.legend()
    ax1.grid(alpha=0.25)
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(7, 4.5))
    ax2.bar(bar_df["Weather"], bar_df["End of Forecast %"])
    ax2.set_ylabel("Percent")
    ax2.set_title("Probability of each ending weather")
    st.pyplot(fig2)

    st.subheader("Presentation-ready explanation")
    dominant_state = bar_df.loc[bar_df["End of Forecast %"].idxmax(), "Weather"]
    st.info(
        f"Starting from **{start_state}**, the model's most likely weather by Day {days} is **{dominant_state}**. "
        f"Across **{simulations:,} simulations**, the ending-day probabilities and long-run percentages begin to settle toward a stable pattern, "
        "which is the core idea behind a Markov chain steady state."
    )
else:
    st.info("Use the controls in the left sidebar and click **Run forecast** to generate the website demo.")
