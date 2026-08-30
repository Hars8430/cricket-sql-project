"""
Database connection module for Cricket SQL Dashboard.
Uses MySQL connector with connection pooling.
Supports both local Docker MySQL and Streamlit Cloud deployment.
"""

import os
import streamlit as st
import mysql.connector
from mysql.connector import pooling
from lib.sample_data import (
    load_teams, load_batsmen, load_bowlers,
    load_allrounders, load_venues, load_players,
    get_summary_fallback,
)

# ─── Mode: DB available or sample data ────────────────────
MYSQL_AVAILABLE = None  # None = not checked yet


def is_mysql_available() -> bool:
    """Check if MySQL connection is possible."""
    global MYSQL_AVAILABLE
    if MYSQL_AVAILABLE is not None:
        return MYSQL_AVAILABLE

    try:
        conn = get_connection()
        if conn:
            conn.close()
            MYSQL_AVAILABLE = True
        else:
            MYSQL_AVAILABLE = False
    except Exception:
        MYSQL_AVAILABLE = False

    return MYSQL_AVAILABLE


@st.cache_resource
def get_connection_pool():
    """
    Create a cached MySQL connection pool.
    On Streamlit Cloud: uses st.secrets
    On local: uses environment variables or .env
    """
    # Try Streamlit Cloud secrets first
    try:
        db_config = {
            "host": st.secrets["db_host"],
            "port": int(st.secrets.get("db_port", 3306)),
            "user": st.secrets["db_user"],
            "password": st.secrets["db_password"],
            "database": st.secrets["db_name"],
            "pool_name": "cricket_pool",
            "pool_size": 3,
            "pool_reset_session": True,
        }
    except Exception:
        # Fallback to environment variables for local development
        db_config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", "cricket123"),
            "database": os.getenv("DB_NAME", "cricket_db"),
            "pool_name": "cricket_pool",
            "pool_size": 3,
            "pool_reset_session": True,
        }

    try:
        pool = pooling.MySQLConnectionPool(**db_config)
        return pool
    except mysql.connector.Error as e:
        st.error(f"Database connection failed: {e}")
        st.info("Make sure MySQL is running via `docker compose up -d`")
        return None


def get_connection():
    """Get a connection from the pool."""
    pool = get_connection_pool()
    if pool:
        try:
            return pool.get_connection()
        except mysql.connector.Error as e:
            st.error(f"Failed to get connection: {e}")
            return None
    return None


def run_query(query: str, params: tuple = None, fetch: str = "all") -> list:
    """
    Execute a SQL query and return results.

    Args:
        query: SQL query string (use %s for parameters)
        params: Tuple of parameter values
        fetch: "all" | "one" | None (for INSERT/UPDATE)

    Returns:
        List of tuples (for SELECT) or row count (for INSERT/UPDATE)
    """
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())

        if fetch == "all":
            result = cursor.fetchall()
        elif fetch == "one":
            result = cursor.fetchone()
        else:
            conn.commit()
            result = cursor.rowcount

        cursor.close()
        return result
    except mysql.connector.Error as e:
        st.error(f"Query error: {e}")
        return []
    finally:
        conn.close()


def get_table_count(table_name: str) -> int:
    """Get row count for a specific table."""
    result = run_query(f"SELECT COUNT(*) AS cnt FROM {table_name}", fetch="one")
    if result:
        val = result["cnt"]
        # MySQL returns Decimal, convert to int
        return int(val) if hasattr(val, '__int__') else val
    return 0


def get_summary_stats() -> dict:
    """Get high-level stats for the dashboard."""
    stats = {}
    stats["teams"] = get_table_count("teams")
    stats["players"] = get_table_count("players")
    stats["matches"] = get_table_count("matches")
    stats["batting"] = get_table_count("batting_stats")
    stats["bowling"] = get_table_count("bowling_stats")
    stats["series"] = get_table_count("series")

    # Additional stats
    # Get total runs
    runs_result = run_query("SELECT COALESCE(SUM(runs), 0) AS total_runs FROM batting_stats", fetch="one")
    val = runs_result["total_runs"] if runs_result else 0
    stats["total_runs"] = int(val) if hasattr(val, '__int__') else val

    # Get total wickets
    wickets_result = run_query("SELECT COALESCE(SUM(wickets), 0) AS total_wickets FROM bowling_stats", fetch="one")
    val = wickets_result["total_wickets"] if wickets_result else 0
    stats["total_wickets"] = int(val) if hasattr(val, '__int__') else val

    # Get active players (those with batting data)
    active_result = run_query("SELECT COUNT(DISTINCT player_id) AS cnt FROM batting_stats", fetch="one")
    val = active_result["cnt"] if active_result else 0
    stats["active_players"] = int(val) if hasattr(val, '__int__') else val

    return stats


