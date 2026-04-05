"""
Jarvis Unified - Enhanced Core Engine v2
100% Free, modular, local-first AI assistant
"""

import os
import json
import logging
import asyncio
from typing import Optional, Dict, Any, List
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('jarvis')

class JarvisConfig:
    """Enhanced configuration with all user preferences"""
    
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
            # === AI - 100% FREE ===
            'ai_provider': os.getenv('AI_PROVIDER', 'ollama'),
            'ollama_url': os.getenv('OLLAMA_URL', 'http://localhost:11434'),
            'ollama_model': os.getenv('OLLAMA_MODEL', 'qwen3:8b'),
            'openrouter_key': os.getenv('OPENROUTER_API_KEY', ''),
            'gemini_api_key': os.getenv('GEMINI_API_KEY', ''),
            'gemini_model': os.getenv('GEMINI_MODEL', 'gemini-2.0-flash'),
            
            # === Voice ===
            'tts_engine': os.getenv('TTS_ENGINE', 'pyttsx3'),
            'stt_engine': os.getenv('STT_ENGINE', 'whisper'),
            'elevenlabs_key': os.getenv('ELEVENLABS_API_KEY', ''),
            'wake_word': os.getenv('WAKE_WORD', 'Jarvis').lower(),
            'custom_wake_commands': self._parse_list(os.getenv('CUSTOM_WAKE_COMMANDS', '')),
            
            # === Audio Input ===
            'microphone': os.getenv('MICROPHONE', 'default'),
            'headset': os.getenv('HEADSET', 'default'),
            'camera': os.getenv('CAMERA', 'default'),
            
            # === Tone ===
            'jarvis_tone': os.getenv('JARVIS_TONE', 'helpful'),  # humorous, sassy, formal, helpful
            'jarvis_name': os.getenv('JARVIS_NAME', 'Jarvis'),
            
            # === Screen Share ===
            'screen_share_enabled': os.getenv('SCREEN_SHARE', 'false').lower() == 'true',
            
            # === Memory & Learning ===
            'memory_db': os.getenv('MEMORY_DB', 'jarvis_memory.db'),
            'learn_gestures': os.getenv('LEARN_GESTURES', 'true').lower() == 'true',
            'learn_preferences': os.getenv('LEARN_PREFERENCES', 'true').lower() == 'true',
            
            # === Google Services ===
            'google_client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
            'google_client_secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
            'google_refresh_token': os.getenv('GOOGLE_REFRESH_TOKEN', ''),
            
            # === Browser Control ===
            'default_browser': os.getenv('DEFAULT_BROWSER', 'chrome'),
            'chrome_path': os.getenv('CHROME_PATH', ''),
            'edge_path': os.getenv('EDGE_PATH', ''),
            
            # === Automation ===
            'auto_emails_enabled': os.getenv('AUTO_EMAILS', 'false').lower() == 'true',
            'email_schedule': os.getenv('EMAIL_SCHEDULE', '07:00,19:00'),
            'github_repo': os.getenv('GITHUB_REPO', ''),
            'github_token': os.getenv('GITHUB_TOKEN', ''),
            
            # === UI ===
            'port': int(os.getenv('PORT', '5000')),
            'theme': os.getenv('THEME', 'dark'),
            'accent_color': os.getenv('ACCENT_COLOR', '#3b82f6'),
            'show_speech_visual': os.getenv('SHOW_SPEECH_VISUAL', 'true').lower() == 'true',
        }
    
    def _parse_list(self, s: str) -> List[str]:
        return [x.strip() for x in s.split(',') if x.strip()]
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)


