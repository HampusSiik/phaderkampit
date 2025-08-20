#!/usr/bin/env python3
"""
Simple migration script to add difficulty column to sound_clips table.
Run this script to update your existing database.
"""

import sqlite3
import os

def migrate_database():
    """Add difficulty column to sound_clips table"""
    
    # Find the database file
    db_path = "instance/app.db"
    
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        print("Please run the app first to create the database, then run this migration.")
        return False
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if difficulty column already exists
        cursor.execute("PRAGMA table_info(sound_clips)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'difficulty' in columns:
            print("Difficulty column already exists. No migration needed.")
            return True
        
        # Add the difficulty column
        print("Adding difficulty column to sound_clips table...")
        cursor.execute("ALTER TABLE sound_clips ADD COLUMN difficulty VARCHAR(10)")
        
        # Set default value for existing records
        print("Setting default difficulty for existing clips...")
        cursor.execute("UPDATE sound_clips SET difficulty = 'medium' WHERE difficulty IS NULL")
        
        # Commit the changes
        conn.commit()
        print("Migration completed successfully!")
        print("All existing clips have been set to 'medium' difficulty.")
        print("New clips will be automatically assigned difficulty based on their titles.")
        
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Migration failed: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("Starting database migration...")
    success = migrate_database()
    if success:
        print("Migration completed successfully!")
    else:
        print("Migration failed!")
