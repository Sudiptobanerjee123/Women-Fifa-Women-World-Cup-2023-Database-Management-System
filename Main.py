# Import necessary libraries and modules
from tkinter import Tk, Frame, Button, Label
import pymysql
from tkinter import *
import tkinter as tk
from Components import display_database_system

# Function to establish a connection to the MySQL database
def connection(database_name):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='Player_Demo',
    )
    return conn

# Function for the home page
def home_page(root):
    # Home Page Logic
    home_frame = Frame(root)
    home_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

    # Create Navbar for Home Page
    create_navbar_frame(root)

    # Add Home Page Content, e.g., Buttons
    label_home = Label(home_frame, text="Welcome to Fifa Women's World Cup 2023 Database", font=('Georgia', 45, 'bold'))
    label_home.grid(row=2, column=1, pady=60, padx=65)

    # Buttons to navigate to different pages
    player_button = Button(home_frame, text="Player Profile", command=player_page, width=30, padx=15, pady=10, font=('Helvetica', 16, 'bold'), border=10)
    player_button.grid(row=10, column=1)

    team_button = Button(home_frame, text="Team Information", command=team_page, width=30, padx=15, pady=10, font=('Helvetica', 16, 'bold'), border=10)
    team_button.grid(row=40, column=1)

    venue_button = Button(home_frame, text="Venue Details", command=venue_page, padx=15, width=30, pady=10, font=('Helvetica', 16, 'bold'), border=10)
    venue_button.grid(row=70, column=1)

    matches_button = Button(home_frame, text="Match Details", command=matches_page, padx=15, width=30, pady=10, font=('Helvetica', 16, 'bold'), border=10)
    matches_button.grid(row=100, column=1)

    goal_button = Button(home_frame, text="Goal Details", command=goal_page, padx=15, width=30, pady=10, font=('Helvetica', 16, 'bold'), border=10)
    goal_button.grid(row=130, column=1)

    fixture_button = Button(home_frame, text="Fixture Details", command=fixture_page, padx=15, width=30, pady=10, font=('Helvetica', 16, 'bold'), border=10)
    fixture_button.grid(row=170, column=1)

    standing_button = Button(home_frame, text="Standing Details", command=standing_page, padx=15, width=30, pady=10, font=('Helvetica', 16, 'bold'), border=10)
    standing_button.grid(row=180, column=1)

# Function to create the navbar frame
def create_navbar_frame(root):
    navbar_frame = Frame(root, bd=2, relief="solid", bg="#3498db")
    navbar_frame.grid(row=0, column=0, columnspan=13, sticky="nsew")

    label = Label(navbar_frame, text="Women Fifa World Cup 2023 ⚽️", font=('Georgia Bold', 32), bg="#3498db", fg="white")
    label.grid(padx=500, pady=20)
    navbar_frame.grid_rowconfigure(0, weight=1)
    navbar_frame.grid_columnconfigure(0, weight=1)

# Function to display the Venue Page
def venue_page():
    venue_columns = ["VenueID", "VenueName", "City", "Capacity"]
    venue_labels = ["Venue ID", "Venue Name", "City", "Capacity"]
    display_database_system("Player_Demo", "Venue", venue_columns, venue_labels, home_page)

# Function to display the Player Page
def player_page():
    player_columns = ["PlayerID", "FirstName", "LastName", "TeamID", "Positions",
                  "DateOfBirth", "Nationality", "JerseyNumber", "Height", "Weight"]

    player_labels = ["Player ID", "First Name", "Last Name", "Team ID", "Positions",
                 "Date of Birth", "Nationality", "Jersey Number", "Height", "Weight"]
    
    display_database_system("Player_Demo", "Player", player_columns, player_labels, home_page)

# Function to display the Team Page
def team_page():

    team_columns = ["ID", "Team Name", "Country", "Coach", "Formation", "FIFA Ranking", "Matches Played"]

    team_labels = ["ID", "Team Name", "Country", "Coach", "Formation", "FIFA Ranking", "Matches Played"]
    
    display_database_system("Player_Demo", "Team", team_columns, team_labels, home_page)

# Function to display the Matches Page
def matches_page():

    match_columns = ["MatchesID", "MatchesDate", "Location", "TeamID1", "TeamID2", "Result", "VenueID"]

    match_labels = ["MatchesID", "MatchesDate", "Location", "TeamID1", "TeamID2", "Result", "VenueID"]
    
    display_database_system("Player_Demo", "Matches", match_columns, match_labels, home_page)

# Function to display the Goal Page
def goal_page():

    goal_columns = ["GoalID", "MatchesID", "PlayerID"]

    goal_labels = ["GoalID", "MatchesID", "PlayerID"]
    
    display_database_system("Player_Demo", "Goal", goal_columns, goal_labels, home_page)

# Function to display the Fixture Page
def fixture_page():

    fixture_columns = ["FixtureID", "MatchesID", "Stage", "Venue"]

    fixture_labels = ["FixtureID", "MatchesID", "Stage", "Venue"]
    
    display_database_system("Player_Demo", "Fixture", fixture_columns, fixture_labels, home_page)

# Function to display the Standings Page
def standing_page():

    standing_columns = ["StandingID", "TeamID", "Wins", "Draws", "Losses","Points"]

    standing_labels = ["StandingID", "TeamID", "Wins", "Draws", "Losses","Points"]
    
    display_database_system("Player_Demo", "Standing", standing_columns, standing_labels, home_page)

# Main entry point of the program
if __name__ == "__main__":
    # Create the root window
    root = Tk()
    root.title("Women's Fifa World Cup 2023 Database System")
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+0+0' % (width, height))

    # Initial Home Page
    home_page(root)
    root.mainloop()
