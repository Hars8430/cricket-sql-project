"""
🏏 Cricket Stats Dashboard
A comprehensive cricket analytics dashboard built with Streamlit + MySQL.
Covers IPL and International cricket data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from lib.db import (
    get_summary_stats,
    get_top_scorers,
    get_top_bowlers,
    get_team_wins,
    get_match_types,
    get_boundary_hitters,
    get_all_rounders,
    get_best_strike_rates,
    get_best_economy,
    get_venue_stats,
    get_connection,
    is_mysql_available,
)
from lib.sample_data import (
    get_summary_fallback,
    get_top_scorers_fallback,
    get_top_bowlers_fallback,
    get_team_wins_fallback,
    get_match_types_fallback,
    get_allrounders_fallback,
    get_best_economy_fallback,
    get_venue_stats_fallback,
    get_best_strike_rates_fallback,
)

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="🏏 Cricket Stats Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main accent color */
    :root {
        --cricket-green: #1B5E20;
        --cricket-light: #4CAF50;
        --cricket-bg: #F1F8E9;
    }

    /* Big stat cards */
    .stat-card {
        background: linear-gradient(135deg, #1B5E20, #4CAF50);
        color: white;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin: 8px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .stat-card h1 { font-size: 2.8rem; margin: 0; font-weight: 700; }
    .stat-card p { margin: 4px 0 0; opacity: 0.9; font-size: 0.95rem; }

    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1B5E20;
        border-bottom: 3px solid #4CAF50;
        padding-bottom: 6px;
        margin-bottom: 16px;
    }

    /* Table styling */
    .dataframe { border: none !important; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F1F8E9 0%, #ffffff 100%);
    }

    /* Remove padding from main content */
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏏 **Cricket Stats**")
    st.markdown("---")

    # Connection status
    db_available = is_mysql_available()
    if db_available:
        st.success("✅ Database Connected")
    else:
        st.warning("⚡ Demo Mode (Sample Data)")
        st.caption("Connect MySQL for live data")
    st.markdown("---")

    st.markdown("### 📊 Quick Stats")
    stats = get_summary_stats() if db_available else get_summary_fallback()
    if stats:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Teams", stats.get("teams", 0))
            st.metric("Matches", stats.get("matches", 0))
        with col2:
            st.metric("Players", stats.get("players", 0))
            st.metric("Runs", f"{stats.get('total_runs', 0):,}")

    st.markdown("---")
    st.markdown("### 🗂️ Navigation")
    st.page_link("app.py", label="📊 Dashboard Home", icon="📊")
    st.page_link("pages/01_batting.py", label="🏏 Batting Stats", icon="🏏")
    st.page_link("pages/02_bowling.py", label="🎯 Bowling Stats", icon="🎯")
    st.page_link("pages/03_teams.py", label="🏆 Teams & Standings", icon="🏆")
    st.page_link("pages/04_compare.py", label="⚔️ Compare Players", icon="⚔️")
    st.page_link("pages/05_players.py", label="👤 Player Profiles", icon="👤")

    st.markdown("---")
    st.markdown("*Data: IPL 2008–2024 + International Cricket*")

# ─── Title ─────────────────────────────────────────────────────
st.markdown("# 🏏 Cricket Stats Dashboard")
st.markdown("*Comprehensive cricket analytics powered by MySQL*")

# ─── Stats Row ─────────────────────────────────────────────────
if stats:
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("🏟️ Teams", stats.get("teams", 0), help="IPL + International teams")
    with col2:
        st.metric("👤 Players", stats.get("players", 0), help="All players in database")
    with col3:
        st.metric("🏏 Matches", stats.get("matches", 0), help="Total matches")
    with col4:
        st.metric("📈 Runs", f"{stats.get('total_runs', 0):,}", help="Total runs scored")
    with col5:
        st.metric("🎯 Wickets", f"{stats.get('total_wickets', 0):,}", help="Total wickets taken")
    with col6:
        st.metric("🏅 Series", stats.get("series", 0), help="Tournaments covered")

st.markdown("---")

# ─── Main Dashboard Content ─────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🏏 Top Batsmen",
    "🎯 Top Bowlers",
    "⚔️ All-Rounders",
])

# ── Tab 1: Overview ──────────────────────────────────────────
with tab1:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="section-header">🏏 Runs by Match Type</div>', unsafe_allow_html=True)
        match_types = get_match_types() if db_available else get_match_types_fallback()
        if match_types:
            df_types = pd.DataFrame(match_types)
            fig = px.bar(
                df_types,
                x="match_type",
                y="total_runs",
                color="match_type",
                text_auto=True,
                color_discrete_map={"T20": "#4CAF50", "ODI": "#2196F3", "TEST": "#FF9800"},
            )
            fig.update_layout(
                showlegend=False,
                xaxis_title="Match Type",
                yaxis_title="Total Runs",
                height=320,
                margin=dict(t=20, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-header">📍 Top Venues</div>', unsafe_allow_html=True)
        venues = get_venue_stats() if db_available else get_venue_stats_fallback()
        if venues:
            df_venues = pd.DataFrame(venues).head(8)
            fig = px.bar(
                df_venues,
                x="matches_here",
                y="venue",
                orientation="h",
                text_auto=True,
                color="matches_here",
                color_continuous_scale="Greens",
            )
            fig.update_layout(
                showlegend=False,
                xaxis_title="Matches Played",
                yaxis_title="",
                height=320,
                margin=dict(t=20, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)

    # Team wins pie chart
    st.markdown('<div class="section-header">🏆 Team Win Records (IPL)</div>', unsafe_allow_html=True)
    team_data = get_team_wins() if db_available else get_team_wins_fallback()
    if team_data:
        df_teams = pd.DataFrame(team_data).head(10)
        fig = px.pie(
            df_teams,
            names="short_name",
            values="wins",
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Greens,
        )
        fig.update_traces(textposition="outside", textinfo="label+value")
        fig.update_layout(height=320, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 2: Top Batsmen ────────────────────────────────────────
with tab2:
    st.markdown("### 🏏 Top Run Scorers")
    batsmen = get_top_scorers(15) if db_available else get_top_scorers_fallback(15)
    if batsmen:
        df_bat = pd.DataFrame(batsmen)
        df_bat["avg_runs"] = df_bat["avg_runs"].round(2)
        df_bat["strike_rate"] = df_bat["strike_rate"].round(2)
        df_bat.index = range(1, len(df_bat) + 1)
        df_bat.index.name = "Rank"

        # Color team column
        def color_team(val):
            colors = {"MI": "#004B8D", "CSK": "#FDB913", "RCB": "#E31837",
                     "KKR": "#3A225D", "SRH": "#FF8225", "DC": "#1C3F8A",
                     "PBK": "#D71920", "RR": "#C22B2B", "GT": "#003C82", "LSG": "#1A3C8C"}
            return f"background-color: {colors.get(val, '#f0f0f0')}; color: white; padding: 4px 8px; border-radius: 4px; font-weight: 600"

        st.dataframe(
            df_bat.style
            .applymap(color_team, subset=["team"])
            .format({
                "total_runs": "{:,}",
                "avg_runs": "{:.2f}",
                "strike_rate": "{:.2f}",
                "highest": "{:.0f}",
            }),
            use_container_width=True,
            height=500,
        )

        # Visual: Runs vs Strike Rate scatter
        fig = px.scatter(
            df_bat,
            x="total_runs",
            y="strike_rate",
            size="matches_batted",
            color="team",
            hover_data=["full_name", "avg_runs", "highest", "fours", "sixes"],
            size_max=40,
        )
        fig.update_layout(
            title="Runs vs Strike Rate (bubble size = matches)",
            xaxis_title="Total Runs",
            yaxis_title="Strike Rate",
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No batting data available. Check database connection.")

# ── Tab 3: Top Bowlers ───────────────────────────────────────
with tab3:
    st.markdown("### 🎯 Top Wicket Takers")
    bowlers = get_top_bowlers(15) if db_available else get_top_bowlers_fallback(15)
    if bowlers:
        df_bowl = pd.DataFrame(bowlers)
        df_bowl["economy"] = df_bowl["economy"].round(2)
        df_bowl["bowling_avg"] = df_bowl["bowling_avg"].round(2)
        df_bowl["strike_rate"] = df_bowl["strike_rate"].round(2)
        df_bowl.index = range(1, len(df_bowl) + 1)
        df_bowl.index.name = "Rank"

        def color_team_bowl(val):
            colors = {"MI": "#004B8D", "CSK": "#FDB913", "RCB": "#E31837",
                     "KKR": "#3A225D", "SRH": "#FF8225", "DC": "#1C3F8A",
                     "PBK": "#D71920", "RR": "#C22B2B", "GT": "#003C82", "LSG": "#1A3C8C"}
            return f"background-color: {colors.get(val, '#f0f0f0')}; color: white; padding: 4px 8px; border-radius: 4px; font-weight: 600"

        st.dataframe(
            df_bowl.style
            .applymap(color_team_bowl, subset=["team"])
            .format({
                "total_wickets": "{:,}",
                "economy": "{:.2f}",
                "bowling_avg": "{:.2f}",
                "strike_rate": "{:.2f}",
            }),
            use_container_width=True,
            height=500,
        )

        # Wickets vs Economy
        fig = px.scatter(
            df_bowl,
            x="total_wickets",
            y="economy",
            size="matches_bowled",
            color="team",
            hover_data=["full_name", "bowling_avg", "strike_rate"],
            size_max=40,
        )
        fig.update_layout(
            title="Wickets vs Economy (lower economy = better)",
            xaxis_title="Total Wickets",
            yaxis_title="Economy Rate",
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Best economy table
        st.markdown("### ⭐ Best Economy Rates (min 4 matches)")
        economy = get_best_economy(10) if db_available else get_best_economy_fallback(10)
        if economy:
            df_econ = pd.DataFrame(economy)
            df_econ.index = range(1, len(df_econ) + 1)
            df_econ.index.name = "Rank"
            st.dataframe(
                df_econ.style
                .applymap(color_team_bowl, subset=["team"])
                .format({"economy": "{:.2f}", "total_overs": "{:.1f}"}),
                use_container_width=True,
            )
    else:
        st.info("No bowling data available. Check database connection.")

# ── Tab 4: All-Rounders ─────────────────────────────────────
with tab4:
    st.markdown("### ⚡ Best All-Rounders")
    st.caption("Ranking = (runs ÷ 100) + wickets")
    allround = get_all_rounders(15) if db_available else get_allrounders_fallback(15)
    if allround:
        df_ar = pd.DataFrame(allround)
        df_ar["allrounder_score"] = df_ar["allrounder_score"].round(2)
        df_ar.index = range(1, len(df_ar) + 1)
        df_ar.index.name = "Rank"

        def color_team_ar(val):
            colors = {"MI": "#004B8D", "CSK": "#FDB913", "RCB": "#E31837",
                     "KKR": "#3A225D", "SRH": "#FF8225", "DC": "#1C3F8A",
                     "PBK": "#D71920", "RR": "#C22B2B", "GT": "#003C82", "LSG": "#1A3C8C"}
            return f"background-color: {colors.get(val, '#f0f0f0')}; color: white; padding: 4px 8px; border-radius: 4px; font-weight: 600"

        st.dataframe(
            df_ar.style
            .applymap(color_team_ar, subset=["team"])
            .format({"total_runs": "{:,}"}),
            use_container_width=True,
            height=500,
        )

        # Dual bar chart: runs + wickets
        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=("Total Runs", "Total Wickets"),
                            horizontal_spacing=0.15)
        top10 = df_ar.head(10)
        fig.add_trace(go.Bar(x=top10["full_name"], y=top10["total_runs"],
                              marker_color="#4CAF50", name="Runs"), row=1, col=1)
        fig.add_trace(go.Bar(x=top10["full_name"], y=top10["total_wickets"],
                              marker_color="#2196F3", name="Wickets"), row=1, col=2)
        fig.update_layout(height=380, showlegend=False,
                          xaxis_tickangle=-30, xaxis2_tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No all-rounder data available.")

# ─── Footer ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color: #888; font-size: 0.85rem;'>"
    "🏏 Cricket Stats Dashboard | Built with Streamlit + MySQL | "
    "Data: IPL 2008–2024 + International Cricket"
    "</p>",
    unsafe_allow_html=True,
)
