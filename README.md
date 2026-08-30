# 🏏 Cricket Database — MySQL Project

A comprehensive cricket statistics database built with **MySQL 8.0**, covering **IPL** (2008–2024) and **International Cricket** (T20 World Cup, ODI World Cup, WTC, Asia Cup).

> Perfect for learning SQL through real-world cricket data. Run it in a Docker container in 30 seconds.

---

## 📁 Project Structure

```
cricket-sql-project/
├── docker-compose.yml          # MySQL 8.0 container setup
├── README.md                  # This file
│
└── sql/
    ├── 01_schema.sql         # Database schema (9 tables)
    ├── 02_seed_data.sql      # Teams & matches seed data
    ├── 03_seed_players.sql   # 79 players (IPL + International)
    ├── 04_seed_stats.sql     # Batting & bowling performance data
    ├── 05_seed_stats_rest.sql # Fielding, series, standings
    │
    └── queries/
        ├── 01_batting_stats.sql         # Batting analysis queries
        ├── 02_bowling_stats.sql         # Bowling analysis queries
        ├── 03_team_tournament_stats.sql  # Team & tournament analysis
        └── 04_player_comparisons.sql    # Advanced comparisons
```

---

## 🚀 Quick Start

### 1. Start MySQL (Docker)

```bash
# Start the container
docker compose up -d

# Wait ~25 seconds, then verify it's running
docker exec cricket-mysql mysqladmin ping -h localhost
```

**MySQL Credentials:**
- Host: `localhost:3306`
- User: `root`
- Password: `cricket123`
- Database: `cricket_db`

### 2. Connect & Explore

```bash
# Quick connect
docker exec -it cricket-mysql mysql -uroot -pcricket123 cricket_db

# Run a sample query
docker exec -i cricket-mysql mysql -uroot -pcricket123 cricket_db \
  < sql/queries/01_batting_stats.sql

# Run bowling analysis
docker exec -i cricket-mysql mysql -uroot -pcricket123 cricket_db \
  < sql/queries/02_bowling_stats.sql
```

### 3. Load Remaining Data (first-time only)

```bash
docker exec -i cricket-mysql mysql -uroot -pcricket123 cricket_db \
  < sql/05_seed_stats_rest.sql
```

> The first 4 SQL files (`01_schema.sql` → `04_seed_stats.sql`) are auto-loaded by Docker on first container start. The 5th file (`05_seed_stats_rest.sql`) covers the bowling/fielding/series data not in the main auto-load. Run it once after first start.

### 4. Stop

```bash
docker compose down
```

---

## 🗄️ Database Schema

```
teams ──────────┐
players ────────┼──── matches ────── batting_stats
batting_stats ──┤                   bowling_stats
bowling_stats ──┤                   fielding_stats
fielding_stats ─┤
                └── series ─── match_series
                            standings
```

| Table | Rows | Description |
|---|---|---|
| `teams` | 20 | IPL franchises + 10 international teams |
| `players` | 79 | IPL players + international stars |
| `matches` | 36 | IPL + ICC international matches |
| `batting_stats` | 157 | Individual innings records |
| `bowling_stats` | 86 | Bowling spell records |
| `fielding_stats` | 25 | Catches, stumpings, run-outs |
| `series` | 13 | Tournaments (IPL 2008–2024) |
| `standings` | 10 | IPL 2024 points table |
| `match_series` | 36 | Bridge table |

---

## 📊 Sample Query Results

### Top Run Scorers

| Player | Team | Matches | Runs | Avg | SR |
|---|---|---|---|---|---|
| MS Dhoni | CSK | 10 | 791 | 79.10 | 144.70 |
| Aiden Markram | SRH | 10 | 776 | 77.60 | 140.63 |
| Rohit Sharma | MI | 10 | 769 | 76.90 | 144.22 |
| Virat Kohli | RCB | 9 | 597 | 66.33 | 138.07 |
| Shreyas Iyer | KKR | 8 | 567 | 70.88 | 139.05 |

### Best Strike Rates (min 50 balls)

| Player | Team | Runs | Balls | SR |
|---|---|---|---|---|
| MS Dhoni | CSK | 791 | 544 | 145.40 |
| Suryakumar Yadav | MI | 81 | 56 | 144.64 |
| Rohit Sharma | MI | 769 | 532 | 144.55 |

### Top Wicket Takers

| Player | Team | Matches | Wickets | Avg Economy |
|---|---|---|---|---|
| Jasprit Bumrah | MI | 8 | 23 | 7.00 |
| Bhuvneshwar Kumar | SRH | 8 | 22 | 7.38 |
| Rashid Khan | GT | 8 | 21 | 7.14 |

---

## 🔍 Example Queries to Try

```sql
-- Who scored the most centuries?
SELECT full_name, team, COUNT(*) AS centuries
FROM batting_stats
JOIN players ON batting_stats.player_id = players.id
WHERE runs >= 100
GROUP BY player_id, full_name, team
ORDER BY centuries DESC;

-- Best economy (min 4 matches)
SELECT p.full_name, t.short_name, ROUND(AVG(economy), 2) AS avg_economy
FROM bowling_stats b
JOIN players p ON b.player_id = p.id
JOIN teams t ON b.team_id = t.id
GROUP BY player_id, p.full_name, t.short_name
HAVING COUNT(*) >= 4
ORDER BY avg_economy;

-- IPL 2024 Points Table
SELECT t.short_name, s.matches_played, s.wins, s.points, s.net_rr
FROM standings s
JOIN teams t ON s.team_id = t.id
JOIN series sr ON s.series_id = sr.id
WHERE sr.short_name = 'IPL-2024'
ORDER BY s.points DESC;

-- Player head-to-head comparison
SELECT p.full_name, SUM(b.runs) AS runs, SUM(b.wickets) AS wickets
FROM players p
LEFT JOIN batting_stats b ON p.id = b.player_id
WHERE p.full_name IN ('Rohit Sharma', 'Virat Kohli')
GROUP BY p.id, p.full_name;
```

---

## 🛠️ Tools & Technologies

- **Database:** MySQL 8.0 (via Docker)
- **Container:** Docker Compose
- **Queries:** MySQL 8.0 compatible SQL
- **Visualization:** Connect to any MySQL client (MySQL Workbench, DBeaver, DataGrip)

### Connect with MySQL Workbench
```
Host: 127.0.0.1
Port: 3306
User: root
Password: cricket123
Database: cricket_db
```

---

## 📝 Adding More Data

1. Add teams to `02_seed_data.sql`
2. Add players to `03_seed_players.sql`
3. Add match results to `02_seed_data.sql`
4. Add batting/bowling/fielding to `04_seed_stats.sql`
5. Rebuild: `docker compose down -v && docker compose up -d`

---

## 📚 Learn SQL Through Cricket

This project covers these SQL concepts:

| Concept | Examples |
|---|---|
| `JOIN` (INNER, LEFT) | Player stats via team join |
| `GROUP BY` + Aggregates | Team totals, averages, counts |
| `HAVING` | Filter aggregated groups |
| `ORDER BY` + `LIMIT` | Top scorers, best economy |
| `WITH` (CTE) | Recent form, format-specific stats |
| `CASE` statements | Conditional aggregations |
| Generated columns | `strike_rate`, `economy` auto-calculated |
| Foreign keys | Match → Team, Player → Team relationships |
| `ENUM` types | Match type (T20/ODI/TEST) |
| `CHECK` constraints | Prevent invalid data |

---

## 📄 License

MIT — free to use, modify, and learn from.
