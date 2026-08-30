"""
Sample cricket data — embedded CSV data for Streamlit Cloud deployment.
Used when MySQL is not available.
Data covers IPL 2024 cricket statistics.
"""

import pandas as pd

# ─── Teams ──────────────────────────────────────────────
TEAMS_CSV = """short_name,name,wins,losses,ties,no_results,total_matches,net_rr
GT,Gujarat Titans,10,4,0,0,14,0.793
KKR,Kolkata Knight Riders,9,4,0,1,14,1.428
SRH,Sunrisers Hyderabad,8,5,0,1,14,0.572
MI,Mumbai Indians,8,5,0,1,14,0.524
RR,Rajasthan Royals,8,5,0,1,14,0.354
CSK,Chennai Super Kings,7,6,0,1,14,0.211
LSG,Lucknow Super Giants,7,6,0,1,14,0.072
DC,Delhi Capitals,7,6,0,1,14,-0.066
RCB,Royal Challengers Bangalore,6,7,0,1,14,-0.115
PBK,Punjab Kings,5,8,0,1,14,-0.342"""

# ─── Top Batsmen ─────────────────────────────────────────
BATSMEN_CSV = """rank,full_name,team,team_short,matches,total_runs,avg_runs,highest,strike_rate,fours,sixes
1,MS Dhoni,Chennai Super Kings,CSK,10,791,79.10,102,144.70,70,34
2,Aiden Markram,Sunrisers Hyderabad,SRH,10,776,77.60,102,140.63,63,35
3,Rohit Sharma,Mumbai Indians,MI,10,769,76.90,102,144.22,64,36
4,Virat Kohli,Royal Challengers Bangalore,RCB,9,597,66.33,89,138.07,48,28
5,Shreyas Iyer,Kolkata Knight Riders,KKR,8,567,70.88,89,139.05,45,27
6,David Warner,Delhi Capitals,DC,8,554,69.25,102,139.79,46,25
7,Mayank Agarwal,Sunrisers Hyderabad,SRH,10,479,47.90,78,139.30,39,20
8,Ruturaj Gaikwad,Chennai Super Kings,CSK,10,448,44.80,78,137.39,38,18
9,Trent Boult,Gujarat Titans,GT,6,413,68.83,102,138.72,34,19
10,Sunil Narine,Kolkata Knight Riders,KKR,8,387,48.38,89,135.57,32,17
11,Anrich Nortje,Punjab Kings,PBK,5,375,75.00,89,138.39,31,15
12,Faf du Plessis,Royal Challengers Bangalore,RCB,9,372,41.33,78,139.98,32,17
13,Hardik Pandya,Mumbai Indians,MI,9,332,36.89,45,138.65,27,16
14,Shikhar Dhawan,Punjab Kings,PBK,5,280,56.00,89,139.84,24,11
15,Mohammed Shami,Gujarat Titans,GT,3,221,73.67,78,137.88,18,10"""

# ─── Top Bowlers ────────────────────────────────────────
BOWLERS_CSV = """rank,full_name,team,team_short,matches,total_wickets,economy,bowling_avg,strike_rate
1,Jasprit Bumrah,Mumbai Indians,MI,8,22,7.28,10.59,16.67
2,Deepak Chahar,Chennai Super Kings,CSK,7,17,7.50,12.35,18.53
3,Riyan Parag,Gujarat Titans,GT,4,11,8.13,11.82,19.64
4,Sunil Narine,Kolkata Knight Riders,KKR,6,11,8.42,18.36,22.18
5,Bhuvneshwar Kumar,Sunrisers Hyderabad,SRH,4,8,9.00,18.00,20.25
6,Matheesha Pathirana,Chennai Super Kings,CSK,7,7,8.93,35.71,32.71
7,Liam Livingstone,Punjab Kings,PBK,4,6,8.06,21.50,24.83
8,Suryakumar Yadav,Mumbai Indians,MI,6,6,8.25,33.00,27.33
9,Kagiso Rabada,Punjab Kings,PBK,4,6,8.56,22.83,25.17
10,Andre Russell,Kolkata Knight Riders,KKR,6,6,9.92,39.67,32.50"""

# ─── All-Rounders ──────────────────────────────────────
ALLROUNDERS_CSV = """rank,full_name,team,team_short,role,total_runs,total_wickets,allrounder_score
1,Hardik Pandya,Mumbai Indians,MI,all-rounder,332,6,9.32
2,Andre Russell,Kolkata Knight Riders,KKR,all-rounder,387,6,9.87
3,Sunil Narine,Kolkata Knight Riders,KKR,all-rounder,387,11,14.87
4,Axar Patel,Delhi Capitals,DC,all-rounder,116,5,6.16
5,Sam Curran,Punjab Kings,PBK,all-rounder,208,0,2.08"""

