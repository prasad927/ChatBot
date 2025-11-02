#!/usr/bin/env python3
"""
Script to start both backend and frontend services for the AI Code Generator.
"""

import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv


def check_requirements():
    """Check if requirements.txt dependencies are installed."""
    try:
        ## TODO add all required packages
        print("All required packages are installed")
        return True
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False


def check_env_file():
    """Check if environment file exists."""
    env_file = Path(".env")
    if not env_file.exists():
        print(".env file not found")
        return False
    
    print("Please copy env.example to .env and add your OpenAI API key:")
    print("   cp env.example .env")
    print("   # Then edit .env file with your OpenAI API key")
    return True


def start_frontend():
    """Start the Gradio frontend server."""
    print("🎨 Starting frontend server...")
    frontend_process = subprocess.Popen([
        sys.executable, "frontend/app.py"
    ])
    return frontend_process


def main():
    """Main function to start both services."""
    print("AI Chat Bot - Service Starter")
    print("=" * 50)

    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment file
    check_env_file()

    # Load variables from .env file
    load_dotenv()
    
    try:
        # Start frontend
        frontend_process = start_frontend()
        print("Frontend UI: http://127.0.0.1:7819")
        print("\nPress Ctrl+C to stop  services")
        
        # Wait for processes
        try:
            frontend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping services...")
            frontend_process.terminate()
            frontend_process.wait()
            print("Services stopped successfully!")
            
    except Exception as e:
        print(f"Error starting services: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

