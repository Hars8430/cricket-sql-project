"""
⚔️ Player Comparison Page
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from lib.db import get_players_list, get_player_comparison, is_mysql_available
from lib.sample_data import get_players_list_fallback, get_player_comparison_fallback


st.set_page_config(page_title="Compare Players", page_icon="⚔️", layout="wide")

db_available = is_mysql_available()

st.markdown("# ⚔️ Player Comparison")
st.markdown("*Select two players to see a head-to-head statistical comparison*")

st.markdown("---")

# ─── Player Selection ───────────────────────────────────────
players = get_players_list() if db_available else get_players_list_fallback()
player_names = [p["full_name"] for p in players] if players else []

col1, col2 = st.columns(2)

with col1:
    player1 = st.selectbox(
        "🏏 Player 1",
        options=player_names,
        index=player_names.index("Rohit Sharma") if "Rohit Sharma" in player_names else 0,
    )

with col2:
    default_idx = player_names.index("Virat Kohli") if "Virat Kohli" in player_names else 1
    player2 = st.selectbox(
        "🏏 Player 2",
        options=player_names,
        index=default_idx,
    )

compare_btn = st.button("⚔️ Compare", type="primary", use_container_width=True)

st.markdown("---")

# ─── Comparison Results ─────────────────────────────────────
if compare_btn and player1 != player2:
    comparison = get_player_comparison(player1, player2) if db_available else get_player_comparison_fallback(player1, player2)

    if comparison and len(comparison) == 2:
        p1 = comparison[0]
        p2 = comparison[1]

        # Stats cards
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        metrics = [
            (col1, "Matches", "matches"),
            (col2, "Runs", "runs"),
            (col3, "Avg", "avg_runs"),
            (col4, "SR", "strike_rate"),
            (col5, "4s", "fours"),
            (col6, "6s", "sixes"),
        ]
        for col, label, key in metrics:
            with col:
                v1 = p1.get(key) or 0
                v2 = p2.get(key) or 0
                if isinstance(v1, float):
                    v1 = round(v1, 2)
                if isinstance(v2, float):
                    v2 = round(v2, 2)
                winner = "↑" if v1 > v2 else ("↓" if v1 < v2 else "=")
                st.metric(f"{player1} {winner}", v1, f"{player2}: {v2}")

        st.markdown("---")

        # Visual comparison
        st.markdown("### 📊 Visual Comparison")

        stat_labels = ["Matches", "Runs", "Avg", "Strike Rate", "4s", "6s"]
        p1_vals = [p1.get("matches", 0) or 0, p1.get("runs", 0) or 0,
                   p1.get("avg_runs", 0) or 0, p1.get("strike_rate", 0) or 0,
                   p1.get("fours", 0) or 0, p1.get("sixes", 0) or 0]
        p2_vals = [p2.get("matches", 0) or 0, p2.get("runs", 0) or 0,
                   p2.get("avg_runs", 0) or 0, p2.get("strike_rate", 0) or 0,
                   p2.get("fours", 0) or 0, p2.get("sixes", 0) or 0]

        # Normalize for radar chart
        max_vals = [max(a, b) for a, b in zip(p1_vals, p2_vals)]
        p1_norm = [v / m if m > 0 else 0 for v, m in zip(p1_vals, max_vals)]
        p2_norm = [v / m if m > 0 else 0 for v, m in zip(p2_vals, max_vals)]

        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "bar"}, {"type": "bar"}]],
            subplot_titles=(player1, player2),
        )

        colors = ["#4CAF50", "#4CAF50"]
        for i, (vals, name, color) in enumerate(
            [(p1_vals, player1, "#4CAF50"), (p2_vals, player2, "#2196F3")]
        ):
            fig.add_trace(
                go.Bar(
                    x=stat_labels,
                    y=vals,
                    marker_color=color,
                    text=vals,
                    textposition="outside",
                    showlegend=False,
                ),
                row=1, col=i + 1,
            )

        fig.update_layout(height=400, barmode="group", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # Radar chart
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=p1_norm + [p1_norm[0]],
            theta=stat_labels + [stat_labels[0]],
            fill="toself",
            name=player1,
            line_color="#4CAF50",
            fillcolor="rgba(76,175,80,0.3)",
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=p2_norm + [p2_norm[0]],
            theta=stat_labels + [stat_labels[0]],
            fill="toself",
            name=player2,
            line_color="#2196F3",
            fillcolor="rgba(33,150,243,0.3)",
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=False)),
            showlegend=True,
            height=400,
            title="Normalized Stats (Higher = Better)",
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Data table
        st.markdown("### 📋 Full Comparison Table")
        df_compare = pd.DataFrame([p1, p2])
        st.dataframe(df_compare, use_container_width=True, hide_index=True)

    elif comparison and len(comparison) == 1:
        st.info(f"Only found data for {comparison[0]['full_name']}. "
                 "Try selecting different players.")
    else:
        st.warning("No comparison data found for these players.")

elif compare_btn and player1 == player2:
    st.warning("Please select two different players to compare.")

else:
    # Show suggestions
    st.info("👆 Select two players above and click **Compare** to see their head-to-head stats!")
    st.markdown("""
    #### Suggested Matchups:
    - **Rohit Sharma vs Virat Kohli** — India's batting pillars
    - **MS Dhoni vs Hardik Pandya** — CSK's power hitters
    - **Jasprit Bumrah vs Rashid Khan** — Death over specialists
    - **Andre Russell vs Sunil Narine** — KKR's all-rounders
    """)

st.markdown("---")
st.caption("Data sourced from matches in the cricket database.")
