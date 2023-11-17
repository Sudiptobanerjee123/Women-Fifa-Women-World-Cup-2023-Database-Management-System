-- Create a database named Player_Demo
DROP DATABASE IF EXISTS Player_Demo;
CREATE DATABASE Player_Demo;
USE Player_Demo;

-- Team Table
CREATE TABLE Team (
    TeamID varchar(20) PRIMARY KEY,
    TeamName varchar(20),
    Country varchar(20),
    Coach varchar(20),
    Formation varchar(20),
    FIFA_Ranking varchar(20),
    Matches_played varchar(20)
);

-- Insert data into the Team table
INSERT INTO Team (TeamID, TeamName, Country, Coach, Formation, FIFA_Ranking, Matches_played)
VALUES
    ('SWI', 'Switzerland', 'Switzerland', 'Coach1', '4-4-2', '5', '3'),
    -- ... (inserted data for other teams)
    ('KOR', 'Korea Republic', 'Korea', 'Coach32', '4-4-2', '18', '3');

-- Drop the Team table (it is later recreated, not necessary to keep it)
DROP TABLE Team;

-- Select all records from the Team table
SELECT * FROM Team;

-- Player Table
CREATE TABLE Player (
    PlayerID varchar(20) PRIMARY KEY,
    FirstName varchar(20),
    LastName varchar(20),
    TeamID varchar(20),
    Positions varchar(20),
    DateOfBirth varchar(20),
    Nationality varchar(20),
    JerseyNumber varchar(20),
    Height varchar(20),
    Weight varchar(20),
    FOREIGN KEY (TeamID) REFERENCES Team (TeamID)
);

-- Drop the Player table (it is later recreated, not necessary to keep it)
DROP TABLE Player;

-- Insert data into the Player table
INSERT INTO Player (PlayerID, FirstName, LastName, TeamID, Positions, DateOfBirth, Nationality, JerseyNumber, Height, Weight)
VALUES
    ('SWI-1', 'Eva', 'Müller', 'SWI', 'Forward', '1993-05-12', 'Swiss', '9', '165', '60'),
    -- ... (inserted data for other players)
    ('JPN-11', 'Yumi', 'Nakajima', 'JPN', 'Goalkeeper', '1989-10-15', 'Japanese', '23', '183', '76');

-- Drop the Player table (it is later recreated, not necessary to keep it)
DROP TABLE Player;

-- Venue Table
CREATE TABLE Venue (
    VenueID varchar(20) PRIMARY KEY,
    VenueName varchar(20),
    City varchar(20),
    Capacity varchar(20)
);

-- Insert data into the Venue table
INSERT INTO Venue (VenueID, VenueName, City, Capacity)
VALUES
    ('VEN-1', 'Sydney Stadium', 'Sydney', '45000'),
    -- ... (inserted data for other venues)
    ('VEN-10', 'Hamilton Park', 'Hamilton', '35000');

-- Matches Table
CREATE TABLE Matches (
    MatchesID varchar(20) PRIMARY KEY,
    MatchesDate varchar(20),
    Location varchar(20),
    TeamID1 varchar(20),
    TeamID2 varchar(20),
    Result varchar(7),
    VenueID varchar(20),
    FOREIGN KEY (TeamID1) REFERENCES Team (TeamID),
    FOREIGN KEY (TeamID2) REFERENCES Team (TeamID),
    FOREIGN KEY (VenueID) REFERENCES Venue (VenueID)
);

-- Select all records from the Matches table
SELECT * FROM Matches;

-- Insert data into the Matches table
INSERT INTO Matches (MatchesID, MatchesDate, Location, TeamID1, TeamID2, Result, VenueID)
VALUES
    ('MCH-1', '2023-10-20', 'Sydney', 'SWI', 'NOR', '2-1', 'VEN-1'),
    -- ... (inserted data for other matches)
    ('MCH-16', '2023-11-04', 'Perth', 'ENG', 'DEN', '1-1', 'VEN-6');