def get_top_scorers(limit: int = 10) -> list:
    """Get top run scorers."""
    return run_query("""
        SELECT
            p.full_name,
            t.short_name AS team,
            t.name AS team_name,
            COUNT(b.id) AS matches_batted,
            SUM(b.runs) AS total_runs,
            ROUND(AVG(b.runs), 2) AS avg_runs,
            ROUND(MAX(b.runs), 0) AS highest,
            ROUND(SUM(b.runs) * 100.0 / NULLIF(SUM(b.balls), 0), 2) AS strike_rate,
            SUM(b.fours) AS fours,
            SUM(b.sixes) AS sixes
        FROM batting_stats b
        JOIN players p ON b.player_id = p.id
        JOIN teams t ON b.team_id = t.id
        WHERE b.runs > 0
        GROUP BY p.id, p.full_name, t.short_name, t.name
        ORDER BY total_runs DESC
        LIMIT %s
    """, params=(limit,), fetch="all")


def get_top_bowlers(limit: int = 10) -> list:
    """Get top wicket takers."""
    return run_query("""
        SELECT
            p.full_name,
            t.short_name AS team,
            t.name AS team_name,
            COUNT(b.id) AS matches_bowled,
            SUM(b.wickets) AS total_wickets,
            ROUND(SUM(b.runs_conceded) / NULLIF(SUM(b.overs), 0), 2) AS economy,
            ROUND(SUM(b.runs_conceded) * 1.0 / NULLIF(SUM(b.wickets), 0), 2) AS bowling_avg,
            ROUND(SUM(b.overs * 6) / NULLIF(SUM(b.wickets), 0), 2) AS strike_rate
        FROM bowling_stats b
        JOIN players p ON b.player_id = p.id
        JOIN teams t ON b.team_id = t.id
        WHERE b.wickets > 0
        GROUP BY p.id, p.full_name, t.short_name, t.name
        ORDER BY total_wickets DESC, economy ASC
        LIMIT %s
    """, params=(limit,), fetch="all")


def get_team_wins() -> list:
    """Get team win/loss record."""
    return run_query("""
        SELECT
            t.name,
            t.short_name,
            COUNT(CASE WHEN m.winner_id = t.id THEN 1 END) AS wins,
            COUNT(CASE WHEN m.winner_id != t.id
                AND m.winner_id IS NOT NULL
                AND (m.team1_id = t.id OR m.team2_id = t.id)
                THEN 1 END) AS losses,
            COUNT(CASE WHEN m.result = 'tie' THEN 1 END) AS ties,
            COUNT(CASE WHEN m.result = 'no-result' THEN 1 END) AS no_results,
            COUNT(m.id) AS total_matches
        FROM teams t
        LEFT JOIN matches m ON m.team1_id = t.id OR m.team2_id = t.id
        GROUP BY t.id, t.name, t.short_name
        HAVING total_matches > 0
        ORDER BY wins DESC
    """, fetch="all")


def get_series_list() -> list:
    """Get list of all series/tournaments."""
    return run_query("""
        SELECT id, name, short_name, type, country, start_date, end_date
        FROM series
        ORDER BY start_date DESC
    """, fetch="all")


def get_venue_stats() -> list:
    """Get venue statistics."""
    return run_query("""
        SELECT
            venue,
            city,
            country,
            COUNT(*) AS matches_here,
            COUNT(DISTINCT team1_id) AS teams_visited
        FROM matches
        WHERE venue IS NOT NULL
        GROUP BY venue, city, country
        ORDER BY matches_here DESC
        LIMIT 20
    """, fetch="all")


