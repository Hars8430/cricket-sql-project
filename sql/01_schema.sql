-- ============================================================
-- Cricket Database Schema
-- MySQL 8.0
-- ============================================================

USE cricket_db;

-- ------------------------------------------------------------
-- Teams Table
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS teams (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    short_name  CHAR(3) NOT NULL,        -- e.g., 'RCB', 'MI', 'IND'
    country     VARCHAR(50),              -- NULL for club/T20 teams
    founded     YEAR,
    home_ground VARCHAR(100),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_short_name (short_name)
);

-- ------------------------------------------------------------
-- Players Table
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS players (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    first_name    VARCHAR(50) NOT NULL,
    last_name     VARCHAR(50) NOT NULL,
    full_name     VARCHAR(100) NOT NULL,
    country       VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    role          ENUM('batsman', 'bowler', 'all-rounder', 'wicket-keeper') NOT NULL,
    batting_style ENUM('right-handed', 'left-handed', 'switch-hit') DEFAULT NULL,
    bowling_style ENUM('fast', 'fast-medium', 'medium', 'off-spin', 'leg-spin', 'left-arm') DEFAULT NULL,
    team_id       INT,
    is_international BOOLEAN DEFAULT FALSE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL
);

-- ------------------------------------------------------------
-- Matches Table
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS matches (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    match_date    DATE NOT NULL,
    team1_id      INT NOT NULL,
    team2_id      INT NOT NULL,
    venue          VARCHAR(100),
    city           VARCHAR(50),
    country        VARCHAR(50),
    match_type     ENUM('T20', 'ODI', 'TEST') NOT NULL,
    toss_winner_id INT,             -- team that won the toss
    toss_decision  ENUM('bat', 'bowl', 'field') DEFAULT NULL,
    winner_id      INT,             -- team that won the match
    man_of_the_match_id INT,        -- player id
    team1_score    VARCHAR(20),      -- e.g., '180/7'  (NULL if chasing or not batted)
    team2_score    VARCHAR(20),      -- NULL if not yet batted
    target         INT,             -- target for the chasing team
    result         ENUM('normal', 'tie', 'no-result', 'walkover') DEFAULT 'normal',
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team1_id) REFERENCES teams(id),
    FOREIGN KEY (team2_id) REFERENCES teams(id),
    FOREIGN KEY (toss_winner_id) REFERENCES teams(id),
    FOREIGN KEY (winner_id) REFERENCES teams(id),
    FOREIGN KEY (man_of_the_match_id) REFERENCES players(id),
    CHECK (team1_id != team2_id)
);

-- ------------------------------------------------------------
-- Batting Stats Table (per innings per player)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS batting_stats (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    match_id     INT NOT NULL,
    player_id    INT NOT NULL,
    team_id      INT NOT NULL,
    runs         SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    balls        SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    fours        TINYINT UNSIGNED NOT NULL DEFAULT 0,
    sixes        TINYINT UNSIGNED NOT NULL DEFAULT 0,
    strike_rate  DECIMAL(5,2) GENERATED ALWAYS AS (
        CASE WHEN balls > 0 THEN (runs * 100.0 / balls) ELSE 0 END
    ) STORED,
    dismissal    VARCHAR(50),           -- e.g., 'bowled', 'caught', 'run-out', 'not-out'
    fielder_id   INT,                    -- player who made the dismissal (if caught/run-out)
    bowler_id    INT,                    -- bowler who took the wicket
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id)  REFERENCES matches(id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (team_id)   REFERENCES teams(id),
    FOREIGN KEY (fielder_id) REFERENCES players(id),
    FOREIGN KEY (bowler_id)  REFERENCES players(id),
    UNIQUE KEY uk_match_player (match_id, player_id)
);

-- ------------------------------------------------------------
-- Bowling Stats Table (per innings per player)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bowling_stats (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    match_id         INT NOT NULL,
    player_id        INT NOT NULL,
    team_id          INT NOT NULL,
    overs            DECIMAL(3,1) NOT NULL DEFAULT 0,    -- e.g., 4.2
    maidens          TINYINT UNSIGNED NOT NULL DEFAULT 0,
    runs_conceded    SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    wickets          TINYINT UNSIGNED NOT NULL DEFAULT 0,
    economy          DECIMAL(5,2) GENERATED ALWAYS AS (
        CASE WHEN overs > 0 THEN (runs_conceded / overs) ELSE 0 END
    ) STORED,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id)  REFERENCES matches(id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (team_id)   REFERENCES teams(id),
    UNIQUE KEY uk_match_player_bowl (match_id, player_id)
);

-- ------------------------------------------------------------
-- Fielding Stats Table
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fielding_stats (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    match_id     INT NOT NULL,
    player_id    INT NOT NULL,
    team_id      INT NOT NULL,
    catches      TINYINT UNSIGNED NOT NULL DEFAULT 0,
    stumpings    TINYINT UNSIGNED NOT NULL DEFAULT 0,
    run_outs     TINYINT UNSIGNED NOT NULL DEFAULT 0,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id)  REFERENCES matches(id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (team_id)   REFERENCES teams(id),
    UNIQUE KEY uk_match_player_field (match_id, player_id)
);

-- ------------------------------------------------------------
-- Series / Tournaments Table
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS series (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    short_name    VARCHAR(20),             -- e.g., 'T20I', 'IPL-2024'
    type          ENUM('T20', 'ODI', 'TEST', 'T20I', 'ODI-I', 'TEST-I', 'OTHER') NOT NULL,
    country       VARCHAR(50),
    start_date    DATE,
    end_date      DATE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_name (name)
);

-- ------------------------------------------------------------
-- Match-Series Bridge Table (many-to-many)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS match_series (
    match_id  INT,
    series_id INT,
    PRIMARY KEY (match_id, series_id),
    FOREIGN KEY (match_id)  REFERENCES matches(id) ON DELETE CASCADE,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Standings Table (for tournament/group stage results)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS standings (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    series_id   INT NOT NULL,
    team_id     INT NOT NULL,
    matches_played TINYINT UNSIGNED DEFAULT 0,
    wins        TINYINT UNSIGNED DEFAULT 0,
    losses      TINYINT UNSIGNED DEFAULT 0,
    ties        TINYINT UNSIGNED DEFAULT 0,
    no_results  TINYINT UNSIGNED DEFAULT 0,
    points      DECIMAL(5,2) DEFAULT 0,
    net_rr       DECIMAL(5,3) DEFAULT 0,     -- Net Run Rate
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id)   REFERENCES teams(id),
    UNIQUE KEY uk_series_team (series_id, team_id)
);