-- Venue Table (mistakenly created again, should be dropped)
DROP TABLE Venue;

-- Select all records from the Venue table
SELECT * FROM Venue;

-- Goal Table
CREATE TABLE Goal (
    GoalID varchar(20) PRIMARY KEY,
    MatchesID varchar(20),
    PlayerID varchar(20),
    FOREIGN KEY (MatchesID) REFERENCES Matches (MatchesID),
    FOREIGN KEY (PlayerID) REFERENCES Player (PlayerID)
);

-- Insert data into the Goal table
INSERT INTO Goal (GoalID, MatchesID, PlayerID)
VALUES
    ('G-1', 'MCH-1', 'SWI-1'),
    -- ... (inserted data for other goals)
    ('G-30', 'MCH-6', 'NGA-9');

-- Fixture Table
CREATE TABLE Fixture (
    FixtureID varchar(20) PRIMARY KEY,
    MatchesID varchar(20),
    VenueID varchar(20),
    FOREIGN KEY (MatchesID) REFERENCES Matches (MatchesID),
    FOREIGN KEY (VenueID) REFERENCES Venue (VenueID)
);

-- Insert data into the Fixture table
INSERT INTO Fixture (FixtureID, MatchesID, VenueID)
VALUES
    ('F-1', 'MCH-1', 'VEN-1'),
    -- ... (inserted data for other fixtures)
    ('F-16', 'MCH-6', 'VEN-6');

-- Select all records from the Fixture table
SELECT * FROM Fixture;

-- Standings Table
CREATE TABLE Standings (
    StandingsID INT AUTO_INCREMENT PRIMARY KEY,
    TeamID varchar(20),
    Points INT,
    Wins INT,
    Draws INT,
    Losses INT,
    GoalsFor INT,
    GoalsAgainst INT,
    FOREIGN KEY (TeamID) REFERENCES Team (TeamID)
);

-- Insert data into the Standings table
INSERT INTO Standings (TeamID, Points, Wins, Draws, Losses, GoalsFor, GoalsAgainst)
VALUES
    ('SWI', 7, 2, 1, 0, 5, 2),
    -- ... (inserted data for other teams)
    ('KOR', 1, 0, 1, 2, 2, 5);

-- Select all records from the Standings table
SELECT * FROM Standings;


-- Advanced Queries --

-- Count the total number of Goals using Window Function --
SELECT
            t.TeamName,
            COUNT(g.GoalID) AS TotalGoals
        FROM
            Team t
        JOIN
            Player p ON t.TeamID = p.TeamID
        JOIN
            Goal g ON p.PlayerID = g.PlayerID
        GROUP BY
            t.TeamName
        ORDER BY
            TotalGoals DESC;


-- Display the cummulative points and TeamRank --
SELECT
            TeamID,
            Points,
            RANK() OVER (ORDER BY Points DESC) AS TeamRank
        FROM
            Standing;

-- Display the tean name, MatchDate and the RunningTotal goals --

SELECT
            TeamID,
            MatchesDate,
            SUM(GoalsFor) OVER (PARTITION BY TeamID ORDER BY MatchesDate) AS RunningTotalGoals
        FROM (
            SELECT
                m.MatchesDate,
                m.TeamID1 AS TeamID,
                COUNT(g.GoalID) AS GoalsFor
            FROM
        Matches m
        LEFT JOIN
            Goal g ON m.MatchesID = g.MatchesID
        GROUP BY
            m.MatchesDate, m.TeamID1

        UNION ALL

        SELECT
            m.MatchesDate,
            m.TeamID2 AS TeamID,
            COUNT(g.GoalID) AS GoalsFor
        FROM
            Matches m
        LEFT JOIN
            Goal g ON m.MatchesID = g.MatchesID
        GROUP BY
            m.MatchesDate, m.TeamID2
        ) AS combined_data;

