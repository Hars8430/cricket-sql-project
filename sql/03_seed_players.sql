-- ============================================================
-- Players Seed Data — IPL + International Stars
-- ============================================================

-- ------------------------------------------------------------
-- Indian Players (IPL + International)
-- ------------------------------------------------------------
INSERT IGNORE INTO players (first_name, last_name, full_name, country, date_of_birth, role, batting_style, bowling_style, team_id, is_international) VALUES
-- Mumbai Indians (MI)
('Rohit', 'Sharma', 'Rohit Sharma', 'India', '1987-04-30', 'batsman', 'right-handed', NULL, 1, TRUE),
('Hardik', 'Pandya', 'Hardik Pandya', 'India', '1993-10-11', 'all-rounder', 'right-handed', 'fast-medium', 1, TRUE),
('Jasprit', 'Bumrah', 'Jasprit Bumrah', 'India', '1993-12-06', 'bowler', 'right-handed', 'fast', 1, TRUE),
('Suryakumar', 'Yadav', 'Suryakumar Yadav', 'India', '1990-09-14', 'batsman', 'right-handed', NULL, 1, TRUE),
('Ishan', 'Kishan', 'Ishan Kishan', 'India', '1998-07-18', 'wicket-keeper', 'left-handed', NULL, 1, TRUE),
('Tilak', 'Varma', 'Tilak Varma', 'India', '2002-11-08', 'batsman', 'left-handed', NULL, 1, FALSE),
('Tim', 'David', 'Tim David', 'Singapore', '1996-03-16', 'all-rounder', 'right-handed', NULL, 1, FALSE),

-- Chennai Super Kings (CSK)
('MS', 'Dhoni', 'MS Dhoni', 'India', '1981-07-07', 'wicket-keeper', 'right-handed', NULL, 2, TRUE),
('Ruturaj', 'Gaikwad', 'Ruturaj Gaikwad', 'India', '1997-01-31', 'batsman', 'right-handed', NULL, 2, TRUE),
('Ravindra', 'Jadeja', 'Ravindra Jadeja', 'India', '1988-12-06', 'all-rounder', 'left-handed', 'left-arm', 2, TRUE),
('Deepak', 'Chahar', 'Deepak Chahar', 'India', '1992-08-07', 'bowler', 'right-handed', 'fast-medium', 2, TRUE),
('Moeen', 'Ali', 'Moeen Ali', 'England', '1987-06-18', 'all-rounder', 'left-handed', 'off-spin', 2, TRUE),
('Matheesha', 'Pathirana', 'Matheesha Pathirana', 'Sri Lanka', '2002-12-18', 'bowler', 'right-handed', 'fast', 2, TRUE),

-- Royal Challengers Bangalore (RCB)
('Virat', 'Kohli', 'Virat Kohli', 'India', '1988-11-05', 'batsman', 'right-handed', NULL, 3, TRUE),
('Faf', 'du Plessis', 'Faf du Plessis', 'South Africa', '1984-07-13', 'batsman', 'right-handed', NULL, 3, TRUE),
('Glenn', 'Maxwell', 'Glenn Maxwell', 'Australia', '1988-10-14', 'all-rounder', 'right-handed', 'off-spin', 3, TRUE),
('Mohammed', 'Siraj', 'Mohammed Siraj', 'India', '1994-03-13', 'bowler', 'right-handed', 'fast', 3, TRUE),
('Dinesh', 'Karthik', 'Dinesh Karthik', 'India', '1985-06-01', 'wicket-keeper', 'right-handed', NULL, 3, TRUE),
('Rajat', 'Patidar', 'Rajat Patidar', 'India', '1993-06-12', 'batsman', 'right-handed', NULL, 3, FALSE),

-- Kolkata Knight Riders (KKR)
('Shreyas', 'Iyer', 'Shreyas Iyer', 'India', '1994-12-06', 'batsman', 'right-handed', NULL, 4, TRUE),
('Andre', 'Russell', 'Andre Russell', 'West Indies', '1988-04-29', 'all-rounder', 'right-handed', 'fast', 4, TRUE),
('Sunil', 'Narine', 'Sunil Narine', 'West Indies', '1988-05-26', 'all-rounder', 'left-handed', 'off-spin', 4, TRUE),
('Varun', 'Chakravarthy', 'Varun Chakravarthy', 'India', '1991-08-29', 'bowler', 'right-handed', 'leg-spin', 4, TRUE),
('Venkatesh', 'Iyer', 'Venkatesh Iyer', 'India', '1994-12-25', 'all-rounder', 'left-handed', 'fast-medium', 4, FALSE),
('Rinku', 'Singh', 'Rinku Singh', 'India', '1997-10-12', 'batsman', 'left-handed', NULL, 4, FALSE),

