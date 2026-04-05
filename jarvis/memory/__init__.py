"""
Memory System - Persistent memory from isair + Mark-XXXV
"""

import os
import json
import sqlite3
import logging
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger('jarvis.memory')

class MemoryStore:
    """SQLite-based persistent memory storage"""
    
    def __init__(self, db_path: str = "jarvis_memory.db"):
        self.db_path = db_path
        self.conn = None
        self._init_db()
    
    def _init_db(self):
        """Initialize the database schema"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Memories table (long-term)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                importance INTEGER DEFAULT 5,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0
            )
        ''')
        
        # Preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User info table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_info (
                id INTEGER PRIMARY KEY,
                name TEXT,
                preferences TEXT,
                goals TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        logger.info(f"Memory database initialized: {self.db_path}")
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (role, content) VALUES (?, ?)",
            (role, content)
        )
        self.conn.commit()
    
    def get_recent_messages(self, limit: int = 20) -> List[Dict]:
        """Get recent conversation messages"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        return [{"role": r, "content": c} for r, c in cursor.fetchall()]
    
    def add_memory(self, category: str, content: str, importance: int = 5):
        """Add a long-term memory"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO memories (category, content, importance) VALUES (?, ?, ?)",
            (category, content, importance)
        )
        self.conn.commit()
    
    def search_memories(self, query: str, limit: int = 5) -> List[Dict]:
        """Search memories"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT category, content FROM memories WHERE content LIKE ? ORDER BY importance DESC LIMIT ?",
            (f"%{query}%", limit)
        )
        return [{"category": c, "content": m} for c, m in cursor.fetchall()]
    
    def set_preference(self, key: str, value: str):
        """Set a user preference"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO preferences (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
            (key, value)
        )
        self.conn.commit()
    
    def get_preference(self, key: str, default: str = None) -> Optional[str]:
        """Get a user preference"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
        result = cursor.fetchone()
        return result[0] if result else default
    
    def get_user_info(self) -> Dict:
        """Get user information"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, preferences, goals FROM user_info WHERE id = 1")
        result = cursor.fetchone()
        if result:
            return {
                "name": result[0],
                "preferences": json.loads(result[1]) if result[1] else {},
                "goals": json.loads(result[2]) if result[2] else {}
            }
        return {}
    
    def set_user_info(self, name: str = None, preferences: Dict = None, goals: Dict = None):
        """Set user information"""
        cursor = self.conn.cursor()
        cursor.execute(
            '''INSERT OR REPLACE INTO user_info (id, name, preferences, goals, updated_at)
               VALUES (1, ?, ?, ?, CURRENT_TIMESTAMP)''',
            (name, json.dumps(preferences or {}), json.dumps(goals or {}))
        )
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class ContextManager:
    """Rolling context manager for ongoing conversations"""
    
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.messages = []
    
    def add(self, role: str, content: str):
        """Add a message to context"""
        self.messages.append({"role": role, "content": content})
        self._trim()
    
    def _trim(self):
        """Trim old messages if exceeding token limit"""
        # Simple heuristic: ~4 chars per token
        total_chars = sum(len(m["content"]) for m in self.messages)
        while total_chars > self.max_tokens * 4 and len(self.messages) > 1:
            self.messages.pop(0)
            total_chars = sum(len(m["content"]) for m in self.messages)
    
    def get_context(self) -> List[Dict]:
        """Get current context"""
        return self.messages
    
    def clear(self):
        """Clear context"""
        self.messages = []


class Memory:
    """Main memory system combining persistent storage and context"""
    
    def __init__(self, config: dict):
        db_path = config.get('memory_db', 'jarvis_memory.db')
        self.store = MemoryStore(db_path)
        self.context = ContextManager()
    
    def add_interaction(self, user_message: str, assistant_message: str):
        """Add an interaction to memory"""
        # Add to conversation history
        self.store.add_message("user", user_message)
        self.store.add_message("assistant", assistant_message)
        
        # Add to rolling context
        self.context.add("user", user_message)
        self.context.add("assistant", assistant_message)
        
        # Check for important info to store
        self._extract_and_store_memory(user_message)
    
    def _extract_and_store_memory(self, text: str):
        """Extract important information and store as memory"""
        # This would use NLP to extract key information
        # For now, just storing important-sounding text
        important_keywords = ['name', 'preference', 'goal', 'remember', 'always']
        if any(kw in text.lower() for kw in important_keywords):
            self.store.add_memory("user_info", text, importance=8)
    
    def get_context(self) -> List[Dict]:
        """Get conversation context"""
        return self.context.get_context()
    
    def get_recent_history(self, limit: int = 20) -> List[Dict]:
        """Get recent conversation history"""
        return self.store.get_recent_messages(limit)
    
    def search_memory(self, query: str) -> List[Dict]:
        """Search long-term memories"""
        return self.store.search_memories(query)
    
    def get_preference(self, key: str, default: str = None) -> Optional[str]:
        """Get a user preference"""
        return self.store.get_preference(key, default)
    
    def set_preference(self, key: str, value: str):
        """Set a user preference"""
        self.store.set_preference(key, value)
    
    def close(self):
        """Close memory systems"""
        self.store.close()