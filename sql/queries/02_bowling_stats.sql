-- ============================================================
-- Bowling Statistics Queries
-- ============================================================

USE cricket_db;

-- ------------------------------------------------------------
-- 1. Top Wicket Takers
-- ------------------------------------------------------------
SELECT
    p.full_name,
    t.short_name AS team,
    p.bowling_style,
    COUNT(b.id)         AS matches_bowled,
    SUM(b.wickets)      AS total_wickets,
    ROUND(AVG(b.wickets), 2) AS avg_wickets,
    SUM(b.maidens)      AS total_maidens,
    SUM(b.runs_conceded) AS total_runs_conceded,
    ROUND(AVG(b.economy), 2) AS avg_economy
FROM bowling_stats b
JOIN players p ON b.player_id = p.id
JOIN teams t   ON b.team_id  = t.id
GROUP BY p.id, p.full_name, t.short_name, p.bowling_style
HAVING SUM(b.wickets) > 0
ORDER BY total_wickets DESC, avg_economy ASC
LIMIT 20;

-- ------------------------------------------------------------
-- 2. Best Economy Rate (min 4 matches)
-- ------------------------------------------------------------
SELECT
    p.full_name,
    t.short_name AS team,
    COUNT(b.id)             AS matches,
    SUM(b.wickets)          AS wickets,
    ROUND(SUM(b.runs_conceded) / SUM(b.overs), 2) AS economy,
    SUM(b.overs)            AS total_overs
FROM bowling_stats b
JOIN players p ON b.player_id = p.id
JOIN teams t   ON b.team_id  = t.id
GROUP BY p.id, p.full_name, t.short_name
HAVING COUNT(b.id) >= 4 AND SUM(b.overs) > 0
ORDER BY economy ASC
LIMIT 15;

-- ------------------------------------------------------------
-- 3. Best Strike Rate (wickets per ball bowled)
-- ------------------------------------------------------------
SELECT
    p.full_name,
    t.short_name AS team,
    SUM(b.wickets) AS wickets,
    SUM(b.overs * 6) AS balls_bowled,
    ROUND(SUM(b.overs * 6) / NULLIF(SUM(b.wickets), 0), 2) AS strike_rate,
    ROUND(SUM(b.runs_conceded) / NULLIF(SUM(b.wickets), 0), 2) AS bowling_avg
FROM bowling_stats b
JOIN players p ON b.player_id = p.id
JOIN teams t   ON b.team_id  = t.id
GROUP BY p.id, p.full_name, t.short_name
HAVING SUM(b.wickets) >= 5
ORDER BY strike_rate ASC
LIMIT 15;

-- ------------------------------------------------------------
-- 4. Best Bowling Average (runs per wicket)
-- ------------------------------------------------------------
SELECT
    p.full_name,
    t.short_name AS team,
    SUM(b.wickets) AS wickets,
    SUM(b.runs_conceded) AS runs_conceded,
    ROUND(SUM(b.runs_conceded) * 1.0 / NULLIF(SUM(b.wickets), 0), 2) AS bowling_avg,
    COUNT(b.id)   AS matches
FROM bowling_stats b
JOIN players p ON b.player_id = p.id
JOIN teams t   ON b.team_id  = t.id
GROUP BY p.id, p.full_name, t.short_name
HAVING SUM(b.wickets) >= 5
ORDER BY bowling_avg ASC
LIMIT 15;

-- ------------------------------------------------------------
-- 5. Most Maidens
-- ------------------------------------------------------------
SELECT
    p.full_name,
    t.short_name AS team,
    SUM(b.maidens) AS total_maidens,
    COUNT(b.id)     AS matches,
    SUM(b.overs)    AS total_overs
FROM bowling_stats b
JOIN players p ON b.player_id = p.id
JOIN teams t   ON b.team_id  = t.id
GROUP BY p.id, p.full_name, t.short_name
HAVING SUM(b.maidens) > 0
ORDER BY total_maidens DESC
LIMIT 15;

-- ------------------------------------------------------------
-- 6. 5-Wicket Hauls (5+ wickets in a match)
-- ------------------------------------------------------------
SELECT
    p.full_name,
    t.short_name AS team,
    m.match_date,
    m.venue,
    m.match_type,
    b.wickets,
    b.runs_conceded,
    b.overs,
    b.economy
FROM bowling_stats b
JOIN players p ON b.player_id = p.id
JOIN teams  t ON b.team_id   = t.id
JOIN matches m ON b.match_id  = m.id
WHERE b.wickets >= 5
ORDER BY b.wickets DESC, b.economy ASC;

-- ------------------------------------------------------------
-- 7. Best All-Rounders (batting + bowling combined)
-- ------------------------------------------------------------
WITH batting_totals AS (
    SELECT player_id,
           SUM(runs) AS runs,
           COUNT(id)  AS innings
    FROM batting_stats
    GROUP BY player_id
),
bowling_totals AS (
    SELECT player_id,
           SUM(wickets) AS wickets,
           COUNT(id)     AS spells
    FROM bowling_stats
    GROUP BY player_id
)
SELECT
    p.full_name,
    t.short_name AS team,
    p.role,
    COALESCE(b.runs, 0)   AS total_runs,
    COALESCE(bw.wickets, 0) AS total_wickets,
    COALESCE(b.innings, 0) AS batting_innings,
    COALESCE(bw.spells, 0) AS bowling_spells,
    ROUND(COALESCE(b.runs, 0) * 1.0 +
          COALESCE(bw.wickets, 0) * 20, 2) AS allrounder_index
FROM players p
LEFT JOIN batting_totals b  ON p.id = b.player_id
LEFT JOIN bowling_totals bw ON p.id = bw.player_id
LEFT JOIN teams t ON p.team_id = t.id
WHERE p.role = 'all-rounder'
  AND b.runs > 100
  AND bw.wickets > 5
ORDER BY allrounder_index DESC;

-- ------------------------------------------------------------
-- 8. Wickets by Bowling Style
-- ------------------------------------------------------------
SELECT
    p.bowling_style,
    COUNT(DISTINCT b.player_id) AS unique_bowlers,
    COUNT(b.id)                 AS spells,
    SUM(b.wickets)              AS total_wickets,
    ROUND(AVG(b.economy), 2)    AS avg_economy
FROM bowling_stats b
JOIN players p ON b.player_id = p.id
WHERE p.bowling_style IS NOT NULL
GROUP BY p.bowling_style
ORDER BY total_wickets DESC;