-- Sunrisers Hyderabad (SRH)
('Aiden', 'Markram', 'Aiden Markram', 'South Africa', '1994-10-31', 'batsman', 'right-handed', 'off-spin', 5, TRUE),
('Heinrich', 'Klaasen', 'Heinrich Klaasen', 'South Africa', '1991-07-30', 'wicket-keeper', 'right-handed', NULL, 5, TRUE),
('Bhuvneshwar', 'Kumar', 'Bhuvneshwar Kumar', 'India', '1990-02-05', 'bowler', 'right-handed', 'fast-medium', 5, TRUE),
('Mayank', 'Agarwal', 'Mayank Agarwal', 'India', '1991-02-16', 'batsman', 'right-handed', NULL, 5, TRUE),
('Abhishek', 'Sharma', 'Abhishek Sharma', 'India', '2000-09-04', 'all-rounder', 'left-handed', 'left-arm', 5, FALSE),
('Travis', 'Head', 'Travis Head', 'Australia', '1993-12-29', 'batsman', 'left-handed', 'off-spin', 5, TRUE),

-- Delhi Capitals (DC)
('Rishabh', 'Pant', 'Rishabh Pant', 'India', '1997-10-04', 'wicket-keeper', 'left-handed', NULL, 6, TRUE),
('David', 'Warner', 'David Warner', 'Australia', '1986-10-27', 'batsman', 'left-handed', NULL, 6, TRUE),
('Axar', 'Patel', 'Axar Patel', 'India', '1994-01-20', 'all-rounder', 'left-handed', 'left-arm', 6, TRUE),
('Kuldeep', 'Yadav', 'Kuldeep Yadav', 'India', '1994-12-14', 'bowler', 'left-handed', 'leg-spin', 6, TRUE),
('Anrich', 'Nortje', 'Anrich Nortje', 'South Africa', '1993-11-16', 'bowler', 'right-handed', 'fast', 6, TRUE),
('Tristan', 'Stubbs', 'Tristan Stubbs', 'South Africa', '2000-08-14', 'batsman', 'right-handed', NULL, 6, FALSE),

-- Punjab Kings (PBKS)
('Shikhar', 'Dhawan', 'Shikhar Dhawan', 'India', '1985-12-05', 'batsman', 'left-handed', NULL, 7, TRUE),
('Liam', 'Livingstone', 'Liam Livingstone', 'England', '1993-08-04', 'all-rounder', 'right-handed', 'leg-spin', 7, TRUE),
('Kagiso', 'Rabada', 'Kagiso Rabada', 'South Africa', '1995-05-25', 'bowler', 'left-handed', 'fast', 7, TRUE),
('Sam', 'Curran', 'Sam Curran', 'England', '1998-06-03', 'all-rounder', 'left-handed', 'fast-medium', 7, TRUE),
('Jitesh', 'Sharma', 'Jitesh Sharma', 'India', '1993-10-22', 'wicket-keeper', 'right-handed', NULL, 7, FALSE),
('Arshdeep', 'Singh', 'Arshdeep Singh', 'India', '1999-02-05', 'bowler', 'left-handed', 'fast-medium', 7, TRUE),

-- Rajasthan Royals (RR)
('Sanju', 'Samson', 'Sanju Samson', 'India', '1994-11-11', 'wicket-keeper', 'right-handed', NULL, 8, TRUE),
('Jos', 'Buttler', 'Jos Buttler', 'England', '1990-09-08', 'batsman', 'right-handed', NULL, 8, TRUE),
('Yashasvi', 'Jaiswal', 'Yashasvi Jaiswal', 'India', '2001-12-28', 'batsman', 'left-handed', NULL, 8, TRUE),
('Yuzvendra', 'Chahal', 'Yuzvendra Chahal', 'India', '1990-07-23', 'bowler', 'right-handed', 'leg-spin', 8, TRUE),
('Trent', 'Boult', 'Trent Boult', 'New Zealand', '1989-07-22', 'bowler', 'right-handed', 'fast', 8, TRUE),
('Riyan', 'Parag', 'Riyan Parag', 'India', '2001-11-10', 'all-rounder', 'right-handed', 'leg-spin', 8, FALSE),

