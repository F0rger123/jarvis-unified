#!/usr/bin/env python3
"""
Jarvis Unified v3 - Main Entry Point
Tron UI + Food Agent + Self-Learning + SMS + Brain Viz
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from jarvis.core.jarvis import JarvisConfig, Jarvis

def parse_args():
    parser = argparse.ArgumentParser(description='🤖 Jarvis v3 - Tron UI')
    parser.add_argument('--config', '-c', default='.env', help='Config file')
    parser.add_argument('--web', '-w', action='store_true', help='Start web UI')
    parser.add_argument('--port', '-p', type=int, default=5000, help='Port')
    return parser.parse_args()


async def main():
    args = parse_args()
    
    print("🤖 Jarvis v3 - TRON EDITION")
    print("=" * 40)
    print("⚡ Self-Learning  🍔 Food Agent  🧠 Brain Viz")
    print("📱 SMS via Gmail  🔒 Secure Confirmations")
    print("=" * 40)
    
    # Load config
    os.chdir(Path(__file__).parent / 'jarvis')
    config = JarvisConfig(args.config)
    
    # Initialize Jarvis
    jarvis = Jarvis(config)
    
    print(f"\n📋 Status:")
    print(f"   Theme: {config.get('ui_theme')}")
    print(f"   Input: {jarvis.input_mode}")
    print(f"   Learning: {config.get('self_learning')}")
    print(f"   Brain Viz: {config.get('brain_viz')}")
    print(f"   AI: {jarvis.ai.provider}")
    
    if args.web:
        from jarvis.ui.web_ui import JarvisTronUI
        print(f"\n🌐 Starting TRON UI on http://localhost:{args.port}")
        ui = JarvisTronUI(jarvis, config.config)
        ui.run(port=args.port)
    else:
        print("\n💬 Interactive Mode")
        print("   Commands: 'mode' (toggle text/voice), 'brain', 'dash', 'quit'\n")
        
        while True:
            try:
                user_input = input(f"{'🎤' if jarvis.input_mode == 'voice' else '⌨️'} You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['quit', 'exit']:
                    print("👋")
                    break
                if user_input.lower() == 'mode':
                    print(jarvis.toggle_input_mode())
                    continue
                if user_input.lower() == 'brain':
                    import json
                    print(json.dumps(jarvis.brain.get_brain_data(), indent=2))
                    continue
                if user_input.lower() == 'dash':
                    import json
                    print(json.dumps(jarvis.dashboard.get_data(), indent=2))
                    continue
                
                response = await jarvis.process(user_input)
                print(f"🤖 Jarvis: {response}\n")
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    asyncio.run(main())