-- ============================================================
-- Cricket Database Seed Data
-- MySQL 8.0 — populated with IPL + International cricket data
-- ============================================================

-- ------------------------------------------------------------
-- Teams: IPL + International
-- ------------------------------------------------------------
INSERT IGNORE INTO teams (name, short_name, country, founded, home_ground) VALUES
-- IPL Teams
('Mumbai Indians', 'MI', 'India', 2008, 'Wankhede Stadium'),
('Chennai Super Kings', 'CSK', 'India', 2008, 'M. A. Chidambaram Stadium'),
('Royal Challengers Bangalore', 'RCB', 'India', 2008, 'M. Chinnaswamy Stadium'),
('Kolkata Knight Riders', 'KKR', 'India', 2008, 'Eden Gardens'),
('Sunrisers Hyderabad', 'SRH', 'India', 2013, 'Rajiv Gandhi International Stadium'),
('Delhi Capitals', 'DC', 'India', 2008, 'Arun Jaitley Stadium'),
('Punjab Kings', 'PBK', 'India', 2008, 'PCA Stadium'),
('Rajasthan Royals', 'RR', 'India', 2008, 'Sawai Mansingh Stadium'),
('Gujarat Titans', 'GT', 'India', 2022, 'Narendra Modi Stadium'),
('Lucknow Super Giants', 'LSG', 'India', 2022, 'BRSAB Cricket Stadium'),

-- International Teams
('India', 'IND', 'India', NULL, NULL),
('Australia', 'AUS', 'Australia', NULL, NULL),
('England', 'ENG', 'England', NULL, NULL),
('South Africa', 'SA', 'South Africa', NULL, NULL),
('New Zealand', 'NZ', 'New Zealand', NULL, NULL),
('Pakistan', 'PAK', 'Pakistan', NULL, NULL),
('Sri Lanka', 'SL', 'Sri Lanka', NULL, NULL),
('West Indies', 'WI', 'West Indies', NULL, NULL),
('Afghanistan', 'AFG', 'Afghanistan', NULL, NULL),
('Bangladesh', 'BD', 'Bangladesh', NULL, NULL);

-- ------------------------------------------------------------
-- IPL Match Results (2008-2024)
-- ------------------------------------------------------------
INSERT IGNORE INTO matches (match_date, team1_id, team2_id, venue, city, country, match_type, toss_winner_id, toss_decision, winner_id, man_of_the_match_id, team1_score, team2_score, target, result) VALUES
-- 2024 IPL Matches
('2024-05-19', 9, 10, 'Narendra Modi Stadium', 'Ahmedabad', 'India', 'T20', 9, 'bat', 9, NULL, '185/4', '178/8', 186, 'normal'),
('2024-05-12', 7, 9, 'PCA Stadium', 'Mohali', 'India', 'T20', 7, 'field', 9, NULL, '162/5', '158/7', NULL, 'normal'),
('2024-05-05', 1, 2, 'Wankhede Stadium', 'Mumbai', 'India', 'T20', 1, 'bowl', 1, NULL, '202/5', '199/6', NULL, 'normal'),

-- 2023 IPL Matches
('2023-05-21', 1, 3, 'M. Chinnaswamy Stadium', 'Bengaluru', 'India', 'T20', 1, 'bat', 3, NULL, '200/3', '198/5', NULL, 'normal'),
('2023-05-14', 4, 5, 'Eden Gardens', 'Kolkata', 'India', 'T20', 4, 'field', 5, NULL, '165/8', '166/4', NULL, 'normal'),
('2023-05-07', 6, 7, 'Arun Jaitley Stadium', 'Delhi', 'India', 'T20', 6, 'bat', 7, NULL, '170/6', '168/7', NULL, 'normal'),

-- 2022 IPL Matches
('2022-05-29', 8, 9, 'Narendra Modi Stadium', 'Ahmedabad', 'India', 'T20', 8, 'bowl', 9, NULL, '175/6', '176/4', NULL, 'normal'),
('2022-05-22', 4, 10, 'Eden Gardens', 'Kolkata', 'India', 'T20', 10, 'bat', 10, NULL, '180/5', '182/3', NULL, 'normal'),
('2022-05-15', 2, 6, 'Wankhede Stadium', 'Mumbai', 'India', 'T20', 2, 'field', 2, NULL, '195/4', '190/6', NULL, 'normal'),

