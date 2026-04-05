"""
Jarvis Unified - Core Agent Engine
Combines best features from 6 open-source repos into a modular, free AI assistant.
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('jarvis')

class JarvisConfig:
    """Configuration manager supporting .env files"""
    
    def __init__(self, env_file: str = '.env'):
        self.env_file = env_file
        self.config = {}
        self.load_env()
    
    def load_env(self):
        """Load environment variables from .env file"""
        if Path(self.env_file).exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
        
        # Load into config
        self.config = {
            # AI Engine settings
            'model': os.getenv('JARVIS_MODEL', 'gemini-2.0-flash'),
            'api_key': os.getenv('GEMINI_API_KEY', ''),
            'openai_key': os.getenv('OPENAI_API_KEY', ''),
            'anthropic_key': os.getenv('ANTHROPIC_API_KEY', ''),
            
            # Ollama (local, FREE)
            'ollama_url': os.getenv('OLLAMA_URL', 'http://localhost:11434'),
            'ollama_model': os.getenv('OLLAMA_MODEL', 'qwen3:8b'),
            
            # OpenRouter (free models)
            'openrouter_key': os.getenv('OPENROUTER_API_KEY', ''),
            
            # Google services
            'google_client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
            'google_client_secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
            
            # Voice settings
            'tts_engine': os.getenv('TTS_ENGINE', 'pyttsx3'),  # free
            'stt_engine': os.getenv('STT_ENGINE', 'whisper'),  # or whisper
            'elevenlabs_key': os.getenv('ELEVENLABS_API_KEY', ''),
            
            # Wake word (from isair)
            'wake_word_enabled': os.getenv('WAKE_WORD', 'false').lower() == 'true',
            'wake_word_model': os.getenv('WAKE_WORD_MODEL', 'jarvis'),
            
            # Memory
            'memory_db': os.getenv('MEMORY_DB', 'jarvis_memory.db'),
            
            # Server
            'port': int(os.getenv('PORT', '5000')),
            'host': os.getenv('HOST', '0.0.0.0'),
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)


class AIClient:
    """Unified AI client supporting multiple providers"""
    
    def __init__(self, config: JarvisConfig):
        self.config = config
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Initialize the best available AI client"""
        # Priority: Ollama (FREE) > OpenRouter (free tier) > Gemini (free tier) > OpenAI
        
        # Check Ollama first (completely free, local)
        if self._check_ollama():
            logger.info("Using Ollama (local, free)")
            self.provider = 'ollama'
            return
        
        # Check OpenRouter (has free models)
        if self.config.get('openrouter_key'):
            logger.info("Using OpenRouter (free tier available)")
            self.provider = 'openrouter'
            return
        
        # Check Gemini (generous free tier)
        if self.config.get('api_key'):
            logger.info("Using Google Gemini (free tier)")
            self.provider = 'gemini'
            return
        
        # Check OpenAI
        if self.config.get('openai_key'):
            logger.info("Using OpenAI")
            self.provider = 'openai'
            return
        
        logger.warning("No AI provider configured!")
        self.provider = None
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is available locally"""
        try:
            import requests
            resp = requests.get(f"{self.config.get('ollama_url')}/api/tags", timeout=2)
            return resp.status_code == 200
        except:
            return False
    
    async def chat(self, message: str, context: List[Dict] = None) -> str:
        """Send a chat message and get response"""
        if self.provider == 'ollama':
            return await self._ollama_chat(message, context)
        elif self.provider == 'openrouter':
            return await self._openrouter_chat(message, context)
        elif self.provider == 'gemini':
            return await self._gemini_chat(message, context)
        elif self.provider == 'openai':
            return await self._openai_chat(message, context)
        else:
            return "No AI provider configured. Set up Ollama or an API key in .env"
    
    async def _ollama_chat(self, message: str, context: List[Dict] = None) -> str:
        """Chat using local Ollama (FREE)"""
        import requests
        
        model = self.config.get('ollama_model')
        url = f"{self.config.get('ollama_url')}/api/chat"
        
        messages = []
        if context:
            messages.extend(context)
        messages.append({"role": "user", "content": message})
        
        try:
            resp = requests.post(url, json={
                "model": model,
                "messages": messages,
                "stream": False
            }, timeout=120)
            return resp.json().get('message', {}).get('content', 'No response')
        except Exception as e:
            return f"Ollama error: {str(e)}"
    
    async def _openrouter_chat(self, message: str, context: List[Dict] = None) -> str:
        """Chat using OpenRouter (some free models)"""
        import requests
        
        messages = []
        if context:
            messages.extend(context)
        messages.append({"role": "user", "content": message})
        
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.config.get('openrouter_key')}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/jarvis-unified",
                    "X-Title": "Jarvis Unified"
                },
                json={
                    "model": "mistralai/mistral-7b-instruct:free",
                    "messages": messages
                },
                timeout=60
            )
            data = resp.json()
            return data.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
        except Exception as e:
            return f"OpenRouter error: {str(e)}"
    
    async def _gemini_chat(self, message: str, context: List[Dict] = None) -> str:
        """Chat using Google Gemini (free tier)"""
        import requests
        
        try:
            # Build conversation history
            contents = []
            if context:
                for msg in context:
                    contents.append({
                        "role": "user" if msg.get("role") == "user" else "model",
                        "parts": [{"text": msg.get("content", "")}]
                    })
            contents.append({"role": "user", "parts": [{"text": message}]})
            
            resp = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.get('model')}:generateContent",
                params={"key": self.config.get('api_key')},
                json={"contents": contents},
                timeout=60
            )
            data = resp.json()
            return data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No response')
        except Exception as e:
            return f"Gemini error: {str(e)}"
    
    async def _openai_chat(self, message: str, context: List[Dict] = None) -> str:
        """Chat using OpenAI"""
        import requests
        
        messages = []
        if context:
            messages.extend(context)
        messages.append({"role": "user", "content": message})
        
        try:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.config.get('openai_key')}"},
                json={"model": "gpt-3.5-turbo", "messages": messages},
                timeout=60
            )
            data = resp.json()
            return data.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
        except Exception as e:
            return f"OpenAI error: {str(e)}"


class Jarvis:
    """Main Jarvis assistant class"""
    
    def __init__(self, config: JarvisConfig = None):
        self.config = config or JarvisConfig()
        self.ai = AIClient(self.config)
        self.memory = None
        self.tools = None
        logger.info("Jarvis initialized")
    
    async def process(self, user_input: str) -> str:
        """Process user input and return response"""
        # Get context from memory
        context = self._get_context()
        
        # Get AI response
        response = await self.ai.chat(user_input, context)
        
        # Save to memory
        self._save_interaction(user_input, response)
        
        return response
    
    def _get_context(self) -> List[Dict]:
        """Get conversation context from memory"""
        # This would be implemented by the memory module
        return []
    
    def _save_interaction(self, user: str, assistant: str):
        """Save interaction to memory"""
        # This would be implemented by the memory module
        pass


# Main entry point
if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("🤖 Jarvis Unified - Starting...")
        
        config = JarvisConfig()
        jarvis = Jarvis(config)
        
        print(f"\n📋 Configuration:")
        print(f"   AI Provider: {jarvis.ai.provider or 'None'}")
        print(f"   Ollama Model: {config.get('ollama_model')}")
        print(f"   Port: {config.get('port')}")
        
        print("\n💬 Type 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                response = await jarvis.process(user_input)
                print(f"Jarvis: {response}\n")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")
    
    asyncio.run(main())