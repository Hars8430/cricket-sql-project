-- ============================================================
-- Player Comparison & Advanced Analysis Queries
-- ============================================================

USE cricket_db;

-- ------------------------------------------------------------
-- 1. Head-to-Head: Two Players Compared
-- ------------------------------------------------------------
SELECT
    p.full_name,
    p.role,
    p.country,
    COUNT(DISTINCT b.match_id)          AS matches,
    SUM(b.runs)                          AS runs,
    ROUND(AVG(b.runs), 2)               AS avg_runs,
    ROUND(MAX(b.runs), 0)               AS highest,
    ROUND(SUM(b.runs) * 100.0 / NULLIF(SUM(b.balls), 0), 2) AS strike_rate,
    SUM(b.fours)                         AS fours,
    SUM(b.sixes)                         AS sixes
FROM players p
LEFT JOIN batting_stats b ON b.player_id = p.id
WHERE p.full_name IN ('Virat Kohli', 'Rohit Sharma')
GROUP BY p.id, p.full_name, p.role, p.country
ORDER BY runs DESC;

-- ------------------------------------------------------------
-- 2. All-Rounders Performance Matrix
-- ------------------------------------------------------------
WITH player_stats AS (
    SELECT
        p.id,
        p.full_name,
        t.short_name AS team,
        p.role,
        COALESCE(SUM(b.runs), 0)    AS runs,
        COALESCE(SUM(bowl.wickets), 0) AS wickets,
        COALESCE(SUM(bowl.overs), 0)    AS overs
    FROM players p
    LEFT JOIN batting_stats b  ON p.id = b.player_id
    LEFT JOIN bowling_stats bw ON p.id = bw.player_id
    LEFT JOIN teams t          ON p.team_id = t.id
    WHERE p.role = 'all-rounder'
    GROUP BY p.id, p.full_name, t.short_name, p.role
)
SELECT
    full_name,
    team,
    runs,
    wickets,
    ROUND(runs * 1.0 / NULLIF(overs, 0), 2) AS batting_per_over,
    ROUND(wickets * 1.0 / NULLIF(overs, 0), 3) AS wickets_per_over,
    ROUND(runs / 100.0 + wickets, 2) AS allrounder_score
FROM player_stats
WHERE overs > 5 AND (runs > 100 OR wickets > 5)
ORDER BY allrounder_score DESC
LIMIT 15;

-- ------------------------------------------------------------
-- 3. Form Analysis (Last 5 Matches Average)
-- ------------------------------------------------------------
WITH recent_batting AS (
    SELECT
        b.player_id,
        b.match_id,
        b.runs,
        ROW_NUMBER() OVER (PARTITION BY b.player_id ORDER BY m.match_date DESC) AS recency
    FROM batting_stats b
    JOIN matches m ON b.match_id = m.id
),
recent_avg AS (
    SELECT
        p.full_name,
        t.short_name AS team,
        COUNT(rb.match_id) AS matches_used,
        ROUND(AVG(rb.runs), 2) AS last_5_avg,
        SUM(rb.runs) AS last_5_runs
    FROM players p
    JOIN recent_batting rb ON p.id = rb.player_id
    JOIN teams t ON p.team_id = t.id
    WHERE rb.recency <= 5
    GROUP BY p.id, p.full_name, t.short_name
    HAVING COUNT(rb.match_id) >= 3
)
SELECT *
FROM recent_avg
ORDER BY last_5_avg DESC
LIMIT 15;

-- ------------------------------------------------------------
-- 4. Performance at Different Venues
-- ------------------------------------------------------------
SELECT
    p.full_name,
    t.short_name AS team,
    m.venue,
    COUNT(DISTINCT m.id) AS matches_at_venue,
    ROUND(AVG(b.runs), 2) AS avg_runs,
    SUM(b.runs) AS total_runs,
    ROUND(MAX(b.runs), 0) AS highest_at_venue
FROM batting_stats b
JOIN players p ON b.player_id = p.id
JOIN teams  t ON b.team_id  = t.id
JOIN matches m ON b.match_id = m.id
WHERE m.venue IS NOT NULL
GROUP BY p.id, p.full_name, t.short_name, m.venue
HAVING COUNT(DISTINCT m.id) >= 2
ORDER BY avg_runs DESC
LIMIT 20;

