# 🚀 Quick Start Guide

Get the cricket database running in **under 1 minute**.

## Step 1: Start MySQL

```bash
docker compose up -d
```

## Step 2: Wait for Database to Initialize

```bash
# This typically takes 25-30 seconds
docker exec cricket-mysql mysqladmin ping -h localhost
```

## Step 3: Load Additional Data

```bash
docker exec -i cricket-mysql mysql -uroot -pcricket123 cricket_db < sql/05_seed_stats_rest.sql
```

## Step 4: Run a Query

```bash
docker exec -i cricket-mysql mysql -uroot -pcricket123 cricket_db < sql/queries/01_batting_stats.sql
```

## Step 5: Open MySQL CLI

```bash
docker exec -it cricket-mysql mysql -uroot -pcricket123 cricket_db
```

## Step 6: Cleanup

```bash
# Stop and remove container
docker compose down

# Stop and remove container + data
docker compose down -v
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---|---|
| `Cannot connect to Docker daemon` | Make sure Docker Desktop is running |
| `Port 3306 already in use` | Stop the conflicting service, or change port in `docker-compose.yml` |
| `Access denied for user` | Password is `cricket123` |
| Tables not loaded | Run `docker logs cricket-mysql` to see init errors |
| `Unknown database 'cricket_db'` | Wait 30s after `up -d` for initialization to complete |

---

## 📊 Test It Works

After setup, run this single command to see your first insights:

```bash
docker exec -i cricket-mysql mysql -uroot -pcricket123 cricket_db -e "
SELECT p.full_name, t.short_name, SUM(b.runs) AS total_runs
FROM batting_stats b
JOIN players p ON b.player_id = p.id
JOIN teams t ON b.team_id = t.id
GROUP BY p.id, p.full_name, t.short_name
ORDER BY total_runs DESC LIMIT 10;
"
```

Expected output (something like):
```
MS Dhoni        CSK    791
Aiden Markram   SRH    776
Rohit Sharma    MI     769
Virat Kohli     RCB    597
...
```
