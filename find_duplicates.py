#!/usr/bin/env python3
"""
Script to find and handle duplicate files in the database.
"""

import sqlite3
import os
from collections import defaultdict

def find_duplicates():
    """Find duplicate files by title and original_name"""
    
    # Find the database file
    db_path = "instance/app.db"
    
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return False
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all clips
        cursor.execute("SELECT id, title, original_name, filename, list_id FROM sound_clips ORDER BY title, id")
        clips = cursor.fetchall()
        
        if not clips:
            print("No clips found in database.")
            return True
        
        print(f"Found {len(clips)} total clips")
        print()
        
        # Group by title to find duplicates
        title_groups = defaultdict(list)
        for clip in clips:
            clip_id, title, original_name, filename, list_id = clip
            title_groups[title.lower().strip()].append(clip)
        
        # Find duplicates
        duplicates = []
        for title, clip_list in title_groups.items():
            if len(clip_list) > 1:
                duplicates.append((title, clip_list))
        
        if not duplicates:
            print("✅ No duplicate files found!")
            return True
        
        print(f"Found {len(duplicates)} duplicate titles:")
        print()
        
        for title, clip_list in duplicates:
            print(f"📁 '{title}' ({len(clip_list)} copies):")
            for clip in clip_list:
                clip_id, title, original_name, filename, list_id = clip
                print(f"  - ID: {clip_id}, List: {list_id}, File: {filename}")
            print()
        
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def remove_duplicates():
    """Remove duplicate files, keeping the oldest one"""
    
    # Find the database file
    db_path = "instance/app.db"
    
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return False
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all clips
        cursor.execute("SELECT id, title, original_name, filename, list_id, created_at FROM sound_clips ORDER BY title, created_at")
        clips = cursor.fetchall()
        
        if not clips:
            print("No clips found in database.")
            return True
        
        # Group by title to find duplicates
        title_groups = defaultdict(list)
        for clip in clips:
            clip_id, title, original_name, filename, list_id, created_at = clip
            title_groups[title.lower().strip()].append(clip)
        
        # Find duplicates
        duplicates = []
        for title, clip_list in title_groups.items():
            if len(clip_list) > 1:
                duplicates.append((title, clip_list))
        
        if not duplicates:
            print("✅ No duplicate files found!")
            return True
        
        print(f"Found {len(duplicates)} duplicate titles to clean up:")
        print()
        
        removed_count = 0
        
        for title, clip_list in duplicates:
            print(f"📁 '{title}' ({len(clip_list)} copies):")
            
            # Sort by creation date (oldest first)
            clip_list.sort(key=lambda x: x[5])  # created_at is at index 5
            
            # Keep the oldest one, remove the rest
            keep_clip = clip_list[0]
            remove_clips = clip_list[1:]
            
            print(f"  ✅ Keeping: ID {keep_clip[0]} (oldest)")
            
            for clip in remove_clips:
                clip_id, title, original_name, filename, list_id, created_at = clip
                print(f"  🗑️ Removing: ID {clip_id}, File: {filename}")
                
                # Delete the physical file
                file_path = os.path.join("uploads", filename)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        print(f"    - Deleted file: {filename}")
                    except OSError as e:
                        print(f"    - Failed to delete file {filename}: {e}")
                
                # Delete from database
                cursor.execute("DELETE FROM sound_clips WHERE id = ?", (clip_id,))
                removed_count += 1
            
            print()
        
        # Commit the changes
        conn.commit()
        print(f"✅ Removed {removed_count} duplicate clips!")
        
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "remove":
        print("Removing duplicate files...")
        success = remove_duplicates()
    else:
        print("Finding duplicate files...")
        success = find_duplicates()
        if success:
            print("\nTo remove duplicates, run: python3 find_duplicates.py remove")
    
    if success:
        print("Operation completed successfully!")
    else:
        print("Operation failed!")
