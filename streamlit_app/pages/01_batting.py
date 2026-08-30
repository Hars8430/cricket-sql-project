"""
🏏 Batting Statistics Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from lib.db import (
    get_top_scorers,
    get_best_strike_rates,
    get_boundary_hitters,
    get_players_list,
    get_player_comparison,
    is_mysql_available,
)
from lib.sample_data import (
    get_top_scorers_fallback,
    get_best_strike_rates_fallback,
    get_players_list_fallback,
    get_boundary_hitters_fallback,
)

st.set_page_config(page_title="Batting Stats", page_icon="🏏", layout="wide")

db_available = is_mysql_available()

st.markdown("# 🏏 Batting Statistics")
st.caption("Deep dive into batting performance across IPL and International cricket")

# Sidebar filters
with st.sidebar:
    st.markdown("### 🎛️ Filters")
    limit = st.slider("Show Top N Players", 5, 30, 15)

st.markdown("---")

# ─── Top Run Scorers ──────────────────────────────────────────
st.markdown("### 📊 Top Run Scorers")

top_batsmen = get_top_scorers(limit) if db_available else get_top_scorers_fallback(limit)
if top_batsmen:
    df = pd.DataFrame(top_batsmen)

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.bar(
            df.head(10),
            x="total_runs",
            y="full_name",
            orientation="h",
            color="team",
            text_auto=True,
            hover_data=["avg_runs", "strike_rate", "fours", "sixes"],
            category_orders={"full_name": df.head(10)["full_name"].tolist()[::-1]},
        )
        fig.update_layout(
            height=500,
            yaxis_title="",
            xaxis_title="Total Runs",
            showlegend=True,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Quick Stats")
        st.metric("Most Runs", df.iloc[0]["total_runs"], delta=None)
        st.metric("Player", df.iloc[0]["full_name"])
        st.metric("Avg SR", f"{df['strike_rate'].mean():.2f}")
        st.metric("Total 6s", int(df["sixes"].sum()))

    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "total_runs": st.column_config.NumberColumn("Runs", format="%d"),
            "avg_runs": st.column_config.NumberColumn("Avg", format="%.2f"),
            "strike_rate": st.column_config.NumberColumn("SR", format="%.2f"),
        },
        hide_index=True,
    )
else:
    st.warning("No batting data available.")

st.markdown("---")

# ─── Best Strike Rates ────────────────────────────────────────
st.markdown("### ⚡ Best Strike Rates (min 50 balls)")

best_sr = get_best_strike_rates(limit) if db_available else get_best_strike_rates_fallback(limit)
if best_sr:
    df_sr = pd.DataFrame(best_sr)

    fig = px.bar(
        df_sr.head(15),
        x="strike_rate",
        y="full_name",
        orientation="h",
        color="strike_rate",
        color_continuous_scale="Greens",
        text_auto=".2f",
        category_orders={"full_name": df_sr.head(15)["full_name"].tolist()[::-1]},
    )
    fig.update_layout(
        height=500,
        yaxis_title="",
        xaxis_title="Strike Rate",
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        df_sr,
        use_container_width=True,
        column_config={
            "total_runs": st.column_config.NumberColumn("Runs", format="%d"),
            "strike_rate": st.column_config.NumberColumn("SR", format="%.2f"),
        },
        hide_index=True,
    )
else:
    st.warning("No strike rate data available.")

st.markdown("---")

# ─── Boundary Hitters ──────────────────────────────────────────
st.markdown("### 🚀 Boundary Hitters (4s + 6s)")

boundaries = get_boundary_hitters(limit) if db_available else get_boundary_hitters_fallback(limit)
if boundaries:
    df_bd = pd.DataFrame(boundaries)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Most Fours")
        top_fours = df_bd.nlargest(10, "fours")
        fig = px.bar(
            top_fours,
            x="fours",
            y="full_name",
            orientation="h",
            color="fours",
            color_continuous_scale="Blues",
            text_auto=True,
            category_orders={"full_name": top_fours["full_name"].tolist()[::-1]},
        )
        fig.update_layout(height=400, yaxis_title="", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Most Sixes")
        top_sixes = df_bd.nlargest(10, "sixes")
        fig = px.bar(
            top_sixes,
            x="sixes",
            y="full_name",
            orientation="h",
            color="sixes",
            color_continuous_scale="Reds",
            text_auto=True,
            category_orders={"full_name": top_sixes["full_name"].tolist()[::-1]},
        )
        fig.update_layout(height=400, yaxis_title="", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        df_bd,
        use_container_width=True,
        hide_index=True,
    )