# ─── Venues ─────────────────────────────────────────────
VENUES_CSV = """venue,city,country,matches_here,teams_visited
M. Chinnaswamy Stadium,Bengaluru,India,7,2
Eden Gardens,Kolkata,India,6,2
Wankhede Stadium,Mumbai,India,5,2
M. A. Chidambaram Stadium,Chennai,India,5,2
Arun Jaitley Stadium,Delhi,India,4,2
PCA Stadium,Mohali,India,3,2
Sawai Mansingh Stadium,Jaipur,India,3,2
Rajiv Gandhi International Stadium,Hyderabad,India,3,2
Narendra Modi Stadium,Ahmedabad,India,3,2"""

# ─── Players (for dropdown) ──────────────────────────────
PLAYERS_CSV = """full_name,team,country,role,batting_style,bowling_style
Rohit Sharma,MI,India,batsman,right-handed,
MS Dhoni,CSK,India,wicket-keeper,right-handed,
Virat Kohli,RCB,India,batsman,right-handed,
Shreyas Iyer,KKR,India,batsman,right-handed,
Hardik Pandya,MI,India,all-rounder,right-handed,fast-medium
Jasprit Bumrah,MI,India,bowler,right-handed,fast
Aiden Markram,SRH,South Africa,batsman,right-handed,off-spin
Andre Russell,KKR,West Indies,all-rounder,right-handed,fast
Sunil Narine,KKR,West Indies,all-rounder,left-handed,off-spin
David Warner,DC,Australia,batsman,left-handed,
Shubman Gill,GT,India,batsman,right-handed,
Rashid Khan,GT,Afghanistan,bowler,right-handed,leg-spin
Trent Boult,RR,New Zealand,bowler,right-handed,fast
Suryakumar Yadav,MI,India,batsman,right-handed,
Ravindra Jadeja,CSK,India,all-rounder,left-handed,left-arm
KL Rahul,LSG,India,wicket-keeper,right-handed,
Deepak Chahar,CSK,India,bowler,right-handed,fast-medium
Bhuvneshwar Kumar,SRH,India,bowler,right-handed,fast-medium
Mayank Agarwal,SRH,India,batsman,right-handed,
Ruturaj Gaikwad,CSK,India,batsman,right-handed,
Faf du Plessis,RCB,South Africa,batsman,right-handed,
Kagiso Rabada,PBK,South Africa,bowler,left-handed,fast
Mohammed Siraj,RCB,India,bowler,right-handed,fast
Glenn Maxwell,RCB,Australia,all-rounder,right-handed,off-spin
Sam Curran,PBK,England,all-rounder,left-handed,fast-medium
Riyan Parag,RR,India,all-rounder,right-handed,leg-spin
Axar Patel,DC,India,all-rounder,left-handed,left-arm
Ishan Kishan,MI,India,wicket-keeper,left-handed,
Sanju Samson,RR,India,wicket-keeper,right-handed,
Jos Buttler,RR,England,batsman,right-handed,
Yashasvi Jaiswal,RR,India,batsman,left-handed,
Rinku Singh,KKR,India,batsman,left-handed,
Nicholas Pooran,LSG,West Indies,wicket-keeper,left-handed,
Quinton de Kock,LSG,South Africa,wicket-keeper,left-handed,
Marcus Stoinis,LSG,Australia,all-rounder,right-handed,fast-medium
Ravi Bishnoi,LSG,India,bowler,right-handed,leg-spin
Anrich Nortje,DC,South Africa,bowler,right-handed,fast
Kuldeep Yadav,DC,India,bowler,left-handed,leg-spin
Yuzvendra Chahal,RR,India,bowler,right-handed,leg-spin
Heinrich Klaasen,SRH,South Africa,wicket-keeper,right-handed,
Travis Head,SRH,Australia,batsman,left-handed,off-spin"""


def load_teams() -> pd.DataFrame:
    return pd.read_csv(pd.io.common.StringIO(TEAMS_CSV))


def load_batsmen() -> pd.DataFrame:
    return pd.read_csv(pd.io.common.StringIO(BATSMEN_CSV))


def load_bowlers() -> pd.DataFrame:
    return pd.read_csv(pd.io.common.StringIO(BOWLERS_CSV))


def load_allrounders() -> pd.DataFrame:
    return pd.read_csv(pd.io.common.StringIO(ALLROUNDERS_CSV))


def load_venues() -> pd.DataFrame:
    return pd.read_csv(pd.io.common.StringIO(VENUES_CSV))


def load_players() -> list:
    return pd.read_csv(pd.io.common.StringIO(PLAYERS_CSV))["full_name"].tolist()


def get_summary_fallback() -> dict:
    """Summary stats when DB not available."""
    teams = load_teams()
    batsmen = load_batsmen()
    bowlers = load_bowlers()
    return {
        "teams": len(teams),
        "players": 79,
        "matches": 36,
        "total_runs": int(batsmen["total_runs"].sum()),
        "total_wickets": int(bowlers["total_wickets"].sum()),
        "series": 13,
    }


