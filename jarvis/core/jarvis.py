"""
Jarvis Unified v3.3 - Multi-Model Support + Gemma 4 Code Brain
Google Gemini 3.1 Flash Lite default + model switching
"""

import os
import json
import logging
import asyncio
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime
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
        
        # Available FREE models with their specs
        FREE_MODELS = {
            # Google Gemini (best free tier!)
            'gemini-3.1-flash-lite': {
                'name': 'Gemini 3.1 Flash Lite',
                'provider': 'google',
                'rate_limit': '15 RPM',
                'context': '32K',
                'description': 'FASTEST - Best for general use',
                'code_capable': False
            },
            'gemini-2.0-flash': {
                'name': 'Gemini 2.0 Flash',
                'provider': 'google',
                'rate_limit': '15 RPM',
                'context': '32K',
                'description': 'Balanced speed and quality',
                'code_capable': True
            },
            'gemini-2.0-flash-lite': {
                'name': 'Gemini 2.0 Flash Lite',
                'provider': 'google',
                'rate_limit': '15 RPM',
                'context': '32K',
                'description': 'Most economical',
                'code_capable': False
            },
            # Gemma 4 - Google's latest!
            'gemma-4-2b-it': {
                'name': 'Gemma 4 2B (Instruction Tuned)',
                'provider': 'google',
                'rate_limit': '15 RPM',
                'context': '8K',
                'description': '⚡ LIGHTNING FAST - Great for code!',
                'code_capable': True,
                'special': 'code_brain'
            },
            'gemma-4-9b-it': {
                'name': 'Gemma 4 9B (Instruction Tuned)',
                'provider': 'google',
                'rate_limit': '15 RPM',
                'context': '8K',
                'description': '🧠 POWERFUL - Best for complex tasks',
                'code_capable': True,
                'special': 'code_brain'
            },
            # OpenRouter free models
            'mistralai/mistral-7b-instruct:free': {
                'name': 'Mistral 7B (Free)',
                'provider': 'openrouter',
                'rate_limit': 'Varies',
                'context': '8K',
                'description': 'Solid all-rounder',
                'code_capable': True
            },
            'meta-llama/llama-3.1-8b-instruct:free': {
                'name': 'Llama 3.1 8B (Free)',
                'provider': 'openrouter',
                'rate_limit': 'Varies',
                'context': '8K',
                'description': 'Meta\'s best free model',
                'code_capable': True
            },
            # Ollama (local)
            'ollama': {
                'name': 'Ollama (Local)',
                'provider': 'local',
                'rate_limit': 'Unlimited',
                'context': 'Varies',
                'description': '🔒 100% Private - Runs on your machine',
                'code_capable': True,
                'requires': 'ollama_running'
            }
        }
        
        self.config = {
            # === AI PROVIDER ===
            'ai_provider': os.getenv('AI_PROVIDER', 'gemini'),
            
            # === GEMINI MODELS ===
            'gemini_api_key': os.getenv('GEMINI_API_KEY', ''),
            'gemini_model': os.getenv('GEMINI_MODEL', 'gemini-3.1-flash-lite'),  # DEFAULT!
            
            # === CODE BRAIN - Gemma 4 ===
            'gemma_4_code_brain': os.getenv('GEMINI_MODEL', 'gemma-4-9b-it'),  # Use for code!
            'use_gemma_for_code': os.getenv('USE_GEMMA_FOR_CODE', 'true').lower() == 'true',
            
            # === OPENROUTER (fallback) ===
            'openrouter_key': os.getenv('OPENROUTER_API_KEY', ''),
            'openrouter_model': os.getenv('OPENROUTER_MODEL', 'mistralai/mistral-7b-instruct:free'),
            
            # === OLLAMA (local fallback) ===
            'ollama_url': os.getenv('OLLAMA_URL', 'http://localhost:11434'),
            'ollama_model': os.getenv('OLLAMA_MODEL', 'qwen3:8b'),
            
            # === VOICE ===
            'tts_engine': os.getenv('TTS_ENGINE', 'pyttsx3'),
            'input_mode': os.getenv('INPUT_MODE', 'text'),
            
            # === UI ===
            'ui_theme': os.getenv('UI_THEME', 'tron'),
            'accent_color': os.getenv('ACCENT_COLOR', '#00ffff'),
            
            # === TONE ===
            'jarvis_tone': os.getenv('JARVIS_TONE', 'helpful'),
            
            # === LEARNING ===
            'self_learning': os.getenv('SELF_LEARNING', 'true').lower() == 'true',
            
            # === WHATSAPP ===
            'whatsapp_enabled': os.getenv('WHATSAPP_ENABLED', 'false').lower() == 'true',
            'twilio_account_sid': os.getenv('TWILIO_ACCOUNT_SID', ''),
            'twilio_auth_token': os.getenv('TWILIO_AUTH_TOKEN', ''),
            'twilio_phone_number': os.getenv('TWILIO_PHONE_NUMBER', ''),
            
            # === SECURITY ===
            'confirm_payments': os.getenv('CONFIRM_PAYMENTS', 'true').lower() == 'true',
            'confirm_whatsapp': os.getenv('CONFIRM_WHATSAPP', 'true').lower() == 'true',
            
            # === AVAILABLE MODELS (for UI) ===
            'available_models': FREE_MODELS,
            
            # === SERVER ===
            'port': int(os.getenv('PORT', '5000')),
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)


