# Women's Fifa World Cup 2023 Database System

## Overview

This project implements a comprehensive database system for managing information related to the Women's Fifa World Cup 2023. The system provides a user-friendly graphical interface built using Tkinter and interacts with a MySQL database. The application is designed to handle various aspects of the tournament, including player profiles, team information, match details, goals, fixtures, and standings.

## Files

### Main.py

#### Functions

1. **`connection(database_name):`**
   - Establishes a connection to the MySQL database.

2. **`home_page(root):`**
   - Displays the home page, featuring a navigation bar with buttons for different sections of the database.

3. **`create_navbar_frame(root):`**
   - Creates the navigation bar at the top of the window, providing a consistent look and feel.

4. **`venue_page():`**
   - Displays venue information using the `display_database_system` function.

5. **`player_page():`**
   - Displays player information using the `display_database_system` function.

6. **`team_page():`**
   - Displays team information using the `display_database_system` function.

7. **`matches_page():`**
   - Displays match information using the `display_database_system` function.

8. **`goal_page():`**
   - Displays goal information using the `display_database_system` function.

9. **`fixture_page():`**
   - Displays fixture information using the `display_database_system` function.

10. **`standing_page():`**
    - Displays standing information using the `display_database_system` function.

11. **`main():`**
    - Initializes the Tkinter GUI, displaying the home page and initiating the main loop.

### Components.py

#### Functions

1. **`connection(database_name):`**
   - Establishes a connection to the MySQL database.

2. **`back_to_home(root, home_page_function):`**
   - Clears the current window and recreates the home page, providing seamless navigation.

3. **`display_database_system(database_name, table_name, entry_columns, labels, home_page_function):`**
   - Presents a flexible database system interface for viewing, adding, updating, and deleting records.

## Usage

1. Run the `Main.py` script to launch the application.
2. The home page will be displayed, featuring navigation buttons for different sections.
3. Click on a specific section button (e.g., Venue, Player) to view a table with relevant information.
4. Utilize provided buttons to perform operations such as adding, updating, and deleting records.
5. The "Back to Home" button allows seamless navigation back to the home page from any section.

## Setup

- Ensure that MySQL is running.
- Set up the necessary database (`Player_Demo`) and tables for the application to function correctly.

## Customization

Feel free to customize the database connection details and adapt the code to suit specific requirements. The application provides a modular structure for easy extension and modification.

## Dependencies

- Tkinter (GUI)
- MySQL (Database)