def get_boundary_hitters_fallback(limit: int = 15) -> list[dict]:
    """Top boundary hitters."""
    df = load_batsmen().copy()
    if 'team' in df.columns and 'team_short' in df.columns:
        df = df.drop(columns=['team_short'])
    return df.nlargest(limit, "sixes").to_dict("records")


def get_top_scorers_fallback(limit: int = 15) -> list[dict]:
    """Top scorers as list of dicts."""
    df = load_batsmen().head(limit)
    # Drop duplicate team_short column if exists
    if 'team' in df.columns and 'team_short' in df.columns:
        df = df.drop(columns=['team_short'])
    if 'matches' in df.columns and 'matches_batted' not in df.columns:
        df = df.rename(columns={'matches': 'matches_batted'})
    return df.to_dict("records")


def get_top_bowlers_fallback(limit: int = 15) -> list[dict]:
    df = load_bowlers().head(limit)
    if 'team_short' in df.columns:
        df = df.rename(columns={'team_short': 'team'})
    if 'matches' in df.columns and 'matches_bowled' not in df.columns:
        df = df.rename(columns={'matches': 'matches_bowled'})
    return df.to_dict("records")


def get_team_wins_fallback() -> list[dict]:
    df = load_teams()
    return df.to_dict("records")


def get_allrounders_fallback(limit: int = 15) -> list[dict]:
    df = load_allrounders().head(limit)
    if 'team_short' in df.columns:
        df = df.rename(columns={'team_short': 'team'})
    return df.to_dict("records")


def get_venue_stats_fallback() -> list[dict]:
    df = load_venues()
    return df.to_dict("records")


def get_best_strike_rates_fallback(limit: int = 15) -> list[dict]:
    df = load_batsmen().head(limit)
    if 'team_short' in df.columns:
        df = df.rename(columns={'team_short': 'team'})
    if 'matches' in df.columns and 'matches_batted' not in df.columns:
        df = df.rename(columns={'matches': 'matches_batted'})
    return df.to_dict("records")


def get_best_economy_fallback(limit: int = 15) -> list[dict]:
    df = load_bowlers().nsmallest(limit, "economy")
    return df.to_dict("records")


def get_standings_fallback() -> list[dict]:
    df = load_teams()
    return df.to_dict("records")


def get_players_list_fallback() -> list[dict]:
    return [{"full_name": p} for p in load_players()]


def get_match_types_fallback() -> list[dict]:
    return [
        {"match_type": "T20", "total_matches": 36, "total_runs": 8462, "avg_runs": 53.92, "total_wickets": 143, "avg_overs": 4.0}
    ]


def get_player_comparison_fallback(player1: str, player2: str) -> list[dict]:
    """Get sample comparison data."""
    df = load_batsmen()
    rows = []
    for p in [player1, player2]:
        match = df[df["full_name"] == p]
        if not match.empty:
            r = match.iloc[0]
            rows.append({
                "full_name": r["full_name"],
                "role": "batsman",
                "country": "India",
                "matches": int(r["matches"]),
                "runs": int(r["total_runs"]),
                "avg_runs": float(r["avg_runs"]),
                "highest": int(r["highest"]),
                "strike_rate": float(r["strike_rate"]),
                "fours": int(r["fours"]),
                "sixes": int(r["sixes"]),
            })
    return rows


def get_player_detail_fallback(name: str) -> dict:
    """Get sample player detail."""
    df = load_batsmen()
    match = df[df["full_name"] == name]
    if match.empty:
        return None
    r = match.iloc[0]

    player_info = {
        "full_name": r["full_name"],
        "country": "India",
        "role": "batsman",
        "team_name": r["team"],
        "batting_style": "right-handed",
        "bowling_style": None,
    }

    batting = {
        "matches": int(r["matches"]),
        "total_runs": int(r["total_runs"]),
        "avg_runs": float(r["avg_runs"]),
        "highest": int(r["highest"]),
        "strike_rate": float(r["strike_rate"]),
        "fours": int(r["fours"]),
        "sixes": int(r["sixes"]),
        "centuries": 1 if r["total_runs"] >= 600 else 0,
        "fifties": int(r["total_runs"] // 70),
    }

    return {
        "player": player_info,
        "batting": batting,
        "bowling": {"matches": 0, "total_wickets": 0, "economy": 0, "bowling_avg": 0, "total_overs": 0},
        "recent": [
            {"match_date": "2024-05-19", "venue": "Narendra Modi Stadium", "match_type": "T20", "runs": 67, "balls": 50, "fours": 6, "sixes": 2, "strike_rate": 134.0, "dismissal": "not-out"},
            {"match_date": "2024-05-12", "venue": "PCA Stadium", "match_type": "T20", "runs": 45, "balls": 32, "fours": 4, "sixes": 2, "strike_rate": 140.6, "dismissal": "caught"},
            {"match_date": "2024-05-05", "venue": "Wankhede Stadium", "match_type": "T20", "runs": 65, "balls": 45, "fours": 6, "sixes": 3, "strike_rate": 144.4, "dismissal": "caught"},
        ]
    }
