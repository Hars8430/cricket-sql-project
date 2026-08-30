"""
👤 Player Profiles Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from lib.db import get_players_list, get_player_detail, is_mysql_available
from lib.sample_data import get_players_list_fallback, get_player_detail_fallback


st.set_page_config(page_title="Player Profiles", page_icon="👤", layout="wide")

db_available = is_mysql_available()

st.markdown("# 👤 Player Profiles")
st.markdown("*Search for any player to see their complete statistics and recent match performance*")

st.markdown("---")

# ─── Player Search ─────────────────────────────────────────
players = get_players_list() if db_available else get_players_list_fallback()
player_names = [p["full_name"] for p in players] if players else []

selected_player = st.selectbox(
    "🔍 Search for a player",
    options=player_names,
    index=0 if player_names else None,
)

if selected_player:
    data = get_player_detail(selected_player) if db_available else get_player_detail_fallback(selected_player)

    if data and data["player"]:
        p = data["player"]
        batting = data["batting"]
        bowling = data["bowling"]
        recent = data["recent"]

        # ─── Player Header ────────────────────────────────────
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(f"### {p['full_name']}")
            st.caption(f"{p['country']} • {p['role'].replace('-', ' ').title()}")
            if p.get("team_name"):
                st.markdown(f"**Team:** {p['team_name']}")

        with col2:
            if batting:
                st.metric("🏏 Total Runs", f"{batting.get('total_runs', 0):,}")
        with col3:
            if batting:
                st.metric("📊 Avg Runs", f"{batting.get('avg_runs', 0):.2f}")
        with col4:
            if batting:
                st.metric("⚡ Strike Rate", f"{batting.get('strike_rate', 0):.2f}")
        with col5:
            if bowling and int(bowling.get("total_wickets", 0)) > 0:
                st.metric("🎯 Wickets", bowling.get("total_wickets", 0))

        st.markdown("---")

        # ─── Detailed Stats ───────────────────────────────────
        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown("#### 🏏 Batting Statistics")
            if batting:
                bat_cols = st.columns(3)
                stats = [
                    ("Matches Batted", batting.get("matches", 0)),
                    ("Total Runs", f"{batting.get('total_runs', 0):,}"),
                    ("Highest Score", batting.get("highest", 0)),
                    ("Average", f"{batting.get('avg_runs', 0):.2f}"),
                    ("Strike Rate", f"{batting.get('strike_rate', 0):.2f}"),
                    ("4s", batting.get("fours", 0)),
                    ("6s", batting.get("sixes", 0)),
                    ("100s", batting.get("centuries", 0)),
                    ("50s", batting.get("fifties", 0)),
                ]
                for i, (label, val) in enumerate(stats):
                    with bat_cols[i % 3]:
                        st.metric(label, val)
            else:
                st.info("No batting data for this player.")

        with col_right:
            st.markdown("#### 🎯 Bowling Statistics")
            if bowling and int(bowling.get("total_wickets", 0)) > 0:
                bowl_cols = st.columns(3)
                bstats = [
                    ("Matches Bowled", bowling.get("matches", 0)),
                    ("Total Wickets", bowling.get("total_wickets", 0)),
                    ("Economy", f"{bowling.get('economy', 0):.2f}"),
                    ("Bowling Avg", f"{bowling.get('bowling_avg', 0):.2f}"),
                    ("Overs Bowled", bowling.get("total_overs", 0)),
                ]
                for i, (label, val) in enumerate(bstats):
                    with bowl_cols[i % 3]:
                        st.metric(label, val)
            else:
                st.info("No bowling data for this player.")

        st.markdown("---")

        # ─── Player Info ───────────────────────────────────────
        with st.expander("📋 Player Details"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Role:** {p['role'].replace('-', ' ').title()}")
            with col2:
                st.write(f"**Batting:** {p.get('batting_style', 'N/A')}")
            with col3:
                st.write(f"**Bowling:** {p.get('bowling_style', 'N/A')}")

        # ─── Recent Matches ────────────────────────────────────
        if recent:
            st.markdown("#### 🏏 Recent Match Performance")
            df_recent = pd.DataFrame(recent)
            df_recent["runs"] = df_recent["runs"].apply(lambda x: f"⭐ {x}" if x and int(x) >= 50 else str(x))
            st.dataframe(
                df_recent[["match_date", "venue", "match_type", "runs", "balls", "fours", "sixes", "strike_rate", "dismissal"]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No recent match data for this player.")
    else:
        st.warning(f"Player '{selected_player}' not found in the database.")
else:
    st.info("👆 Select a player from the dropdown above to view their profile.")

st.markdown("---")
st.caption("Profiles include batting and bowling statistics from all matches in the database.")
