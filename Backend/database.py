import sqlite3
import hashlib
import json
from datetime import datetime

class FitnessDB:
    def __init__(self, db_path="fitness_app.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                fitness_level TEXT,
                primary_goal TEXT,
                weight REAL,
                height REAL,
                age INTEGER,
                activity_level TEXT,
                workout_frequency TEXT,
                workout_duration TEXT,
                target_weight REAL,
                timeline TEXT,
                motivation TEXT,
                preferred_time TEXT,
                workout_location TEXT,
                sleep_hours TEXT,
                stress_level TEXT,
                dietary_restrictions TEXT,
                medical_conditions TEXT,
                preferences TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # User knowledge base for RAG
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Workout journal entries
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workout_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                title TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Individual exercises within workout entries
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workout_exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_id INTEGER,
                exercise_name TEXT,
                sets INTEGER,
                reps INTEGER,
                weight REAL,
                duration_minutes INTEGER,
                notes TEXT,
                completed BOOLEAN DEFAULT 0,
                FOREIGN KEY (entry_id) REFERENCES workout_entries (id)
            )
        ''')
        
        # Migrate existing profiles to new schema
        try:
            cursor.execute("ALTER TABLE user_profiles ADD COLUMN workout_frequency TEXT")
            cursor.execute("ALTER TABLE user_profiles ADD COLUMN workout_duration TEXT")
            cursor.execute("ALTER TABLE user_profiles ADD COLUMN target_weight REAL")
            cursor.execute("ALTER TABLE user_profiles ADD COLUMN timeline TEXT")
            cursor.execute("ALTER TABLE user_profiles ADD COLUMN motivation TEXT")
            cursor.execute("ALTER TABLE user_profiles ADD COLUMN preferred_time TEXT")
            cursor.execute("ALTER TABLE user_profiles ADD COLUMN workout_location TEXT")
            cursor.execute("ALTER TABLE user_profiles ADD COLUMN sleep_hours TEXT")
            cursor.execute("ALTER TABLE user_profiles ADD COLUMN stress_level TEXT")
        except sqlite3.OperationalError:
            # Columns already exist
            pass
        
        conn.commit()
        conn.close()
    
    def _safe_json_loads(self, json_str):
        """Safely load JSON with fallback to empty dict"""
        if not json_str or not json_str.strip():
            return {}
        try:
            return json.loads(json_str)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def hash_password(self, password):
        """Hash password with salt"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, password):
        """Create new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def save_user_profile(self, user_id, profile_data):
        """Save user profile data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_profiles 
            (user_id, fitness_level, primary_goal, weight, height, age, 
             activity_level, workout_frequency, workout_duration, target_weight,
             timeline, motivation, preferred_time, workout_location, sleep_hours,
             stress_level, dietary_restrictions, medical_conditions, preferences)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            profile_data.get('fitness_level'),
            profile_data.get('primary_goal'),
            profile_data.get('weight'),
            profile_data.get('height'),
            profile_data.get('age'),
            profile_data.get('activity_level'),
            profile_data.get('workout_frequency'),
            profile_data.get('workout_duration'),
            profile_data.get('target_weight'),
            profile_data.get('timeline'),
            profile_data.get('motivation'),
            profile_data.get('preferred_time'),
            profile_data.get('workout_location'),
            profile_data.get('sleep_hours'),
            profile_data.get('stress_level'),
            profile_data.get('dietary_restrictions'),
            profile_data.get('medical_conditions'),
            json.dumps(profile_data.get('preferences', {}))
        ))
        
        conn.commit()
        conn.close()
    
    def get_user_profile(self, user_id):
        """Get user profile data"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            profile = {
                'fitness_level': result['fitness_level'],
                'primary_goal': result['primary_goal'],
                'weight': result['weight'],
                'height': result['height'],
                'age': result['age'],
                'activity_level': result['activity_level'],
                'workout_frequency': result['workout_frequency'],
                'workout_duration': result['workout_duration'],
                'target_weight': result['target_weight'],
                'timeline': result['timeline'],
                'motivation': result['motivation'],
                'preferred_time': result['preferred_time'],
                'workout_location': result['workout_location'],
                'sleep_hours': result['sleep_hours'],
                'stress_level': result['stress_level'],
                'dietary_restrictions': result['dietary_restrictions'],
                'medical_conditions': result['medical_conditions'],
                'preferences': self._safe_json_loads(result['preferences'])
            }
            return profile
        return None
    
    def add_user_knowledge(self, user_id, category, content):
        """Add knowledge entry for RAG"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO user_knowledge (user_id, category, content) VALUES (?, ?, ?)",
            (user_id, category, content)
        )
        
        conn.commit()
        conn.close()
    
    def get_user_knowledge(self, user_id, limit=10):
        """Get user knowledge for RAG context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT category, content, timestamp FROM user_knowledge WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        return [{'category': r[0], 'content': r[1], 'timestamp': r[2]} for r in results]
    
    def save_workout_entry(self, user_id, entry_data):
        """Save workout journal entry with exercises"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Save main entry
        cursor.execute(
            "INSERT INTO workout_entries (user_id, date, title, notes) VALUES (?, ?, ?, ?)",
            (user_id, entry_data['date'], entry_data['title'], entry_data.get('notes', ''))
        )
        entry_id = cursor.lastrowid
        
        # Save exercises
        for exercise in entry_data.get('exercises', []):
            cursor.execute(
                "INSERT INTO workout_exercises (entry_id, exercise_name, sets, reps, weight, duration_minutes, notes, completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (entry_id, exercise['name'], exercise.get('sets'), exercise.get('reps'), 
                 exercise.get('weight'), exercise.get('duration'), exercise.get('notes', ''), exercise.get('completed', False))
            )
        
        conn.commit()
        conn.close()
        return entry_id
    
    def get_workout_entries(self, user_id, limit=20):
        """Get workout journal entries for user"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM workout_entries WHERE user_id = ? ORDER BY date DESC, created_at DESC LIMIT ?",
            (user_id, limit)
        )
        entries = cursor.fetchall()
        
        result = []
        for entry in entries:
            # Get exercises for this entry
            cursor.execute(
                "SELECT * FROM workout_exercises WHERE entry_id = ? ORDER BY id",
                (entry['id'],)
            )
            exercises = cursor.fetchall()
            
            result.append({
                'id': entry['id'],
                'date': entry['date'],
                'title': entry['title'],
                'notes': entry['notes'],
                'created_at': entry['created_at'],
                'exercises': [dict(ex) for ex in exercises]
            })
        
        conn.close()
        return result
    
    def update_exercise_completion(self, exercise_id, completed):
        """Update exercise completion status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE workout_exercises SET completed = ? WHERE id = ?",
            (completed, exercise_id)
        )
        
        conn.commit()
        conn.close()
    
    def update_workout_entry(self, entry_id, user_id, entry_data):
        """Update existing workout entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update main entry
        cursor.execute(
            "UPDATE workout_entries SET date = ?, title = ?, notes = ? WHERE id = ? AND user_id = ?",
            (entry_data['date'], entry_data['title'], entry_data.get('notes', ''), entry_id, user_id)
        )
        
        # Delete existing exercises
        cursor.execute("DELETE FROM workout_exercises WHERE entry_id = ?", (entry_id,))
        
        # Add updated exercises
        for exercise in entry_data.get('exercises', []):
            cursor.execute(
                "INSERT INTO workout_exercises (entry_id, exercise_name, sets, reps, weight, duration_minutes, notes, completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (entry_id, exercise['name'], exercise.get('sets'), exercise.get('reps'), 
                 exercise.get('weight'), exercise.get('duration'), exercise.get('notes', ''), exercise.get('completed', False))
            )
        
        conn.commit()
        conn.close()
    
    def get_workout_entry(self, entry_id, user_id):
        """Get single workout entry"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM workout_entries WHERE id = ? AND user_id = ?",
            (entry_id, user_id)
        )
        entry = cursor.fetchone()
        
        if entry:
            cursor.execute(
                "SELECT * FROM workout_exercises WHERE entry_id = ? ORDER BY id",
                (entry['id'],)
            )
            exercises = cursor.fetchall()
            
            result = {
                'id': entry['id'],
                'date': entry['date'],
                'title': entry['title'],
                'notes': entry['notes'],
                'created_at': entry['created_at'],
                'exercises': [dict(ex) for ex in exercises]
            }
            
            conn.close()
            return result
        
        conn.close()
        return None

db = FitnessDB()
