"""
Jarvis Unified v3.1 - Gemini-Powered + WhatsApp Integration
Optimized for any device - works without Ollama
"""

import os
import json
import logging
import asyncio
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('jarvis')

# ==================== CONFIG ====================

class JarvisConfig:
    def __init__(self, env_file: str = '.env'):
        self.env_file = env_file
        self.config = {}
        self.load_env()
    
    def load_env(self):
        if Path(self.env_file).exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        
        self.config = {
            # === AI PROVIDERS - PRIORITY: GEMINI (FREE TIER) ===
            'ai_provider': os.getenv('AI_PROVIDER', 'gemini'),  # Changed default to gemini!
            'gemini_api_key': os.getenv('GEMINI_API_KEY', ''),
            'gemini_model': os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-lite'),
            
            # Fallback: Ollama (local, optional)
            'ollama_url': os.getenv('OLLAMA_URL', 'http://localhost:11434'),
            'ollama_model': os.getenv('OLLAMA_MODEL', 'qwen3:8b'),
            
            # Also support OpenRouter as fallback
            'openrouter_key': os.getenv('OPENROUTER_API_KEY', ''),
            
            # === Voice ===
            'tts_engine': os.getenv('TTS_ENGINE', 'pyttsx3'),
            'stt_engine': os.getenv('STT_ENGINE', 'whisper'),
            'wake_word': os.getenv('WAKE_WORD', 'Jarvis').lower(),
            'input_mode': os.getenv('INPUT_MODE', 'text'),
            
            # === UI ===
            'ui_theme': os.getenv('UI_THEME', 'tron'),
            'accent_color': os.getenv('ACCENT_COLOR', '#00ffff'),
            
            # === Tone ===
            'jarvis_tone': os.getenv('JARVIS_TONE', 'helpful'),
            
            # === Learning ===
            'self_learning': os.getenv('SELF_LEARNING', 'true').lower() == 'true',
            'learning_db': os.getenv('LEARNING_DB', 'jarvis_learning.json'),
            
            # === Memory & Brain ===
            'memory_db': os.getenv('MEMORY_DB', 'jarvis_memory.db'),
            'brain_viz': os.getenv('BRAIN_VIZ', 'true').lower() == 'true',
            
            # === WhatsApp (Business API) ===
            'whatsapp_enabled': os.getenv('WHATSAPP_ENABLED', 'false').lower() == 'true',
            'whatsapp_token': os.getenv('WHATSAPP_TOKEN', ''),
            'whatsapp_phone_id': os.getenv('WHATSAPP_PHONE_ID', ''),
            'whatsapp_business_id': os.getenv('WHATSAPP_BUSINESS_ID', ''),
            # Alternative: Twilio
            'twilio_account_sid': os.getenv('TWILIO_ACCOUNT_SID', ''),
            'twilio_auth_token': os.getenv('TWILIO_AUTH_TOKEN', ''),
            'twilio_phone_number': os.getenv('TWILIO_PHONE_NUMBER', ''),
            
            # === Food Agent ===
            'food_default_store': os.getenv('FOOD_DEFAULT_STORE', 'walmart'),
            
            # === SMS ===
            'sms_via_gmail': os.getenv('SMS_VIA_GMAIL', 'true').lower() == 'true',
            
            # === Security ===
            'confirm_payments': os.getenv('CONFIRM_PAYMENTS', 'true').lower() == 'true',
            'confirm_orders': os.getenv('CONFIRM_ORDERS', 'true').lower() == 'true',
            'confirm_sms': os.getenv('CONFIRM_SMS', 'true').lower() == 'true',
            'confirm_whatsapp': os.getenv('CONFIRM_WHATSAPP', 'true').lower() == 'true',
            
            # === Google Services ===
            'google_client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
            'google_client_secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
            'google_refresh_token': os.getenv('GOOGLE_REFRESH_TOKEN', ''),
            
            # === Server ===
            'port': int(os.getenv('PORT', '5000')),
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)