def get_boundary_hitters(limit: int = 10) -> list:
    """Get players with most boundaries (4s + 6s)."""
    return run_query("""
        SELECT
            p.full_name,
            t.short_name AS team,
            SUM(b.fours) + SUM(b.sixes) AS total_boundaries,
            SUM(b.fours) AS fours,
            SUM(b.sixes) AS sixes,
            SUM(b.runs) AS total_runs
        FROM batting_stats b
        JOIN players p ON b.player_id = p.id
        JOIN teams t ON b.team_id = t.id
        GROUP BY p.id, p.full_name, t.short_name
        HAVING total_boundaries > 0
        ORDER BY total_boundaries DESC
        LIMIT %s
    """, params=(limit,), fetch="all")


def get_all_rounders(limit: int = 10) -> list:
    """Get best all-rounders."""
    return run_query("""
        SELECT
            p.full_name,
            t.short_name AS team,
            p.role,
            COALESCE(SUM(bat.runs), 0) AS total_runs,
            COALESCE(SUM(bowl.wickets), 0) AS total_wickets,
            COALESCE(SUM(bowl.overs), 0) AS total_overs,
            ROUND(COALESCE(SUM(bat.runs), 0) / 100.0 +
                  COALESCE(SUM(bowl.wickets), 0), 2) AS allrounder_score
        FROM players p
        LEFT JOIN batting_stats bat ON p.id = bat.player_id
        LEFT JOIN bowling_stats bowl ON p.id = bowl.player_id
        LEFT JOIN teams t ON p.team_id = t.id
        WHERE p.role = 'all-rounder'
        GROUP BY p.id, p.full_name, t.short_name, p.role
        HAVING total_runs > 0 AND total_wickets > 0
        ORDER BY allrounder_score DESC
        LIMIT %s
    """, params=(limit,), fetch="all")


def get_match_types() -> list:
    """Get match type breakdown."""
    return run_query("""
        SELECT
            match_type,
            COUNT(*) AS total_matches,
            SUM(bat.runs) AS total_runs,
            ROUND(AVG(bat.runs), 2) AS avg_runs,
            SUM(bowl.wickets) AS total_wickets,
            ROUND(AVG(bowl.overs), 2) AS avg_overs
        FROM matches m
        LEFT JOIN batting_stats bat ON m.id = bat.match_id
        LEFT JOIN bowling_stats bowl ON m.id = bowl.match_id
        GROUP BY match_type
    """, fetch="all")


def get_player_comparison(player1: str, player2: str) -> list:
    """Head-to-head player comparison."""
    return run_query("""
        SELECT
            p.full_name,
            p.role,
            p.country,
            COUNT(DISTINCT b.match_id) AS matches,
            COALESCE(SUM(b.runs), 0) AS runs,
            ROUND(COALESCE(AVG(b.runs), 0), 2) AS avg_runs,
            ROUND(COALESCE(MAX(b.runs), 0), 0) AS highest,
            ROUND(COALESCE(SUM(b.runs) * 100.0 / NULLIF(SUM(b.balls), 0), 0), 2) AS strike_rate,
            COALESCE(SUM(b.fours), 0) AS fours,
            COALESCE(SUM(b.sixes), 0) AS sixes
        FROM players p
        LEFT JOIN batting_stats b ON p.id = b.player_id
        WHERE p.full_name IN (%s, %s)
        GROUP BY p.id, p.full_name, p.role, p.country
        ORDER BY runs DESC
    """, params=(player1, player2), fetch="all")


def get_best_strike_rates(limit: int = 10) -> list:
    """Best strike rates (min 50 balls faced)."""
    return run_query("""
        SELECT
            p.full_name,
            t.short_name AS team,
            COALESCE(SUM(b.runs), 0) AS total_runs,
            COALESCE(SUM(b.balls), 0) AS balls_faced,
            ROUND(COALESCE(SUM(b.runs) * 100.0 / NULLIF(SUM(b.balls), 0), 0), 2) AS strike_rate,
            COUNT(b.id) AS innings
        FROM players p
        LEFT JOIN batting_stats b ON p.id = b.player_id
        LEFT JOIN teams t ON p.team_id = t.id
        GROUP BY p.id, p.full_name, t.short_name
        HAVING balls_faced >= 50
        ORDER BY strike_rate DESC
        LIMIT %s
    """, params=(limit,), fetch="all")