# ==================== AI CLIENT ====================

class AIClient:
    """Multi-model AI client - switch between free models"""
    
    def __init__(self, config: JarvisConfig):
        self.config = config
        self.current_model = config.get('gemini_model', 'gemini-3.1-flash-lite')
        self.api_key = config.get('gemini_api_key')
        self.provider = 'gemini'
        
        # Check what we can use
        self._init_available_models()
    
    def _init_available_models(self):
        """Check which models are available"""
        self.available = []
        
        # Check Gemini
        if self.api_key:
            self.available.append('gemini')
            logger.info("✅ Gemini API available")
        
        # Check Ollama
        try:
            resp = requests.get(f"{self.config.get('ollama_url')}/api/tags", timeout=2)
            if resp.status_code == 200:
                self.available.append('ollama')
                logger.info("✅ Ollama (local) available")
        except:
            pass
        
        # Check OpenRouter (if key provided)
        if self.config.get('openrouter_key'):
            self.available.append('openrouter')
            logger.info("✅ OpenRouter available")
        
        if not self.available:
            logger.warning("⚠️ No AI providers available!")
    
    def switch_model(self, model_name: str) -> str:
        """Switch to a different model"""
        self.current_model = model_name
        logger.info(f"Switched to model: {model_name}")
        return f"Switched to {model_name}"
    
    async def chat(self, message: str, context: List[Dict] = None, use_code_brain: bool = False) -> str:
        """Send chat - can use Gemma 4 for code tasks"""
        
        # If code task and Gemma for code enabled, use Gemma 4
        if use_code_brain and self.config.get('use_gemma_for_code'):
            # Try to use Gemma 4 for code
            code_model = self.config.get('gemma_4_code_brain', 'gemma-4-9b-it')
            if 'gemma' in code_model.lower():
                logger.info(f"Using Gemma 4 for code task: {code_model}")
                return await self._call_gemini(message, context, code_model)
        
        # Regular chat - use current model
        return await self._call_gemini(message, context, self.current_model)
    
    async def _call_gemini(self, message: str, context: List[Dict], model: str) -> str:
        """Call Gemini API"""
        
        if not self.api_key:
            return "⚠️ No API key. Get free key: https://aistudio.google.com/app/apikey"
        
        try:
            contents = []
            if context:
                for msg in context[-10:]:
                    contents.append({
                        "role": "model" if msg.get("role") == "assistant" else "user",
                        "parts": [{"text": msg.get("content", "")}]
                    })
            
            contents.append({"role": "user", "parts": [{"text": message}]})
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            
            resp = requests.post(
                url,
                params={"key": self.api_key},
                json={"contents": contents},
                timeout=60
            )
            
            if resp.status_code == 200:
                data = resp.json()
                response = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                return response if response else "No response"
            else:
                return f"API Error {resp.status_code}"
                
        except Exception as e:
            return f"Error: {e}"
    
    async def code_task(self, code_request: str, context: List[Dict] = None) -> str:
        """Use Gemma 4 specifically for code tasks"""
        return await self.chat(code_request, context, use_code_brain=True)
    
    def get_available_models(self) -> List[Dict]:
        """Get list of available models for UI"""
        models = self.config.get('available_models', {})
        
        # Filter to only show models user has access to
        available = []
        
        for model_id, info in models.items():
            # Check if we have credentials
            can_use = False
            
            if info.get('provider') == 'google' and self.api_key:
                can_use = True
            elif info.get('provider') == 'local' and 'ollama' in self.available:
                can_use = True
            elif info.get('provider') == 'openrouter' and self.config.get('openrouter_key'):
                can_use = True
            
            if can_use:
                available.append({
                    'id': model_id,
                    'name': info.get('name'),
                    'description': info.get('description'),
                    'rate_limit': info.get('rate_limit'),
                    'context': info.get('context'),
                    'code_capable': info.get('code_capable', False),
                    'is_code_brain': info.get('special') == 'code_brain'
                })
        
        return available


# ==================== MAIN JARVIS ====================