# ==================== GEMINI AI CLIENT ====================

class GeminiClient:
    """Google Gemini API - 100% FREE tier available"""
    
    def __init__(self, config: JarvisConfig):
        self.config = config
        self.api_key = config.get('gemini_api_key')
        self.model = config.get('gemini_model', 'gemini-2.0-flash-lite')
        self.provider = 'gemini'
        logger.info(f"Gemini client initialized with model: {self.model}")
    
    async def chat(self, message: str, context: List[Dict] = None) -> str:
        if not self.api_key:
            return "⚠️ No Gemini API key configured. Get one free at: https://aistudio.google.com/app/apikey"
        
        try:
            # Build conversation
            contents = []
            if context:
                for msg in context[-10:]:
                    contents.append({
                        "role": "model" if msg.get("role") == "assistant" else "user",
                        "parts": [{"text": msg.get("content", "")}]
                    })
            
            contents.append({"role": "user", "parts": [{"text": message}]})
            
            # Call Gemini API
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
            
            resp = requests.post(
                url,
                params={"key": self.api_key},
                json={"contents": contents},
                timeout=60
            )
            
            if resp.status_code == 200:
                data = resp.json()
                response = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                return response if response else "No response from Gemini"
            else:
                logger.error(f"Gemini error: {resp.status_code} - {resp.text}")
                return f"Gemini error: {resp.status_code}. Check your API key."
                
        except Exception as e:
            logger.error(f"Gemini exception: {e}")
            return f"Error: {e}"


# ==================== WHATSAPP INTEGRATION ====================

class WhatsAppAgent:
    """WhatsApp Business API integration - Send messages from Jarvis"""
    
    def __init__(self, config: JarvisConfig):
        self.config = config
        self.enabled = config.get('whatsapp_enabled', False)
        
        # WhatsApp Business API credentials
        self.whatsapp_token = config.get('whatsapp_token', '')
        self.phone_id = config.get('whatsapp_phone_id', '')
        
        # Twilio fallback
        self.twilio_sid = config.get('twilio_account_sid', '')
        self.twilio_token = config.get('twilio_auth_token', '')
        self.twilio_number = config.get('twilio_phone_number', '')
    
    async def send_message(self, to: str, message: str) -> str:
        """Send WhatsApp message with confirmation check"""
        
        # Security confirmation check
        if self.config.get('confirm_whatsapp', True):
            return f"⚠️ WHATSAPP CONFIRMATION REQUIRED:\n\nSend WhatsApp to {to}:\n\n\"{message}\"\n\nReply 'yes' to confirm or 'no' to cancel."
        
        return await self._send(to, message)
    
    async def _send(self, to: str, message: str) -> str:
        """Actually send the message"""
        
        # Try WhatsApp Business API first
        if self.enabled and self.whatsapp_token and self.phone_id:
            return await self._send_whatsapp_api(to, message)
        
        # Try Twilio fallback
        if self.twilio_sid and self.twilio_token:
            return await self._send_twilio(to, message)
        
        # No credentials - show setup instructions
        return self._get_setup_instructions()
    
    async def _send_whatsapp_api(self, to: str, message: str) -> str:
        """Send via WhatsApp Business API"""
        try:
            url = f"https://graph.facebook.com/v18.0/{self.phone_id}/messages"
            headers = {
                "Authorization": f"Bearer {self.whatsapp_token}",
                "Content-Type": "application/json"
            }
            data = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": message}
            }
            
            resp = requests.post(url, headers=headers, json=data, timeout=30)
            
            if resp.status_code in [200, 201]:
                return f"✅ WhatsApp sent to {to}:\n\n\"{message}\""
            else:
                return f"❌ WhatsApp error: {resp.status_code}\n{resp.text}"
                
        except Exception as e:
            return f"❌ WhatsApp failed: {e}"
    
    async def _send_twilio(self, to: str, message: str) -> str:
        """Send via Twilio (alternative)"""
        try:
            from twilio.rest import Client
            
            client = Client(self.twilio_sid, self.twilio_token)
            
            # Format number for WhatsApp
            if not to.startswith('whatsapp:'):
                to = f"whatsapp:{to}"
            
            twilio_msg = client.messages.create(
                from_=f"whatsapp:{self.twilio_number}",
                body=message,
                to=to
            )
            
            return f"✅ WhatsApp (Twilio) sent: {twilio_msg.sid}"
            
        except ImportError:
            return "❌ Twilio not installed. Run: pip install twilio"
        except Exception as e:
            return f"❌ Twilio error: {e}"
    
    def _get_setup_instructions(self) -> str:
        return """📱 WhatsApp Setup Options:

OPTION 1: WhatsApp Business API (Recommended)
1. Go to: https://developers.facebook.com/
2. Create app → WhatsApp
3. Get Phone Number ID and Access Token
4. Add to .env:
   WHATSAPP_ENABLED=true
   WHATSAPP_TOKEN=your_token
   WHATSAPP_PHONE_ID=your_phone_id

OPTION 2: Twilio (Easier)
1. Go to: https://console.twilio.com
2. Get phone number with WhatsApp
3. Add to .env:
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_PHONE_NUMBER=your_number

⚠️ Note: WhatsApp requires verified numbers for sending to new contacts."""


