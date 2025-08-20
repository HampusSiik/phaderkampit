#!/usr/bin/env python3
"""
Script to update existing clips with correct difficulties based on difficulties.txt file.
"""

import sqlite3
import os

def get_difficulty_mapping():
    """Load difficulty mapping from difficulties.txt file"""
    mapping = {
        'easy': [],
        'medium': [],
        'hard': []
    }
    
    try:
        with open('app/difficulties.txt', 'r', encoding='utf-8') as f:
            current_category = None
            for line in f:
                line = line.strip()
                if line == 'Lätta:':
                    current_category = 'easy'
                elif line == 'Mellan:':
                    current_category = 'medium'
                elif line == 'Svår:':
                    current_category = 'hard'
                elif line and current_category and not line.startswith('✅') and not line.startswith('❌') and not line.startswith('☑️'):
                    # Extract the title from the line (remove URLs and other info)
                    title = line.split(',')[0].split('https://')[0].strip()
                    if title:
                        mapping[current_category].append(title.lower())
    except FileNotFoundError:
        print("difficulties.txt file not found!")
        return None
    
    return mapping

def determine_difficulty(title, mapping):
    """Determine difficulty based on title using the mapping"""
    title_lower = title.lower()
    
    # Normalize title by removing special characters and extra spaces
    title_normalized = ' '.join(title_lower.replace('-', ' ').replace('_', ' ').split())
    
    # Check for exact matches first
    for difficulty, titles in mapping.items():
        for mapped_title in titles:
            # Normalize mapped title too
            mapped_normalized = ' '.join(mapped_title.replace('-', ' ').replace('_', ' ').split())
            
            if mapped_normalized in title_normalized or title_normalized in mapped_normalized:
                return difficulty
    
    # Check for partial matches with better word matching
    for difficulty, titles in mapping.items():
        for mapped_title in titles:
            # Normalize mapped title
            mapped_normalized = ' '.join(mapped_title.replace('-', ' ').replace('_', ' ').split())
            
            # Split into words and check for significant word matches
            title_words = set(title_normalized.split())
            mapped_words = set(mapped_normalized.split())
            
            # Check if any significant words match (longer than 3 chars)
            significant_matches = 0
            for title_word in title_words:
                if len(title_word) > 3:
                    for mapped_word in mapped_words:
                        if len(mapped_word) > 3:
                            if title_word in mapped_word or mapped_word in title_word:
                                significant_matches += 1
            
            # If we have at least 2 significant word matches, consider it a match
            if significant_matches >= 2:
                return difficulty
    
    # Check for single word matches for very specific terms
    for difficulty, titles in mapping.items():
        for mapped_title in titles:
            mapped_normalized = ' '.join(mapped_title.replace('-', ' ').replace('_', ' ').split())
            
            # For very specific terms like "widowmaker", "sekiro", "pokemon", etc.
            for word in title_normalized.split():
                if len(word) > 4:  # Longer words are more specific
                    for mapped_word in mapped_normalized.split():
                        if len(mapped_word) > 4:
                            if word == mapped_word:
                                return difficulty
    
    # Check for keyword matches (like "pokemon" in any context)
    # Use word boundaries to avoid false positives
    # Only use keywords for titles that don't match anything in difficulties.txt
    keywords = {
        'easy': ['minecraft', 'roblox', 'cs', 'league', 'valorant', 'mario', 'pac', 'zelda'],
        'medium': ['dark', 'souls', 'terraria', 'portal', 'tf2', 'fortnite', 'cod'],
        'hard': ['sekiro', 'widowmaker', 'warframe', 'hearts', 'iron', 'eu4', 'arma', 'titanfall', 'hollowknight', 'kerbal']
        # Removed 'pokemon' from hard keywords since it's in difficulties.txt
    }
    
    # Split title into words for more precise matching
    title_words = set(title_normalized.split())
    
    for difficulty, keyword_list in keywords.items():
        for keyword in keyword_list:
            # Check if the keyword appears as a complete word
            if keyword in title_words:
                return difficulty
    
    # Default to medium if no match found
    return 'medium'

def update_clip_difficulties():
    """Update existing clips with correct difficulties"""
    
    # Find the database file
    db_path = "instance/app.db"
    
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return False
    
    # Get difficulty mapping
    mapping = get_difficulty_mapping()
    if not mapping:
        return False
    
    print("Difficulty mapping loaded:")
    print(f"  Easy: {len(mapping['easy'])} titles")
    print(f"  Medium: {len(mapping['medium'])} titles")
    print(f"  Hard: {len(mapping['hard'])} titles")
    print()
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all clips
        cursor.execute("SELECT id, title FROM sound_clips")
        clips = cursor.fetchall()
        
        if not clips:
            print("No clips found in database.")
            return True
        
        print(f"Found {len(clips)} clips to update:")
        print()
        
        updated_count = 0
        
        for clip_id, title in clips:
            old_difficulty = cursor.execute("SELECT difficulty FROM sound_clips WHERE id = ?", (clip_id,)).fetchone()[0]
            new_difficulty = determine_difficulty(title, mapping)
            
            if old_difficulty != new_difficulty:
                cursor.execute("UPDATE sound_clips SET difficulty = ? WHERE id = ?", (new_difficulty, clip_id))
                print(f"  '{title}' -> {old_difficulty} → {new_difficulty}")
                updated_count += 1
            else:
                print(f"  '{title}' -> {old_difficulty} (no change)")
        
        # Commit the changes
        conn.commit()
        print()
        print(f"Updated {updated_count} clips with new difficulties!")
        
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Update failed: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("Updating clip difficulties based on difficulties.txt...")
    success = update_clip_difficulties()
    if success:
        print("Difficulty update completed successfully!")
    else:
        print("Difficulty update failed!")
