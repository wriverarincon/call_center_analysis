import sqlite3
import os


# Get current directory
current_directory = os.path.dirname(os.path.abspath(__file__))


# Create database file
db_file_path = os.path.join(current_directory, "local_database.db")


# Connection to database
connection = sqlite3.connect(db_file_path)
cursor = connection.cursor()


"""Create tables"""
# Agents table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS agents (
        name TEXT NOT NULL,
        average_handle_time INTEGER NOT NULL,
        service_level INTEGER NOT NULL,
        idle_time INTEGER NOT NULL,
        email TEXT NOT NULL,
        supervisor_id INTEGER NOT NULL,
        FOREIGN KEY (supervisor_id) REFERENCES supervisors(id)
    )
    """
)


# Supervisors table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS supervisors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """
)


# Commit the queries
connection.commit()
connection.close()