-- 2021 IPL Matches
('2021-05-16', 1, 5, 'M. Chinnaswamy Stadium', 'Bengaluru', 'India', 'T20', 5, 'bat', 5, NULL, '170/6', '171/4', NULL, 'normal'),
('2021-05-09', 3, 7, 'PCA Stadium', 'Mohali', 'India', 'T20', 3, 'field', 7, NULL, '155/8', '156/5', NULL, 'normal'),
('2021-05-02', 2, 9, 'Wankhede Stadium', 'Mumbai', 'India', 'T20', 2, 'bowl', 9, NULL, '160/7', '161/5', NULL, 'normal'),

-- 2020 IPL Matches (UAE)
('2020-11-22', 1, 4, 'Sheikh Zayed Stadium', 'Abu Dhabi', 'UAE', 'T20', 1, 'bat', 4, NULL, '194/5', '191/6', NULL, 'normal'),
('2020-11-15', 5, 8, 'Dubai International Stadium', 'Dubai', 'UAE', 'T20', 5, 'bowl', 8, NULL, '165/6', '168/7', NULL, 'normal'),
('2020-11-08', 2, 6, 'Sharjah Cricket Stadium', 'Sharjah', 'UAE', 'T20', 2, 'field', 6, NULL, '155/8', '156/6', NULL, 'normal'),

-- 2019 IPL Matches
('2019-05-12', 1, 3, 'M. Chinnaswamy Stadium', 'Bengaluru', 'India', 'T20', 3, 'field', 1, NULL, '180/6', '181/4', NULL, 'normal'),
('2019-05-05', 5, 2, 'Rajiv Gandhi International Stadium', 'Hyderabad', 'India', 'T20', 2, 'bat', 2, NULL, '175/5', '174/6', NULL, 'normal'),
('2019-04-28', 6, 9, 'PCA Stadium', 'Mohali', 'India', 'T20', 9, 'bat', 9, NULL, '172/4', '171/5', NULL, 'normal'),

-- 2018 IPL Matches
('2018-05-20', 1, 5, 'M. Chinnaswamy Stadium', 'Bengaluru', 'India', 'T20', 1, 'bat', 5, NULL, '185/4', '184/6', NULL, 'normal'),
('2018-05-13', 4, 8, 'Eden Gardens', 'Kolkata', 'India', 'T20', 4, 'field', 8, NULL, '170/5', '172/4', NULL, 'normal'),
('2018-05-06', 3, 7, 'Sawai Mansingh Stadium', 'Jaipur', 'India', 'T20', 3, 'bowl', 7, NULL, '165/7', '166/5', NULL, 'normal'),

-- 2017 IPL Matches
('2017-05-21', 2, 6, 'Eden Gardens', 'Kolkata', 'India', 'T20', 6, 'bat', 6, NULL, '178/5', '177/6', NULL, 'normal'),
('2017-05-14', 9, 10, 'BRSAB Cricket Stadium', 'Lucknow', 'India', 'T20', 9, 'bowl', 10, NULL, '160/6', '161/4', NULL, 'normal'),
('2017-05-07', 3, 5, 'M. Chinnaswamy Stadium', 'Bengaluru', 'India', 'T20', 3, 'field', 5, NULL, '175/3', '176/4', NULL, 'normal'),

-- 2016 IPL Matches
('2016-05-29', 4, 1, 'Eden Gardens', 'Kolkata', 'India', 'T20', 4, 'bat', 1, NULL, '183/6', '182/7', NULL, 'normal'),
('2016-05-22', 5, 2, 'Rajiv Gandhi International Stadium', 'Hyderabad', 'India', 'T20', 5, 'field', 2, NULL, '170/5', '171/4', NULL, 'normal'),
('2016-05-15', 3, 6, 'Sawai Mansingh Stadium', 'Jaipur', 'India', 'T20', 3, 'bowl', 6, NULL, '158/5', '159/6', NULL, 'normal'),

-- 2015 IPL Matches
('2015-05-24', 1, 4, 'M. Chinnaswamy Stadium', 'Bengaluru', 'India', 'T20', 1, 'bat', 4, NULL, '175/5', '176/4', NULL, 'normal'),
('2015-05-17', 2, 5, 'Wankhede Stadium', 'Mumbai', 'India', 'T20', 5, 'bat', 2, NULL, '180/6', '181/4', NULL, 'normal'),
('2015-05-10', 3, 6, 'Sawai Mansingh Stadium', 'Jaipur', 'India', 'T20', 3, 'bowl', 6, NULL, '165/4', '166/5', NULL, 'normal'),

