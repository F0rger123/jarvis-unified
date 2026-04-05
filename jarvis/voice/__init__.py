"""
Voice Module - TTS and STT
Combines features from isair, Mark-XXXV, and taskmaster
"""

import os
import asyncio
import logging
from typing import Optional

logger = logging.getLogger('jarvis.voice')

class TTSEngine:
    """Text-to-Speech engine with multiple backends"""
    
    def __init__(self, config: dict):
        self.config = config
        self.engine = config.get('tts_engine', 'pyttsx3')
    
    def speak(self, text: str, blocking: bool = True):
        """Convert text to speech"""
        if self.engine == 'pyttsx3':
            self._pyttsx3_speak(text)
        elif self.engine == 'elevenlabs':
            self._elevenlabs_speak(text)
        elif self.engine == 'gtts':
            self._gtts_speak(text)
        else:
            logger.warning(f"Unknown TTS engine: {self.engine}")
    
    def _pyttsx3_speak(self, text: str):
        """Free TTS using pyttsx3 (offline)"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            logger.error(f"pyttsx3 error: {e}")
    
    def _elevenlabs_speak(self, text: str):
        """Premium TTS - requires API key"""
        api_key = self.config.get('elevenlabs_key')
        if not api_key:
            logger.warning("ElevenLabs key not set, falling back to pyttsx3")
            return self._pyttsx3_speak(text)
        
        try:
            import requests
            # Using ElevenLabs TTS API
            # This is a placeholder - actual implementation would call their API
            logger.info("ElevenLabs TTS not fully implemented")
        except Exception as e:
            logger.error(f"ElevenLabs error: {e}")
    
    def _gtts_speak(self, text: str):
        """Google TTS (free but requires internet)"""
        try:
            from gtts import gTTS
            import pygame
            import tempfile
            import os
            
            tts = gTTS(text=text)
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                tts.save(f.name)
                pygame.mixer.init()
                pygame.mixer.music.load(f.name)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                os.unlink(f.name)
        except Exception as e:
            logger.error(f"gTTS error: {e}")


class STTEngine:
    """Speech-to-Text engine with multiple backends"""
    
    def __init__(self, config: dict):
        self.config = config
        self.engine = config.get('stt_engine', 'whisper')
    
    async def listen(self, audio_data: bytes = None) -> str:
        """Convert speech to text"""
        if self.engine == 'whisper':
            return await self._whisper_listen(audio_data)
        elif self.engine == 'google':
            return await self._google_listen(audio_data)
        else:
            return ""
    
    async def _whisper_listen(self, audio_data: bytes = None) -> str:
        """Local Whisper STT (FREE)"""
        try:
            # Would use faster-whisper for better performance
            logger.info("Whisper STT - requires audio input")
            return ""
        except Exception as e:
            logger.error(f"Whisper error: {e}")
            return ""
    
    async def _google_listen(self, audio_data: bytes = None) -> str:
        """Google Speech-to-Text (free tier)"""
        logger.info("Google STT - requires audio input and credentials")
        return ""


class WakeWordDetector:
    """Wake word detection - from isair/jarvis"""
    
    def __init__(self, config: dict):
        self.config = config
        self.enabled = config.get('wake_word_enabled', False)
        self.model_path = config.get('wake_word_model', 'jarvis')
        self.detector = None
    
    async def start_listening(self):
        """Start listening for wake word"""
        if not self.enabled:
            logger.info("Wake word detection disabled")
            return
        
        logger.info(f"Starting wake word detection for: {self.model_path}")
        # Implementation would use openwakeword or similar
        # For now, this is a placeholder
    
    def detect(self, audio_chunk: bytes) -> bool:
        """Check if wake word is present in audio"""
        # Placeholder - would use actual wake word model
        return False


class VoiceInterface:
    """Complete voice interface combining TTS, STT, and wake word"""
    
    def __init__(self, config: dict):
        self.config = config
        self.tts = TTSEngine(config)
        self.stt = STTEngine(config)
        self.wake_word = WakeWordDetector(config)
        self.is_listening = False
    
    async def start(self):
        """Start the voice interface"""
        await self.wake_word.start_listening()
        self.is_listening = True
        logger.info("Voice interface started")
    
    async def process_voice_input(self, audio: bytes) -> Optional[str]:
        """Process voice input and return text"""
        if self.wake_word.detect(audio):
            logger.info("Wake word detected!")
            return await self.stt.listen(audio)
        return None
    
    def speak(self, text: str):
        """Speak text to user"""
        self.tts.speak(text)
    
    def stop(self):
        """Stop the voice interface"""
        self.is_listening = False
        logger.info("Voice interface stopped")