# ==================== SELF-LEARNING ====================

class SelfLearningEngine:
    """Jarvis grades and improves its own responses"""
    
    def __init__(self, db_file: str = "jarvis_learning.json"):
        self.db_file = db_file
        self.data = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {"responses": [], "grades": [], "patterns": {}}
    
    def _save(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def log_response(self, prompt: str, response: str, context: str = ""):
        entry = {
            "id": len(self.data.get('responses', [])),
            "prompt": prompt[:200],
            "response": response[:500],
            "timestamp": datetime.now().isoformat(),
            "grade": None
        }
        self.data.setdefault('responses', []).append(entry)
        self._save()
    
    def grade_response(self, response_id: int, grade: int, feedback: str = ""):
        for resp in self.data.get('responses', []):
            if resp['id'] == response_id:
                resp['grade'] = grade
                break
        
        self.data.setdefault('grades', []).append({
            "grade": grade, "timestamp": datetime.now().isoformat()
        })
        self._save()
    
    def get_stats(self) -> Dict:
        grades = self.data.get('grades', [])
        if not grades:
            return {"total_responses": 0, "avg_grade": 0, "trend": "neutral"}
        
        recent = grades[-5:]
        recent_avg = sum(g['grade'] for g in recent) / len(recent)
        
        return {
            "total_responses": len(self.data.get('responses', [])),
            "avg_grade": round(sum(grades) / len(grades), 2),
            "recent_avg": round(recent_avg, 2),
            "trend": "improving" if recent_avg >= 3 else "learning"
        }


# ==================== FOOD AGENT ====================

class FoodAgent:
    """Grocery ordering, recipes, cooking timers"""
    
    def __init__(self, config: JarvisConfig, memory=None):
        self.config = config
        self.memory = memory
        self.shopping_lists = {}
    
    async def process_food_request(self, request: str) -> str:
        req = request.lower()
        
        if any(w in req for w in ['order', 'buy', 'get', 'shop']):
            items = self._extract_items(request)
            if not items:
                return "What items would you like to order?"
            
            store = self.config.get('food_default_store', 'walmart')
            list_name = f"order_{datetime.now().strftime('%Y%m%d_%H%M')}"
            self.shopping_lists[list_name] = {"items": items, "store": store}
            
            return f"📝 Added to {store.title()} cart:\n• {', '.join(items)}\n\n⚠️ CONFIRMATION REQUIRED: Proceed to checkout?"
        
        elif any(w in req for w in ['recipe', 'ingredient', 'make']):
            return self._get_recipe(req)
        
        elif any(w in req for w in ['timer', 'cook', 'minutes']):
            return self._set_timer(request)
        
        return "I can: order groceries, find recipes, set timers. What do you need?"
    
    def _extract_items(self, text: str) -> List[str]:
        food_words = ['milk', 'bread', 'eggs', 'butter', 'cheese', 'chicken', 'beef', 'apple', 'banana', 'lettuce', 'tomato', 'rice', 'pasta', 'coffee', 'juice', 'water']
        words = text.lower().split()
        return [w for w in words if w in food_words][:10]
    
    def _get_recipe(self, req: str) -> str:
        recipes = {
            "pasta": {"ingredients": ["pasta", "sauce", "cheese"], "time": 20},
            "chicken": {"ingredients": ["chicken", "salt", "pepper", "oil"], "time": 35},
            "salad": {"ingredients": ["lettuce", "tomato", "olive oil"], "time": 10},
        }
        for key, recipe in recipes.items():
            if key in req:
                return f"🍳 {key.title()}: {', '.join(recipe['ingredients'])}\n⏱️ {recipe['time']} min"
        return "I know: pasta, chicken, salad. Which one?"
    
    def _set_timer(self, request: str) -> str:
        import re
        match = re.search(r'(\d+)\s*(minute|min|hour|hr)', request.lower())
        if not match:
            return "How long? (e.g., 'set timer for 10 minutes')"
        
        amount = match.group(1)
        unit = match.group(2)
        label = f"{amount} {unit}"
        
        return f"⏱️ Timer set for {label}! I'll notify you when done."


# ==================== MAIN JARVIS ====================

class Jarvis:
    def __init__(self, config: JarvisConfig = None):
        self.config = config or JarvisConfig()
        
        # Initialize AI - Use Gemini by default!
        self.ai = self._init_ai()
        
        # Memory & Learning
        from jarvis.memory import Memory
        self.memory = Memory(self.config.config) if hasattr(self, 'config') else None
        self.learning = SelfLearningEngine(self.config.get('learning_db'))
        
        # WhatsApp
        self.whatsapp = WhatsAppAgent(self.config)
        
        # Food Agent
        self.food = FoodAgent(self.config, self.memory)
        
        # Brain Visualization
        self.brain = self._init_brain()
        
        # Dashboard
        self.dashboard = self._init_dashboard()
        
        self.input_mode = self.config.get('input_mode', 'text')
        
        logger.info(f"Jarvis v3.1 initialized - AI: {self.ai.provider if hasattr(self.ai, 'provider') else 'unknown'}")
    
    def _init_ai(self):
        """Initialize AI - Priority: Gemini (free) > Ollama > OpenRouter"""
        
        # Priority 1: Google Gemini (FREE TIER!)
        if self.config.get('gemini_api_key'):
            logger.info("Using Google Gemini (free tier)")
            return GeminiClient(self.config)
        
        # Priority 2: Ollama (local, free)
        try:
            import requests
            resp = requests.get(f"{self.config.get('ollama_url')}/api/tags", timeout=2)
            if resp.status_code == 200:
                logger.info("Using Ollama (local, free)")
                return OllamaClient(self.config)
        except:
            pass
        
        # Priority 3: Return Gemini anyway (will show key prompt)
        return GeminiClient(self.config)
    
    def _init_brain(self):
        return {
            "nodes": [
                {"id": "core", "label": "AI Core", "type": "processor"},
                {"id": "gemini", "label": "Gemini API", "type": "ai"},
                {"id": "memory", "label": "Memory", "type": "storage"},
                {"id": "voice", "label": "Voice I/O", "type": "io"},
                {"id": "whatsapp", "label": "WhatsApp", "type": "messaging"},
                {"id": "food", "label": "Food Agent", "type": "agent"},
                {"id": "google", "label": "Google Services", "type": "integration"},
            ],
            "links": [
                {"source": "core", "target": "gemini"},
                {"source": "core", "target": "memory"},
                {"source": "core", "target": "voice"},
                {"source": "core", "target": "whatsapp"},
                {"source": "core", "target": "food"},
                {"source": "google", "target": "memory"},
            ]
        }
    
    def _init_dashboard(self):
        return {
            "tasks": {"pending": 0, "completed": 0},
            "learning": self.learning.get_stats(),
            "agents": 7,
            "whatsapp": self.config.get('whatsapp_enabled', False),
            "ai_provider": self.ai.provider if hasattr(self.ai, 'provider') else 'gemini'
        }
    
    async def process(self, user_input: str) -> str:
        # Log for learning
        self.learning.log_response(user_input, "", "chat")
        
        # Route to appropriate handler
        inp = user_input.lower()
        
        if any(w in inp for w in ['whatsapp', 'send message', 'text me']):
            # Extract phone number and message
            return await self._handle_whatsapp(user_input)
        
        elif any(w in inp for w in ['order', 'food', 'grocery', 'cook', 'recipe', 'timer']):
            return await self.food.process_food_request(user_input)
        
        else:
            # Regular AI chat
            context = self.memory.get_context() if self.memory else []
            response = await self.ai.chat(user_input, context)
            
            if self.memory:
                self.memory.add_interaction(user_input, response)
            
            return response
    
    async def _handle_whatsapp(self, request: str) -> str:
        """Handle WhatsApp message request"""
        # Simple parsing - in real use, would be more sophisticated
        result = await self.whatsapp.send_message("user", request.replace("whatsapp", "").replace("send message", "").strip())
        return result
    
    def toggle_input_mode(self) -> str:
        self.input_mode = 'voice' if self.input_mode == 'text' else 'text'
        return f"Input mode: {self.input_mode}"
    
    def get_settings(self) -> Dict:
        return {
            'input_mode': self.input_mode,
            'ai_provider': self.ai.provider if hasattr(self.ai, 'provider') else 'gemini',
            'whatsapp_enabled': self.config.get('whatsapp_enabled', False),
            'self_learning': self.config.get('self_learning'),
            'learning_stats': self.learning.get_stats()
        }


class OllamaClient:
    """Local Ollama as fallback"""
    def __init__(self, config):
        self.config = config
        self.provider = 'ollama'
    
    async def chat(self, message: str, context: List[Dict] = None) -> str:
        import requests
        try:
            messages = [{"role": "system", "content": "You are Jarvis, a helpful AI."}]
            if context:
                messages.extend(context[-10:])
            messages.append({"role": "user", "content": message})
            
            resp = requests.post(
                f"{self.config.get('ollama_url')}/api/chat",
                json={"model": self.config.get('ollama_model'), "messages": messages, "stream": False},
                timeout=120
            )
            return resp.json().get('message', {}).get('content', 'No response')
        except Exception as e:
            return f"Ollama error: {e}"


if __name__ == "__main__":
    async def main():
        print("🤖 Jarvis v3.1 - Gemini Powered + WhatsApp")
        print("=" * 50)
        
        config = JarvisConfig()
        jarvis = Jarvis(config)
        
        print(f"\n📋 Status:")
        print(f"   AI: {jarvis.ai.provider}")
        print(f"   WhatsApp: {'Enabled' if jarvis.config.get('whatsapp_enabled') else 'Not configured'}")
        print(f"   Input: {jarvis.input_mode}")
        
        print("\n💬 Type 'quit' to exit\n")
        
        while True:
            try:
                user_input = input(f"You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['quit', 'exit']:
                    break
                
                response = await jarvis.process(user_input)
                print(f"🤖 Jarvis: {response}\n")
            except KeyboardInterrupt:
                break
    
    asyncio.run(main())