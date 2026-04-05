#!/usr/bin/env python3
"""
Jarvis Unified - Main Entry Point
Run with: python main.py
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# Add jarvis to path
sys.path.insert(0, str(Path(__file__).parent))

from jarvis.core.jarvis import JarvisConfig, Jarvis
from jarvis.voice import VoiceInterface
from jarvis.memory import Memory
from jarvis.automation import AutomationEngine
from jarvis.api.google_services import GoogleServices
from jarvis.ui.web_ui import JarvisWebUI


def parse_args():
    parser = argparse.ArgumentParser(description='🤖 Jarvis Unified AI Assistant')
    parser.add_argument('--config', '-c', default='.env', help='Config file path')
    parser.add_argument('--web', '-w', action='store_true', help='Start web UI')
    parser.add_argument('--port', '-p', type=int, default=5000, help='Web UI port')
    parser.add_argument('--voice', '-v', action='store_true', help='Start voice interface')
    parser.add_argument('--model', '-m', help='Override AI model')
    parser.add_argument('--local', action='store_true', help='Force local (Ollama) mode')
    return parser.parse_args()


async def main():
    args = parse_args()
    
    print("🤖 Jarvis Unified AI System")
    print("=" * 40)
    
    # Load configuration
    config = JarvisConfig(args.config)
    
    # Override with CLI args
    if args.model:
        config.config['ollama_model'] = args.model
    if args.local:
        config.config['model'] = 'ollama'
    
    # Initialize components
    print("\n📦 Initializing components...")
    
    # Memory
    memory = Memory(config.config)
    print("   ✅ Memory system")
    
    # Automation
    automation = AutomationEngine(config.config)
    print("   ✅ Automation engine")
    
    # Google Services
    google = GoogleServices(config.config)
    print("   ✅ Google services")
    
    # Main Jarvis
    jarvis = Jarvis(config)
    jarvis.memory = memory
    jarvis.automation = automation
    print("   ✅ AI engine")
    
    # Show config
    print(f"\n📋 Configuration:")
    print(f"   AI Provider: {jarvis.ai.provider or 'Not configured'}")
    if jarvis.ai.provider == 'ollama':
        print(f"   Model: {config.get('ollama_model')}")
    print(f"   Port: {args.port}")
    
    # Determine mode
    if args.web:
        print(f"\n🌐 Starting web UI on http://localhost:{args.port}")
        ui = JarvisWebUI(jarvis, config.config)
        ui.run(port=args.port)
    else:
        # Interactive mode
        print("\n💬 Interactive Mode")
        print("   Type 'quit' to exit, 'web' to start web UI")
        print("   Type 'voice' to start voice mode\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'web':
                    print(f"\n🌐 Starting web UI on http://localhost:{args.port}")
                    ui = JarvisWebUI(jarvis, config.config)
                    ui.run(port=args.port)
                    break
                
                if user_input.lower() == 'voice':
                    print("\n🎤 Voice mode not fully implemented yet")
                    continue
                
                response = await jarvis.process(user_input)
                print(f"Jarvis: {response}\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")
    
    # Cleanup
    memory.close()


if __name__ == "__main__":
    asyncio.run(main())