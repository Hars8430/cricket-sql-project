"""
🎯 Bowling Statistics Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from lib.db import get_top_bowlers, get_best_economy, is_mysql_available
from lib.sample_data import get_top_bowlers_fallback, get_best_economy_fallback

st.set_page_config(page_title="Bowling Stats", page_icon="🎯", layout="wide")

db_available = is_mysql_available()

st.markdown("# 🎯 Bowling Statistics")
st.caption("Analyze bowling performance: wickets, economy, and strike rates")

with st.sidebar:
    st.markdown("### 🎛️ Filters")
    limit = st.slider("Show Top N Bowlers", 5, 30, 15)

st.markdown("---")

# ─── Top Wicket Takers ─────────────────────────────────────
st.markdown("### 🏆 Top Wicket Takers")

bowlers = get_top_bowlers(limit) if db_available else get_top_bowlers_fallback(limit)
if bowlers:
    df = pd.DataFrame(bowlers)

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.bar(
            df.head(12),
            x="total_wickets",
            y="full_name",
            orientation="h",
            color="team",
            text_auto=True,
            hover_data=["economy", "bowling_avg", "strike_rate"],
        )
        fig.update_layout(
            height=550,
            yaxis_title="",
            xaxis_title="Wickets",
            showlegend=True,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Quick Stats")
        st.metric("Most Wickets", df.iloc[0]["total_wickets"])
        st.metric("Player", df.iloc[0]["full_name"])
        st.metric("Best Economy", f"{df['economy'].min():.2f}")

    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "total_wickets": st.column_config.NumberColumn("Wickets", format="%d"),
            "economy": st.column_config.NumberColumn("Econ", format="%.2f"),
            "bowling_avg": st.column_config.NumberColumn("Avg", format="%.2f"),
            "strike_rate": st.column_config.NumberColumn("SR", format="%.2f"),
        },
        hide_index=True,
    )
else:
    st.warning("No bowling data available.")

st.markdown("---")

# ─── Best Economy Rates ──────────────────────────────────────
st.markdown("### ⭐ Best Economy Rates (min 4 matches)")

economy = get_best_economy(limit) if db_available else get_best_economy_fallback(limit)
if economy:
    df_econ = pd.DataFrame(economy)

    fig = px.bar(
        df_econ.head(15),
        x="economy",
        y="full_name",
        orientation="h",
        color="economy",
        color_continuous_scale="RdYlGn_r",
        text_auto=".2f",
    )
    fig.update_layout(
        height=550,
        yaxis_title="",
        xaxis_title="Economy Rate (lower is better)",
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        df_econ,
        use_container_width=True,
        column_config={
            "economy": st.column_config.NumberColumn("Economy", format="%.2f"),
            "total_overs": st.column_config.NumberColumn("Overs", format="%.1f"),
        },
        hide_index=True,
    )
else:
    st.warning("No economy data available.")

st.markdown("---")

# ─── Bowling Style Breakdown ─────────────────────────────────
st.markdown("### 📊 Bowling Style Analysis")

st.info("📝 Bowling style breakdown coming soon — add style data to the database to visualize!")

st.markdown("""
| Bowling Style | Description | Notable Players |
|---|---|---|
| Fast | Speed > 140 km/h | Jasprit Bumrah, Mohammed Shami |
| Fast-Medium | Speed 130-140 km/h | Bhuvneshwar Kumar, Deepak Chahar |
| Off-Spin | Right-arm finger spin | Sunil Narine, Moeen Ali |
| Leg-Spin | Right-arm wrist spin | Yuzvendra Chahal, Varun Chakravarthy |
| Left-Arm | Left-arm orthodox | Ravindra Jadeja |
""")