class ToneManager:
    """Manage Jarvis's tone/personality"""
    
    TONES = {
        'helpful': "You are Jarvis, a helpful and efficient AI assistant. Be concise and practical.",
        'humorous': "You are Jarvis, a witty and humorous AI assistant. Add personality, jokes, and fun observations while being helpful.",
        'sassy': "You are Jarvis, a sassy but helpful AI assistant. Be direct, a bit witty, and don't sugarcoat things.",
        'formal': "You are Jarvis, a professional and formal AI assistant. Be precise, thorough, and courteous.",
        'friendly': "You are Jarvis, a friendly and warm AI assistant. Be conversational, use light language, and show genuine interest.",
        'minimal': "You are Jarvis, a minimal and direct AI assistant. Keep responses short and to the point.",
    }
    
    @classmethod
    def get_system_prompt(cls, tone: str) -> str:
        base = cls.TONES.get(tone, cls.TONES['helpful'])
        return base + " Always remember user preferences and adapt to their communication style."


class AIClient:
    """Unified AI client - prioritizes FREE options"""
    
    def __init__(self, config: JarvisConfig):
        self.config = config
        self.provider = None
        self._init_provider()
    
    def _init_provider(self):
        provider = self.config.get('ai_provider', 'ollama').lower()
        
        # Priority: Ollama (FREE local) > OpenRouter (free tier) > Gemini (free tier)
        if provider == 'ollama' and self._check_ollama():
            self.provider = 'ollama'
            logger.info("Using Ollama (100% FREE local)")
            return
        
        if provider == 'openrouter' and self.config.get('openrouter_key'):
            self.provider = 'openrouter'
            logger.info("Using OpenRouter (free tier)")
            return
        
        if provider == 'gemini' and self.config.get('gemini_api_key'):
            self.provider = 'gemini'
            logger.info("Using Google Gemini (free tier)")
            return
        
        # Fallback to Ollama if available
        if self._check_ollama():
            self.provider = 'ollama'
            logger.info("Fallback to Ollama")
            return
        
        logger.warning("No free AI provider available!")
    
    def _check_ollama(self) -> bool:
        try:
            import requests
            resp = requests.get(f"{self.config.get('ollama_url')}/api/tags", timeout=2)
            return resp.status_code == 200
        except:
            return False
    
    async def chat(self, message: str, context: List[Dict] = None) -> str:
        tone = self.config.get('jarvis_tone', 'helpful')
        system_prompt = ToneManager.get_system_prompt(tone)
        
        if self.provider == 'ollama':
            return await self._ollama_chat(message, context, system_prompt)
        elif self.provider == 'openrouter':
            return await self._openrouter_chat(message, context, system_prompt)
        elif self.provider == 'gemini':
            return await self._gemini_chat(message, context, system_prompt)
        return "No AI provider. Install Ollama (https://ollama.com) for 100% free usage."
    
    async def _ollama_chat(self, message: str, context: List[Dict], system_prompt: str) -> str:
        import requests
        messages = [{"role": "system", "content": system_prompt}]
        if context:
            messages.extend(context[-10:])
        messages.append({"role": "user", "content": message})
        
        try:
            resp = requests.post(
                f"{self.config.get('ollama_url')}/api/chat",
                json={"model": self.config.get('ollama_model'), "messages": messages, "stream": False},
                timeout=120
            )
            return resp.json().get('message', {}).get('content', 'No response')
        except Exception as e:
            return f"Ollama error: {e}"
    
    async def _openrouter_chat(self, message: str, context: List[Dict], system_prompt: str) -> str:
        import requests
        messages = [{"role": "system", "content": system_prompt}]
        if context:
            messages.extend(context[-10:])
        messages.append({"role": "user", "content": message})
        
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.config.get('openrouter_key')}", "Content-Type": "application/json"},
                json={"model": "mistralai/mistral-7b-instruct:free", "messages": messages},
                timeout=60
            )
            return resp.json().get('choices', [{}])[0].get('message', {}).get('content', 'No response')
        except Exception as e:
            return f"OpenRouter error: {e}"
    
    async def _gemini_chat(self, message: str, context: List[Dict], system_prompt: str) -> str:
        import requests
        contents = [{"role": "user", "parts": [{"text": system_prompt}]}]
        if context:
            for msg in context[-10:]:
                contents.append({"role": msg.get("role", "user"), "parts": [{"text": msg.get("content", "")}]})
        contents.append({"role": "user", "parts": [{"text": message}]})
        
        try:
            resp = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.get('gemini_model')}:generateContent",
                params={"key": self.config.get('gemini_api_key')},
                json={"contents": contents},
                timeout=60
            )
            return resp.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No response')
        except Exception as e:
            return f"Gemini error: {e}"


