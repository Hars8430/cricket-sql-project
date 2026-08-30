"""
🏆 Teams & Standings Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from lib.db import get_team_wins, get_standings, get_series_list, get_venue_stats, is_mysql_available
from lib.sample_data import get_team_wins_fallback, get_venue_stats_fallback, get_standings_fallback

st.set_page_config(page_title="Teams & Standings", page_icon="🏆", layout="wide")

db_available = is_mysql_available()

st.markdown("# 🏆 Teams & Standings")
st.caption("IPL franchise performance and tournament points tables")

st.markdown("---")

# ─── Team Wins ──────────────────────────────────────────────
st.markdown("### 📊 Team Win/Loss Records")

teams = get_team_wins() if db_available else get_team_wins_fallback()
if teams:
    df = pd.DataFrame(teams)

    col1, col2 = st.columns([1, 1])

    with col1:
        fig = px.bar(
            df.head(10),
            x="wins",
            y="short_name",
            orientation="h",
            color="wins",
            color_continuous_scale="Greens",
            text_auto=True,
            category_orders={"short_name": df.head(10)["short_name"].tolist()[::-1]},
        )
        fig.update_layout(
            height=400,
            yaxis_title="",
            xaxis_title="Wins",
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(
            df.head(10),
            x="losses",
            y="short_name",
            orientation="h",
            color="losses",
            color_continuous_scale="Reds",
            text_auto=True,
            category_orders={"short_name": df.head(10)["short_name"].tolist()[::-1]},
        )
        fig2.update_layout(
            height=400,
            yaxis_title="",
            xaxis_title="Losses",
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "wins": st.column_config.NumberColumn("Wins", format="%d"),
            "losses": st.column_config.NumberColumn("Losses", format="%d"),
            "ties": st.column_config.NumberColumn("Ties", format="%d"),
            "no_results": st.column_config.NumberColumn("N/R", format="%d"),
            "total_matches": st.column_config.NumberColumn("Matches", format="%d"),
        },
        hide_index=True,
    )
else:
    st.warning("No team data available.")

st.markdown("---")

# ─── Points Table ───────────────────────────────────────────
st.markdown("### 🏅 Tournament Points Table")

series = get_series_list()
series_options = {s["name"]: s["id"] for s in series} if series else {}

selected = st.selectbox(
    "Select Tournament",
    options=list(series_options.keys()),
    index=0 if series_options else None,
)

if selected and series_options:
    standings = get_standings(series_options[selected]) if db_available else get_standings_fallback()
    if standings:
        df_pts = pd.DataFrame(standings)
        df_pts["win_pct"] = df_pts["win_pct"].round(1)

        # Color the NRR column
        def color_nrr(val):
            try:
                v = float(val)
                if v > 0:
                    return "color: green; font-weight: 600"
                elif v < 0:
                    return "color: red; font-weight: 600"
            except:
                pass
            return ""

        def color_pts(val):
            try:
                v = float(val)
                if v >= 16:
                    return "background-color: #c8e6c9; font-weight: 700"
                elif v >= 12:
                    return "background-color: #fff9c4; font-weight: 600"
            except:
                pass
            return ""

        st.dataframe(
            df_pts.style
            .applymap(color_nrr, subset=["net_rr"])
            .applymap(color_pts, subset=["points"])
            .format({
                "points": "{:.0f}",
                "net_rr": "{:.3f}",
                "win_pct": "{:.1f}%",
            }),
            use_container_width=True,
            column_config={
                "short_name": st.column_config.TextColumn("Team"),
                "name": st.column_config.TextColumn("Full Name"),
                "matches_played": st.column_config.NumberColumn("MP", format="%d"),
                "wins": st.column_config.NumberColumn("W", format="%d"),
                "losses": st.column_config.NumberColumn("L", format="%d"),
                "points": st.column_config.NumberColumn("Pts", format="%d"),
                "net_rr": st.column_config.NumberColumn("NRR", format="%.3f"),
                "win_pct": st.column_config.TextColumn("Win%"),
            },
            hide_index=True,
        )
    else:
        st.info("No standings data for this tournament.")

st.markdown("---")

# ─── Venues ────────────────────────────────────────────────
st.markdown("### 📍 Venue Statistics")

venues = get_venue_stats() if db_available else get_venue_stats_fallback()
if venues:
    df_v = pd.DataFrame(venues)

    fig = px.treemap(
        df_v.head(15),
        path=["city", "venue"],
        values="matches_here",
        color="matches_here",
        color_continuous_scale="Greens",
        title="Matches by City & Venue",
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        df_v,
        use_container_width=True,
        column_config={
            "matches_here": st.column_config.NumberColumn("Matches", format="%d"),
            "teams_visited": st.column_config.NumberColumn("Teams", format="%d"),
        },
        hide_index=True,
    )