class Jarvis:
    def __init__(self, config: JarvisConfig = None):
        self.config = config or JarvisConfig()
        
        # Initialize AI
        self.ai = AIClient(self.config)
        
        # Memory & Learning
        from memory import Memory
        self.memory = Memory(self.config.config) if hasattr(self, 'config') else None
        self.learning = SelfLearningEngine(self.config.get('learning_db', 'jarvis_learning.json'))
        
        # WhatsApp
        self.whatsapp = WhatsAppAgent(self.config)
        
        # Brain Viz
        self.brain = {
            "nodes": [
                {"id": "core", "label": "AI Core", "type": "processor"},
                {"id": "gemini-3.1", "label": "Gemini 3.1 Flash Lite", "type": "ai", "default": True},
                {"id": "gemma-4", "label": "Gemma 4 (Code Brain)", "type": "ai", "special": "code"},
                {"id": "ollama", "label": "Ollama (Local)", "type": "ai"},
                {"id": "memory", "label": "Memory", "type": "storage"},
                {"id": "whatsapp", "label": "WhatsApp", "type": "messaging"},
            ],
            "links": [
                {"source": "core", "target": "gemini-3.1"},
                {"source": "core", "target": "gemma-4"},
                {"source": "core", "target": "memory"},
                {"source": "core", "target": "whatsapp"},
            ]
        }
        
        self.input_mode = self.config.get('input_mode', 'text')
        
        logger.info(f"Jarvis v3.3 - Default: Gemini 3.1 Flash Lite, Code Brain: Gemma 4")
    
    async def process(self, user_input: str, use_code_brain: bool = False) -> str:
        """Process with optional code brain mode"""
        
        # Detect if it's a code task
        code_keywords = ['code', 'program', 'function', 'script', 'debug', 'fix', 'write code', 'create app']
        is_code_task = any(kw in user_input.lower() for kw in code_keywords)
        
        # Auto-use code brain for code tasks
        if is_code_task and self.config.get('use_gemma_for_code'):
            use_code_brain = True
        
        self.learning.log_response(user_input, "", "chat")
        
        # Route
        inp = user_input.lower()
        
        if any(w in inp for w in ['whatsapp', 'send message']):
            return await self.whatsapp.send_message("user", user_input)
        
        # Get context
        context = self.memory.get_context() if self.memory else []
        
        # Chat with AI (using code brain if needed)
        response = await self.ai.chat(user_input, context, use_code_brain=use_code_brain)
        
        if self.memory:
            self.memory.add_interaction(user_input, response)
        
        return response
    
    def switch_model(self, model_id: str) -> str:
        """Switch the active model"""
        return self.ai.switch_model(model_id)
    
    def get_settings(self) -> Dict:
        return {
            'current_model': self.ai.current_model,
            'available_models': self.ai.get_available_models(),
            'gemma_4_code_brain': self.config.get('gemma_4_code_brain'),
            'use_gemma_for_code': self.config.get('use_gemma_for_code'),
            'input_mode': self.input_mode
        }
    
    def toggle_input_mode(self) -> str:
        self.input_mode = 'voice' if self.input_mode == 'text' else 'text'
        return f"Input: {self.input_mode}"


# ==================== SELF-LEARNING ====================

class SelfLearningEngine:
    def __init__(self, db_file: str = "jarvis_learning.json"):
        self.db_file = db_file
        self.data = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {"responses": [], "grades": []}
    
    def log_response(self, prompt: str, response: str, context: str = ""):
        self.data.setdefault('responses', []).append({
            "id": len(self.data.get('responses', [])),
            "prompt": prompt[:200], "response": response[:500],
            "timestamp": datetime.now().isoformat()
        })
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f)
    
    def grade_response(self, response_id: int, grade: int, feedback: str = ""):
        self.data.setdefault('grades', []).append({"grade": grade, "timestamp": datetime.now().isoformat()})
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f)
    
    def get_stats(self) -> Dict:
        grades = self.data.get('grades', [])
        if not grades:
            return {"total_responses": 0, "avg_grade": 0}
        return {"total_responses": len(self.data.get('responses', [])), "avg_grade": round(sum(g['grade'] for g in grades)/len(grades), 1)}


# ==================== WHATSAPP ====================

class WhatsAppAgent:
    def __init__(self, config: JarvisConfig):
        self.config = config
        self.enabled = config.get('whatsapp_enabled', False)
    
    async def send_message(self, to: str, message: str) -> str:
        if self.config.get('confirm_whatsapp', True):
            return f"⚠️ Confirm WhatsApp to {to}:\n\n{message}\n\nReply 'yes' to confirm"
        
        if not (self.config.get('twilio_account_sid') or self.config.get('whatsapp_enabled')):
            return "WhatsApp not configured. Add credentials in Settings."
        
        return "WhatsApp configured but sending requires Twilio/WhatsApp API setup."


if __name__ == "__main__":
    async def main():
        print("🤖 Jarvis v3.3")
        print("=" * 50)
        
        config = JarvisConfig()
        jarvis = Jarvis(config)
        
        models = jarvis.get_settings()['available_models']
        
        print(f"\n📋 AI Models Available:")
        for m in models:
            brain = " 🧠 CODE BRAIN" if m.get('is_code_brain') else ""
            print(f"   • {m['name']} ({m['rate_limit']}){brain}")
        
        print(f"\n⚡ Current: {jarvis.ai.current_model}")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if not user_input or user_input.lower() in ['quit', 'exit']:
                    break
                
                response = await jarvis.process(user_input)
                print(f"🤖: {response}")
            except KeyboardInterrupt:
                break
    
    asyncio.run(main())