def get_best_economy(limit: int = 10) -> list:
    """Best economy rates (min 4 matches)."""
    return run_query("""
        SELECT
            p.full_name,
            t.short_name AS team,
            COUNT(b.id) AS matches,
            COALESCE(SUM(b.wickets), 0) AS wickets,
            ROUND(COALESCE(SUM(b.runs_conceded) / NULLIF(SUM(b.overs), 0), 0), 2) AS economy,
            ROUND(SUM(b.overs), 1) AS total_overs
        FROM players p
        LEFT JOIN bowling_stats b ON p.id = b.player_id
        LEFT JOIN teams t ON p.team_id = t.id
        GROUP BY p.id, p.full_name, t.short_name
        HAVING matches >= 4 AND wickets > 0
        ORDER BY economy ASC
        LIMIT %s
    """, params=(limit,), fetch="all")


def get_standings(series_id: int = None) -> list:
    """Get tournament standings."""
    query = """
        SELECT
            t.short_name,
            t.name,
            s.matches_played,
            s.wins,
            s.losses,
            s.points,
            s.net_rr,
            ROUND(s.points * 100.0 / NULLIF(s.matches_played * 2, 0), 1) AS win_pct
        FROM standings s
        JOIN teams t ON s.team_id = t.id
        JOIN series sr ON s.series_id = sr.id
    """
    if series_id:
        query += " WHERE sr.id = %s"
        params = (series_id,)
    else:
        params = None
    query += " ORDER BY s.points DESC, s.net_rr DESC"

    return run_query(query, params=params, fetch="all")


def get_players_list() -> list:
    """Get all players for dropdown selection."""
    return run_query("""
        SELECT DISTINCT full_name
        FROM players
        ORDER BY full_name
    """, fetch="all")


def get_player_detail(name: str) -> dict:
    """Get detailed player stats."""
    # Basic info
    player = run_query("""
        SELECT p.*, t.short_name AS team_name
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.id
        WHERE p.full_name = %s
        LIMIT 1
    """, params=(name,), fetch="one")

    if not player:
        return None

    # Batting stats
    batting = run_query("""
        SELECT
            COUNT(DISTINCT b.match_id) AS matches,
            COALESCE(SUM(b.runs), 0) AS total_runs,
            ROUND(COALESCE(AVG(b.runs), 0), 2) AS avg_runs,
            ROUND(COALESCE(MAX(b.runs), 0), 0) AS highest,
            ROUND(COALESCE(SUM(b.runs) * 100.0 / NULLIF(SUM(b.balls), 0), 0), 2) AS strike_rate,
            COALESCE(SUM(b.fours), 0) AS fours,
            COALESCE(SUM(b.sixes), 0) AS sixes,
            COUNT(CASE WHEN b.runs >= 100 THEN 1 END) AS centuries,
            COUNT(CASE WHEN b.runs >= 50 AND b.runs < 100 THEN 1 END) AS fifties
        FROM batting_stats b
        WHERE b.player_id = (SELECT id FROM players WHERE full_name = %s)
    """, params=(name, name), fetch="one")

    # Bowling stats
    bowling = run_query("""
        SELECT
            COUNT(DISTINCT b.match_id) AS matches,
            COALESCE(SUM(b.wickets), 0) AS total_wickets,
            ROUND(COALESCE(SUM(b.runs_conceded) / NULLIF(SUM(b.overs), 0), 0), 2) AS economy,
            ROUND(COALESCE(SUM(b.runs_conceded) * 1.0 / NULLIF(SUM(b.wickets), 0), 0), 2) AS bowling_avg,
            ROUND(SUM(b.overs), 1) AS total_overs
        FROM bowling_stats b
        WHERE b.player_id = (SELECT id FROM players WHERE full_name = %s)
    """, params=(name, name), fetch="one")

    # Recent matches
    recent = run_query("""
        SELECT
            m.match_date,
            m.venue,
            m.match_type,
            b.runs,
            b.balls,
            b.fours,
            b.sixes,
            b.strike_rate,
            b.dismissal
        FROM batting_stats b
        JOIN matches m ON b.match_id = m.id
        WHERE b.player_id = (SELECT id FROM players WHERE full_name = %s)
        ORDER BY m.match_date DESC
        LIMIT 10
    """, params=(name,), fetch="all")

    return {
        "player": player,
        "batting": batting,
        "bowling": bowling,
        "recent": recent
    }
