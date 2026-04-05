"""
Enhanced Memory System - Learning, gestures, preferences
"""

import os
import json
import sqlite3
import logging
from typing import Optional, List, Dict
from datetime import datetime

logger = logging.getLogger('jarvis.memory')

class MemoryStore:
    """SQLite-based persistent memory with learning"""
    
    def __init__(self, db_path: str = "jarvis_memory.db"):
        self.db_path = db_path
        self.conn = None
        self._init_db()
    
    def _init_db(self):
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Conversations
        cursor.execute('''CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY, role TEXT, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        
        # Long-term memories
        cursor.execute('''CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY, category TEXT, content TEXT, importance INTEGER DEFAULT 5,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        
        # User preferences - ENHANCED
        cursor.execute('''CREATE TABLE IF NOT EXISTS preferences (
            key TEXT PRIMARY KEY, value TEXT, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        
        # Learned gestures
        cursor.execute('''CREATE TABLE IF NOT EXISTS gestures (
            id INTEGER PRIMARY KEY, name TEXT UNIQUE, action TEXT, trigger TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        
        # Tone preferences
        cursor.execute('''CREATE TABLE IF NOT EXISTS tone_preferences (
            id INTEGER PRIMARY KEY, tone TEXT, feedback TEXT, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        
        # To-do list
        cursor.execute('''CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY, task TEXT, status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'medium', due_date TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        
        # Automation schedules
        cursor.execute('''CREATE TABLE IF NOT EXISTS automations (
            id INTEGER PRIMARY KEY, name TEXT, action_type TEXT, schedule TEXT,
            config TEXT, enabled INTEGER DEFAULT 1, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        
        self.conn.commit()
        logger.info(f"Memory DB: {self.db_path}")
    
    def add_message(self, role: str, content: str):
        self.conn.execute("INSERT INTO conversations (role, content) VALUES (?, ?)", (role, content))
        self.conn.commit()
    
    def get_recent(self, limit: int = 20) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?", (limit,))
        return [{"role": r, "content": c} for r, c in cursor.fetchall()]
    
    def add_memory(self, category: str, content: str, importance: int = 5):
        self.conn.execute("INSERT INTO memories (category, content, importance) VALUES (?, ?, ?)",
                         (category, content, importance))
        self.conn.commit()
    
    def search_memories(self, query: str, limit: int = 5) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT category, content FROM memories WHERE content LIKE ? ORDER BY importance DESC LIMIT ?",
                     (f"%{query}%", limit))
        return [{"category": c, "content": m} for c, m in cursor.fetchall()]
    
    # === PREFERENCES ===
    def set_preference(self, key: str, value: str):
        self.conn.execute("INSERT OR REPLACE INTO preferences (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                         (key, value))
        self.conn.commit()
    
    def get_preference(self, key: str, default: str = None) -> Optional[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
        result = cursor.fetchone()
        return result[0] if result else default
    
    def get_all_preferences(self) -> Dict:
        cursor = self.conn.cursor()
        cursor.execute("SELECT key, value FROM preferences")
        return {k: v for k, v in cursor.fetchall()}
    
    # === GESTURES ===
    def add_gesture(self, name: str, action: str, trigger: str = ""):
        self.conn.execute("INSERT OR REPLACE INTO gestures (name, action, trigger) VALUES (?, ?, ?)",
                         (name, action, trigger))
        self.conn.commit()
    
    def get_gestures(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, action, trigger FROM gestures")
        return [{"name": n, "action": a, "trigger": t} for n, a, t in cursor.fetchall()]
    
    def delete_gesture(self, name: str):
        self.conn.execute("DELETE FROM gestures WHERE name = ?", (name,))
        self.conn.commit()
    
    # === TODOS ===
    def add_todo(self, task: str, priority: str = "medium", due_date: str = None):
        self.conn.execute("INSERT INTO todos (task, priority, due_date) VALUES (?, ?, ?)",
                         (task, priority, due_date))
        self.conn.commit()
    
    def get_todos(self, status: str = None) -> List[Dict]:
        cursor = self.conn.cursor()
        if status:
            cursor.execute("SELECT id, task, status, priority, due_date FROM todos WHERE status = ? ORDER BY id DESC", (status,))
        else:
            cursor.execute("SELECT id, task, status, priority, due_date FROM todos ORDER BY id DESC")
        return [{"id": r[0], "task": r[1], "status": r[2], "priority": r[3], "due_date": r[4]} for r in cursor.fetchall()]
    
    def update_todo(self, todo_id: int, status: str = None, task: str = None):
        if status:
            self.conn.execute("UPDATE todos SET status = ? WHERE id = ?", (status, todo_id))
        if task:
            self.conn.execute("UPDATE todos SET task = ? WHERE id = ?", (task, todo_id))
        self.conn.commit()
    
    def delete_todo(self, todo_id: int):
        self.conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        self.conn.commit()
    
    # === AUTOMATIONS ===
    def add_automation(self, name: str, action_type: str, schedule: str, config: Dict):
        self.conn.execute("INSERT INTO automations (name, action_type, schedule, config) VALUES (?, ?, ?, ?)",
                         (name, action_type, schedule, json.dumps(config)))
        self.conn.commit()
    
    def get_automations(self, enabled_only: bool = True) -> List[Dict]:
        cursor = self.conn.cursor()
        if enabled_only:
            cursor.execute("SELECT name, action_type, schedule, config FROM automations WHERE enabled = 1")
        else:
            cursor.execute("SELECT name, action_type, schedule, config FROM automations")
        return [{"name": r[0], "action_type": r[1], "schedule": r[2], "config": json.loads(r[3])} for r in cursor.fetchall()]
    
    def toggle_automation(self, name: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT enabled FROM automations WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            new_state = 0 if result[0] else 1
            self.conn.execute("UPDATE automations SET enabled = ? WHERE name = ?", (new_state, name))
            self.conn.commit()
    
    def close(self):
        if self.conn:
            self.conn.close()


class ContextManager:
    """Rolling context with preference awareness"""
    
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.messages = []
        self.preferences = {}
    
    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._trim()
    
    def set_preferences(self, prefs: Dict):
        self.preferences = prefs
    
    def _trim(self):
        total_chars = sum(len(m["content"]) for m in self.messages)
        while total_chars > self.max_tokens * 4 and len(self.messages) > 1:
            self.messages.pop(0)
            total_chars = sum(len(m["content"]) for m in self.messages)
    
    def get_context(self) -> List[Dict]:
        return self.messages


class Memory:
    """Main memory system with learning"""
    
    def __init__(self, config: dict):
        db_path = config.get('memory_db', 'jarvis_memory.db')
        self.store = MemoryStore(db_path)
        self.context = ContextManager()
        
        # Load existing preferences
        prefs = self.store.get_all_preferences()
        self.context.set_preferences(prefs)
    
    def add_interaction(self, user_message: str, assistant_message: str):
        self.store.add_message("user", user_message)
        self.store.add_message("assistant", assistant_message)
        self.context.add("user", user_message)
        self.context.add("assistant", assistant_message)
    
    def get_context(self) -> List[Dict]:
        return self.context.get_context()
    
    def get_todos(self, status: str = None) -> List[Dict]:
        return self.store.get_todos(status)
    
    def add_todo(self, task: str, priority: str = "medium", due_date: str = None):
        self.store.add_todo(task, priority, due_date)
    
    def update_todo(self, todo_id: int, status: str = None, task: str = None):
        self.store.update_todo(todo_id, status, task)
    
    def delete_todo(self, todo_id: int):
        self.store.delete_todo(todo_id)
    
    def get_gestures(self) -> List[Dict]:
        return self.store.get_gestures()
    
    def add_gesture(self, name: str, action: str, trigger: str = ""):
        self.store.add_gesture(name, action, trigger)
    
    def delete_gesture(self, name: str):
        self.store.delete_gesture(name)
    
    def get_automations(self, enabled_only: bool = True) -> List[Dict]:
        return self.store.get_automations(enabled_only)
    
    def add_automation(self, name: str, action_type: str, schedule: str, config: Dict):
        self.store.add_gesture(name, action_type, schedule)  # Reusing for automations
    
    def toggle_automation(self, name: str):
        self.store.toggle_automation(name)
    
    def get_preference(self, key: str, default: str = None) -> Optional[str]:
        return self.store.get_preference(key, default)
    
    def set_preference(self, key: str, value: str):
        self.store.set_preference(key, value)
        self.context.preferences[key] = value
    
    def search_memory(self, query: str) -> List[Dict]:
        return self.store.search_memories(query)
    
    def close(self):
        self.store.close()