-- ============================================================
-- Batting Statistics Queries
-- Cricket Database — MySQL 8.0
-- ============================================================

USE cricket_db;

-- ------------------------------------------------------------
-- 1. Top Run Scorers (All Formats)
-- ------------------------------------------------------------
SELECT
    p.full_name,
    t.short_name AS team,
    p.country,
    COUNT(b.id)         AS matches_batted,
    SUM(b.runs)         AS total_runs,
    ROUND(AVG(b.runs), 2) AS avg_per_innings,
    SUM(b.fours)        AS total_fours,
    SUM(b.sixes)        AS total_sixes,
    ROUND(MAX(b.runs), 2) AS highest_score,
    ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate
FROM batting_stats b
JOIN players p ON b.player_id = p.id
JOIN teams t  ON b.team_id  = t.id
GROUP BY p.id, p.full_name, t.short_name, p.country
HAVING SUM(b.runs) > 0
ORDER BY total_runs DESC
LIMIT 20;

-- ------------------------------------------------------------
-- 2. Best Strike Rates (min 50 balls faced)
-- ------------------------------------------------------------
SELECT
    p.full_name,
    t.short_name AS team,
    SUM(b.runs)   AS total_runs,
    SUM(b.balls)  AS balls_faced,
    ROUND(SUM(b.runs) * 100.0 / SUM(b.balls), 2) AS strike_rate,
    COUNT(b.id)   AS innings
FROM batting_stats b
JOIN players p ON b.player_id = p.id
JOIN teams t  ON b.team_id  = t.id
GROUP BY p.id, p.full_name, t.short_name
HAVING SUM(b.balls) >= 50
ORDER BY strike_rate DESC
LIMIT 15;

-- ------------------------------------------------------------
-- 3. Most Centuries
-- ------------------------------------------------------------
WITH player_match_runs AS (
    SELECT player_id, match_id, SUM(runs) AS match_runs
    FROM batting_stats
    GROUP BY player_id, match_id
)
SELECT
    p.full_name,
    t.short_name AS team,
    COUNT(*) AS centuries
FROM player_match_runs pmr
JOIN players p ON pmr.player_id = p.id
JOIN teams t  ON p.team_id = t.id
WHERE pmr.match_runs >= 100
GROUP BY p.id, p.full_name, t.short_name
ORDER BY centuries DESC, p.full_name;

-- ------------------------------------------------------------
-- 4. Most Fifties (50-99 runs)
-- ------------------------------------------------------------
WITH player_match_runs AS (
    SELECT player_id, match_id, SUM(runs) AS match_runs
    FROM batting_stats
    GROUP BY player_id, match_id
)
SELECT
    p.full_name,
    t.short_name AS team,
    COUNT(*) AS fifties
FROM player_match_runs pmr
JOIN players p ON pmr.player_id = p.id
JOIN teams t  ON p.team_id = t.id
WHERE pmr.match_runs BETWEEN 50 AND 99
GROUP BY p.id, p.full_name, t.short_name
ORDER BY fifties DESC
LIMIT 15;

-- ------------------------------------------------------------
-- 5. Best Average (min 10 innings, min 200 runs)
-- ------------------------------------------------------------
SELECT
    p.full_name,
    t.short_name AS team,
    p.role,
    COUNT(b.id)       AS innings,
    SUM(b.runs)        AS total_runs,
    SUM(CASE WHEN b.dismissal != 'not-out'
             AND b.dismissal != 'retired-not-out' THEN 1
             ELSE 0 END) AS outs,
    ROUND(SUM(b.runs) /
        NULLIF(SUM(CASE WHEN b.dismissal != 'not-out'
                        AND b.dismissal != 'retired-not-out' THEN 1 ELSE 0 END), 0), 2) AS batting_avg
FROM batting_stats b
JOIN players p ON b.player_id = p.id
JOIN teams t  ON b.team_id  = t.id
GROUP BY p.id, p.full_name, t.short_name, p.role
HAVING SUM(b.runs) >= 200
   AND SUM(CASE WHEN b.dismissal != 'not-out'
                AND b.dismissal != 'retired-not-out' THEN 1 ELSE 0 END) > 0
ORDER BY batting_avg DESC
LIMIT 20;

-- ------------------------------------------------------------
-- 6. Boundary Hitters (Most 4s + 6s combined)
-- ------------------------------------------------------------
SELECT
    p.full_name,
    t.short_name AS team,
    SUM(b.fours) + SUM(b.sixes) AS total_boundaries,
    SUM(b.fours) AS fours,
    SUM(b.sixes) AS sixes,
    SUM(b.runs)  AS total_runs
FROM batting_stats b
JOIN players p ON b.player_id = p.id
JOIN teams t  ON b.team_id  = t.id
GROUP BY p.id, p.full_name, t.short_name
HAVING total_boundaries > 0
ORDER BY total_boundaries DESC
LIMIT 15;

-- ------------------------------------------------------------
-- 7. Unbeaten Innings (Not Out scores, sorted by runs)
-- ------------------------------------------------------------
SELECT
    p.full_name,
    t.short_name AS team,
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
JOIN players p ON b.player_id = p.id
JOIN teams  t ON b.team_id   = t.id
JOIN matches m ON b.match_id  = m.id
WHERE b.dismissal IN ('not-out', 'retired-not-out')
ORDER BY b.runs DESC
LIMIT 20;

-- ------------------------------------------------------------
-- 8. IPL vs International Performance Comparison
-- ------------------------------------------------------------
SELECT
    p.full_name,
    m.match_type,
    COUNT(DISTINCT m.id)                AS matches,
    SUM(b.runs)                         AS total_runs,
    ROUND(AVG(b.runs), 2)              AS avg_per_match,
    ROUND(SUM(b.runs) * 100.0 / NULLIF(SUM(b.balls), 0), 2) AS strike_rate
FROM batting_stats b
JOIN players p  ON b.player_id = p.id
JOIN matches  m  ON b.match_id  = m.id
WHERE p.is_international = TRUE
GROUP BY p.id, p.full_name, m.match_type
ORDER BY p.full_name, m.match_type;