-- ------------------------------------------------------------
-- 5. Best Batsman by Format
-- ------------------------------------------------------------
WITH format_stats AS (
    SELECT
        p.full_name,
        m.match_type,
        SUM(b.runs) AS runs,
        ROUND(SUM(b.runs) * 100.0 / NULLIF(SUM(b.balls), 0), 2) AS sr,
        COUNT(b.id) AS innings
    FROM batting_stats b
    JOIN players p ON b.player_id = p.id
    JOIN matches m ON b.match_id  = m.id
    GROUP BY p.id, p.full_name, m.match_type
)
SELECT *
FROM format_stats
WHERE (full_name, match_type, runs) IN (
    SELECT full_name, match_type, MAX(runs)
    FROM format_stats
    GROUP BY match_type
)
ORDER BY match_type, runs DESC;

-- ------------------------------------------------------------
-- 6. Best Bowler by Format
-- ------------------------------------------------------------
WITH format_bowling AS (
    SELECT
        p.full_name,
        m.match_type,
        SUM(bw.wickets) AS wickets,
        ROUND(AVG(bw.economy), 2) AS avg_economy,
        COUNT(bw.id) AS spells
    FROM bowling_stats bw
    JOIN players p  ON bw.player_id = p.id
    JOIN matches m  ON bw.match_id  = m.id
    GROUP BY p.id, p.full_name, m.match_type
)
SELECT *
FROM format_bowling
WHERE (full_name, match_type, wickets) IN (
    SELECT full_name, match_type, MAX(wickets)
    FROM format_bowling
    GROUP BY match_type
)
ORDER BY match_type, wickets DESC;

-- ------------------------------------------------------------
-- 7. Country-wise Player Distribution
-- ------------------------------------------------------------
SELECT
    country,
    COUNT(*)                              AS total_players,
    SUM(CASE WHEN is_international THEN 1 ELSE 0 END) AS international_players,
    SUM(CASE WHEN role = 'batsman'         THEN 1 ELSE 0 END) AS batsmen,
    SUM(CASE WHEN role = 'bowler'          THEN 1 ELSE 0 END) AS bowlers,
    SUM(CASE WHEN role = 'all-rounder'     THEN 1 ELSE 0 END) AS all_rounders,
    SUM(CASE WHEN role = 'wicket-keeper'   THEN 1 ELSE 0 END) AS wicket_keepers,
    ROUND(AVG(TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE())), 1) AS avg_age
FROM players
GROUP BY country
ORDER BY total_players DESC;

-- ------------------------------------------------------------
-- 8. Bowling vs Batting Matchups
-- ------------------------------------------------------------
SELECT
    bp.full_name AS bowler,
    bt.full_name AS batsman,
    COUNT(*) AS dismissals,
    GROUP_CONCAT(DISTINCT m.match_type) AS formats
FROM batting_stats b
JOIN bowling_stats bw ON b.match_id = bw.match_id
JOIN players bp ON bw.player_id = bp.id
JOIN players bt ON b.player_id  = bt.id
JOIN matches  m  ON b.match_id   = m.id
WHERE bw.player_id = b.bowler_id
  AND b.dismissal NOT IN ('not-out', 'retired-not-out')
GROUP BY bp.full_name, bt.full_name
HAVING dismissals > 0
ORDER BY dismissals DESC
LIMIT 15;

-- ------------------------------------------------------------
-- 9. Player Career Trajectory (Year by Year)
-- ------------------------------------------------------------
SELECT
    p.full_name,
    YEAR(m.match_date) AS year,
    COUNT(DISTINCT b.match_id) AS matches,
    SUM(b.runs) AS yearly_runs,
    ROUND(AVG(b.runs), 2) AS avg_runs,
    ROUND(MAX(b.runs), 0) AS highest_score
FROM batting_stats b
JOIN players p  ON b.player_id = p.id
JOIN matches m  ON b.match_id  = m.id
WHERE p.full_name = 'Virat Kohli'  -- change to any player
GROUP BY p.id, p.full_name, YEAR(m.match_date)
ORDER BY year;

-- ------------------------------------------------------------
-- 10. Fielding Stats Leaders
-- ------------------------------------------------------------
SELECT
    p.full_name,
    t.short_name AS team,
    SUM(f.catches)   AS total_catches,
    SUM(f.stumpings) AS total_stumpings,
    SUM(f.run_outs)  AS total_run_outs,
    SUM(f.catches) + SUM(f.stumpings) + SUM(f.run_outs) AS total_dismissals,
    COUNT(DISTINCT f.match_id) AS matches
FROM fielding_stats f
JOIN players p ON f.player_id = p.id
JOIN teams t   ON f.team_id  = t.id
GROUP BY p.id, p.full_name, t.short_name
HAVING total_dismissals > 0
ORDER BY total_dismissals DESC
LIMIT 15;