-- Gujarat Titans (GT)
('Shubman', 'Gill', 'Shubman Gill', 'India', '1999-09-08', 'batsman', 'right-handed', NULL, 9, TRUE),
('Rashid', 'Khan', 'Rashid Khan', 'Afghanistan', '1998-09-20', 'bowler', 'right-handed', 'leg-spin', 9, TRUE),
('David', 'Miller', 'David Miller', 'South Africa', '1989-06-10', 'batsman', 'left-handed', NULL, 9, TRUE),
('Mohammed', 'Shami', 'Mohammed Shami', 'India', '1990-09-03', 'bowler', 'right-handed', 'fast', 9, TRUE),
('Rahul', 'Tewatia', 'Rahul Tewatia', 'India', '1993-05-20', 'all-rounder', 'right-handed', 'leg-spin', 9, FALSE),
('Sai', 'Sudharsan', 'Sai Sudharsan', 'India', '2001-10-15', 'batsman', 'left-handed', NULL, 9, FALSE),

-- Lucknow Super Giants (LSG)
('KL', 'Rahul', 'KL Rahul', 'India', '1992-04-18', 'wicket-keeper', 'right-handed', NULL, 10, TRUE),
('Quinton', 'de Kock', 'Quinton de Kock', 'South Africa', '1992-12-17', 'wicket-keeper', 'left-handed', NULL, 10, TRUE),
('Marcus', 'Stoinis', 'Marcus Stoinis', 'Australia', '1989-08-16', 'all-rounder', 'right-handed', 'fast-medium', 10, TRUE),
('Ravi', 'Bishnoi', 'Ravi Bishnoi', 'India', '2000-09-05', 'bowler', 'right-handed', 'leg-spin', 10, TRUE),
('Ayush', 'Badoni', 'Ayush Badoni', 'India', '1999-12-03', 'all-rounder', 'right-handed', 'off-spin', 10, FALSE),
('Nicholas', 'Pooran', 'Nicholas Pooran', 'West Indies', '1995-10-02', 'wicket-keeper', 'left-handed', NULL, 10, TRUE),

-- Additional International Players (not in IPL)
('Kane', 'Williamson', 'Kane Williamson', 'New Zealand', '1990-08-08', 'batsman', 'right-handed', NULL, NULL, TRUE),
('Joe', 'Root', 'Joe Root', 'England', '1990-12-30', 'batsman', 'right-handed', 'off-spin', NULL, TRUE),
('Steve', 'Smith', 'Steve Smith', 'Australia', '1989-06-02', 'batsman', 'right-handed', 'leg-spin', NULL, TRUE),
('Babar', 'Azam', 'Babar Azam', 'Pakistan', '1994-10-15', 'batsman', 'right-handed', NULL, NULL, TRUE),
('Shaheen', 'Afridi', 'Shaheen Afridi', 'Pakistan', '2000-04-06', 'bowler', 'left-handed', 'fast', NULL, TRUE),
('Ben', 'Stokes', 'Ben Stokes', 'England', '1991-06-04', 'all-rounder', 'left-handed', 'fast-medium', NULL, TRUE),
('Pat', 'Cummins', 'Pat Cummins', 'Australia', '1993-05-08', 'bowler', 'right-handed', 'fast', NULL, TRUE),
('Mitchell', 'Starc', 'Mitchell Starc', 'Australia', '1990-01-30', 'bowler', 'left-handed', 'fast', NULL, TRUE),
('Rashid', 'Khan', 'Rashid Khan', 'Afghanistan', '1998-09-20', 'bowler', 'right-handed', 'leg-spin', NULL, TRUE),
('Jasprit', 'Bumrah', 'Jasprit Bumrah', 'India', '1993-12-06', 'bowler', 'right-handed', 'fast', NULL, TRUE),
('Mohammed', 'Siraj', 'Mohammed Siraj', 'India', '1994-03-13', 'bowler', 'right-handed', 'fast', NULL, TRUE),
('Kagiso', 'Rabada', 'Kagiso Rabada', 'South Africa', '1995-05-25', 'bowler', 'left-handed', 'fast', NULL, TRUE),
('Trent', 'Boult', 'Trent Boult', 'New Zealand', '1989-07-22', 'bowler', 'right-handed', 'fast', NULL, TRUE),
('Muttiah', 'Muralitharan', 'Muttiah Muralitharan', 'Sri Lanka', '1972-04-17', 'bowler', 'right-handed', 'off-spin', NULL, TRUE),
('Shane', 'Warne', 'Shane Warne', 'Australia', '1969-09-13', 'bowler', 'right-handed', 'leg-spin', NULL, TRUE),
('Wasim', 'Akram', 'Wasim Akram', 'Pakistan', '1966-06-03', 'bowler', 'left-handed', 'fast', NULL, TRUE),
('Glenn', 'McGrath', 'Glenn McGrath', 'Australia', '1970-02-09', 'bowler', 'right-handed', 'fast', NULL, TRUE),
('Courtney', 'Walsh', 'Courtney Walsh', 'West Indies', '1962-10-30', 'bowler', 'right-handed', 'fast', NULL, TRUE);