class Jarvis:
    """Main Jarvis assistant with all features"""
    
    def __init__(self, config: JarvisConfig = None):
        self.config = config or JarvisConfig()
        self.ai = AIClient(self.config)
        self.memory = None
        self.automation = None
        self.google = None
        self.voice = None
        self.browser = None
        self.gestures = {}
        self.screen_sharing = False
        logger.info(f"Jarvis v2 initialized - Tone: {self.config.get('jarvis_tone')}")
    
    async def process(self, user_input: str) -> str:
        context = self._get_context()
        response = await self.ai.chat(user_input, context)
        self._save_interaction(user_input, response)
        
        # Learn from user
        if self.config.get('learn_preferences'):
            self._learn_preferences(user_input, response)
        
        return response
    
    def _get_context(self) -> List[Dict]:
        if self.memory:
            return self.memory.context.get_context()
        return []
    
    def _save_interaction(self, user: str, assistant: str):
        if self.memory:
            self.memory.add_interaction(user, assistant)
    
    def _learn_preferences(self, user_input: str, response: str):
        """Learn user preferences from interactions"""
        if not self.memory:
            return
        
        # Extract potential preferences
        lower_input = user_input.lower()
        
        if 'i prefer' in lower_input or 'i like' in lower_input or 'i hate' in lower_input:
            # Store as preference
            self.memory.store.set_preference('last_preference', user_input)
        
        # Learn communication style
        if 'be more' in lower_input or 'stop being' in lower_input:
            self.memory.store.set_preference('tone_feedback', user_input)
    
    def toggle_screen_share(self):
        self.screen_sharing = not self.screen_sharing
        return self.screen_sharing
    
    def add_gesture(self, name: str, action: str):
        self.gestures[name] = action
        logger.info(f"Learned gesture: {name} -> {action}")
    
    def get_settings(self) -> Dict:
        return {
            'tone': self.config.get('jarvis_tone'),
            'name': self.config.get('jarvis_name'),
            'wake_word': self.config.get('wake_word'),
            'custom_wakes': self.config.get('custom_wake_commands'),
            'screen_share': self.screen_sharing,
            'microphone': self.config.get('microphone'),
            'camera': self.config.get('camera'),
            'theme': self.config.get('theme'),
            'accent_color': self.config.get('accent_color'),
            'gestures': list(self.gestures.keys()),
            'ai_provider': self.provider if hasattr(self, 'provider') else self.ai.provider,
        }
    
    def update_setting(self, key: str, value: Any):
        self.config.config[key] = value
        logger.info(f"Updated setting: {key} = {value}")


if __name__ == "__main__":
    async def main():
        print("🤖 Jarvis v2 - 100% Free AI Assistant")
        print("=" * 40)
        
        config = JarvisConfig()
        jarvis = Jarvis(config)
        
        print(f"\n📋 Settings:")
        print(f"   AI: {jarvis.ai.provider or 'None'}")
        print(f"   Tone: {config.get('jarvis_tone')}")
        print(f"   Wake: {config.get('wake_word')}")
        print(f"   Theme: {config.get('theme')}")
        
        print("\n💬 Type 'settings' to see all config, 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['quit', 'exit']:
                    print("👋")
                    break
                if user_input.lower() == 'settings':
                    print(json.dumps(jarvis.get_settings(), indent=2))
                    continue
                
                response = await jarvis.process(user_input)
                print(f"Jarvis: {response}\n")
            except KeyboardInterrupt:
                break
    
    asyncio.run(main())