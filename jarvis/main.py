#!/usr/bin/env python3
"""
Jarvis Unified - Main Entry Point
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
import argparse

from core.jarvis import JarvisConfig, Jarvis

def parse_args():
    parser = argparse.ArgumentParser(description='🤖 Jarvis')
    parser.add_argument('--web', '-w', action='store_true', help='Start web UI')
    parser.add_argument('--port', '-p', type=int, default=5000, help='Port')
    parser.add_argument('--host', default='0.0.0.0', help='Host')
    return parser.parse_args()

async def main():
    args = parse_args()
    
    print("🤖 Jarvis v3.3")
    print("=" * 40)
    
    config = JarvisConfig('.env')
    jarvis = Jarvis(config)
    
    print(f"Model: {config.get('gemini_model')}")
    print(f"Code Brain: Gemma 4 - {'ON' if config.get('use_gemma_for_code') else 'OFF'}")
    
    if args.web:
        from ui.web_ui import JarvisTronUI
        print(f"\n🌐 Starting on http://{args.host}:{args.port}")
        ui = JarvisTronUI(jarvis, config.config)
        ui.run(host=args.host, port=args.port)
    else:
        print("\n💬 Interactive mode. Type 'quit' to exit.\n")
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input or user_input.lower() in ['quit', 'exit']:
                    break
                response = await jarvis.process(user_input)
                print(f"Jarvis: {response}\n")
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    asyncio.run(main())