-- 2014 IPL Matches
('2014-05-25', 2, 4, 'Wankhede Stadium', 'Mumbai', 'India', 'T20', 2, 'field', 4, NULL, '168/5', '169/6', NULL, 'normal'),
('2014-05-18', 1, 3, 'M. Chinnaswamy Stadium', 'Bengaluru', 'India', 'T20', 3, 'bat', 1, NULL, '175/4', '176/5', NULL, 'normal'),
('2014-05-11', 5, 6, 'Rajiv Gandhi International Stadium', 'Hyderabad', 'India', 'T20', 5, 'field', 6, NULL, '160/5', '161/4', NULL, 'normal'),

-- 2013 IPL Matches (9 teams after CSK/RR suspension)
('2013-05-26', 7, 1, 'PCA Stadium', 'Mohali', 'India', 'T20', 1, 'bowl', 7, NULL, '158/6', '157/5', NULL, 'normal'),
('2013-05-19', 4, 2, 'Eden Gardens', 'Kolkata', 'India', 'T20', 2, 'field', 4, NULL, '162/5', '163/4', NULL, 'normal'),
('2013-05-12', 3, 5, 'Sawai Mansingh Stadium', 'Jaipur', 'India', 'T20', 5, 'bat', 5, NULL, '155/5', '156/4', NULL, 'normal');

-- ------------------------------------------------------------
-- International Matches (Recent ICC)
-- ------------------------------------------------------------
INSERT IGNORE INTO matches (match_date, team1_id, team2_id, venue, city, country, match_type, toss_winner_id, toss_decision, winner_id, man_of_the_match_id, team1_score, team2_score, target, result) VALUES
-- 2024 T20 World Cup Matches
('2024-06-09', 2, 4, 'Central Broward Stadium', 'Florida', 'USA', 'T20', 2, 'bat', 2, NULL, '159/7', '153/8', 160, 'normal'),
('2024-06-08', 5, 7, 'Darren Sammy National Stadium', 'St Lucia', 'West Indies', 'T20', 5, 'field', 7, NULL, '142/8', '141/9', 143, 'normal'),
('2024-06-07', 9, 10, 'Sir Vivian Richards Stadium', 'Antigua', 'West Indies', 'T20', 9, 'bat', 10, NULL, '189/5', '188/7', 190, 'normal'),

-- 2023 Asia Cup Matches
('2023-09-05', 1, 7, 'R. Premadasa Stadium', 'Colombo', 'Sri Lanka', 'T20', 1, 'field', 7, NULL, '172/6', '173/5', NULL, 'normal'),
('2023-09-03', 3, 5, 'R. Premadasa Stadium', 'Colombo', 'Sri Lanka', 'T20', 5, 'bat', 5, NULL, '185/4', '186/6', NULL, 'normal'),

-- 2023 World Test Championship Final
('2023-06-07', 2, 4, 'The Oval', 'London', 'England', 'TEST', 4, 'bat', 4, NULL, '469/8d', '381/9d', NULL, 'normal'),
('2023-06-09', 4, 2, 'The Oval', 'London', 'England', 'TEST', 2, 'bat', 2, NULL, '329/7d', '312/8d', NULL, 'normal'),

-- 2023 ODI World Cup Matches
('2023-10-08', 1, 3, 'Narendra Modi Stadium', 'Ahmedabad', 'India', 'ODI', 3, 'bat', 1, NULL, '350/8', '325/9', NULL, 'normal'),
('2023-10-15', 5, 2, 'Ekana Cricket Stadium', 'Lucknow', 'India', 'ODI', 2, 'field', 5, NULL, '280/9', '281/5', 282, 'normal'),
('2023-10-22', 4, 6, 'M. Chinnaswamy Stadium', 'Bengaluru', 'India', 'ODI', 4, 'field', 6, NULL, '240/8', '241/5', 242, 'normal'),

-- 2022 T20 World Cup Matches
('2022-10-23', 8, 9, 'Adelaide Oval', 'Adelaide', 'Australia', 'T20', 9, 'bat', 9, NULL, '172/6', '171/7', NULL, 'normal'),
('2022-10-27', 1, 5, 'Melbourne Cricket Ground', 'Melbourne', 'Australia', 'T20', 1, 'field', 5, NULL, '180/5', '181/4', NULL, 'normal'),

-- 2021 World Test Championship Final
('2021-06-23', 2, 4, 'Southampton', 'England', 'TEST', 4, 'bat', 2, NULL, '134 & 296', '217 & 123', NULL, 'normal'),
('2021-06-30', 4, 2, 'Southampton', 'England', 'TEST', 2, 'bat', 4, NULL, '321 & 258', '306 & 162', NULL, 'normal');