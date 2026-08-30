-- ============================================================
-- Team & Tournament Analysis Queries
-- ============================================================

USE cricket_db;

-- ------------------------------------------------------------
-- 1. Team Win/Loss Record
-- ------------------------------------------------------------
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
ORDER BY wins DESC;

-- ------------------------------------------------------------
-- 2. IPL Points Table (IPL 2024)
-- ------------------------------------------------------------
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
WHERE sr.short_name = 'IPL-2024'
ORDER BY s.points DESC, s.net_rr DESC;

-- ------------------------------------------------------------
-- 3. Tournament Performance Summary
-- ------------------------------------------------------------
SELECT
    sr.name AS tournament,
    sr.type,
    COUNT(DISTINCT m.id) AS matches,
    SUM(bat.runs) AS total_runs,
    ROUND(AVG(bat.runs), 2) AS avg_runs_per_innings,
    SUM(bowl.wickets) AS total_wickets
FROM series sr
JOIN match_series ms ON sr.id = ms.series_id
JOIN matches m ON ms.match_id = m.id
LEFT JOIN batting_stats bat ON m.id = bat.match_id
LEFT JOIN bowling_stats bowl ON m.id = bowl.match_id
GROUP BY sr.id, sr.name, sr.type
ORDER BY sr.start_date DESC;

-- ------------------------------------------------------------
-- 4. Most Matches at a Venue
-- ------------------------------------------------------------
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
LIMIT 20;

-- ------------------------------------------------------------
-- 5. T20 vs ODI vs Test Match Distribution
-- ------------------------------------------------------------
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
GROUP BY match_type;

-- ------------------------------------------------------------
-- 6. Team Boundary Stats
-- ------------------------------------------------------------
SELECT
    t.short_name,
    t.name,
    SUM(b.fours) AS total_fours,
    SUM(b.sixes) AS total_sixes,
    SUM(b.fours + b.sixes) AS total_boundaries,
    SUM(b.runs) AS total_runs,
    ROUND(SUM(b.fours + b.sixes) * 100.0 / NULLIF(SUM(b.runs), 0), 2) AS boundary_pct
FROM batting_stats b
JOIN teams t ON b.team_id = t.id
GROUP BY t.id, t.short_name, t.name
ORDER BY total_boundaries DESC;

-- ------------------------------------------------------------
-- 7. Toss Impact Analysis
-- ------------------------------------------------------------
SELECT
    CASE
        WHEN m.toss_decision = 'bat' THEN 'Bat First'
        WHEN m.toss_decision = 'bowl' THEN 'Field First'
        ELSE 'Unknown'
    END AS toss_decision,
    COUNT(m.id) AS total_matches,
    SUM(CASE WHEN m.toss_winner_id = m.winner_id THEN 1 ELSE 0 END) AS toss_winner_won,
    ROUND(SUM(CASE WHEN m.toss_winner_id = m.winner_id THEN 1 ELSE 0 END) * 100.0 / COUNT(m.id), 1) AS win_pct_after_toss
FROM matches m
WHERE m.toss_decision IS NOT NULL AND m.winner_id IS NOT NULL
GROUP BY toss_decision;

-- ------------------------------------------------------------
-- 8. Highest Individual Scores by Format
-- ------------------------------------------------------------
SELECT
    m.match_type,
    p.full_name,
    t.short_name AS team,
    m.venue,
    m.match_date,
    b.runs,
    b.balls,
    b.fours,
    b.sixes,
    b.strike_rate
FROM batting_stats b
JOIN players p ON b.player_id = p.id
JOIN teams  t ON b.team_id  = t.id
JOIN matches m ON b.match_id = m.id
WHERE b.runs = (
    SELECT MAX(b2.runs)
    FROM batting_stats b2
    JOIN matches m2 ON b2.match_id = m2.id
    WHERE m2.match_type = m.match_type
)
ORDER BY m.match_type;

-- ------------------------------------------------------------
-- 9. Win Margins by Team
-- ------------------------------------------------------------
SELECT
    t.short_name,
    t.name,
    COUNT(CASE WHEN m.winner_id = t.id THEN 1 END) AS wins,
    ROUND(AVG(bat.runs), 0) AS avg_win_runs
FROM teams t
JOIN matches m ON m.winner_id = t.id
JOIN batting_stats bat ON m.id = bat.match_id AND bat.team_id = t.id
GROUP BY t.id, t.short_name, t.name
ORDER BY wins DESC;
