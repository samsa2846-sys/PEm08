"""
Build script for MotionCraft Competition Analyzer
Creates standalone executable using PyInstaller
"""
import PyInstaller.__main__
import sys
import os
from pathlib import Path

def build_executable():
    """Build executable with PyInstaller"""
    
    # Get project root
    project_root = Path(__file__).parent.absolute()
    
    # PyInstaller arguments
    args = [
        'desktop_app.py',  # Main script
        '--name=CompetitionMonitor',  # Executable name
        '--onefile',  # Single executable file
        '--windowed',  # No console window
        '--icon=NONE',  # Add icon path if you have one
        
        # Add data files
        f'--add-data=frontend{os.pathsep}frontend',
        f'--add-data=.env.example{os.pathsep}.',
        
        # Hidden imports
        '--hidden-import=PyQt6',
        '--hidden-import=httpx',
        '--hidden-import=pydantic',
        '--hidden-import=backend',
        '--hidden-import=backend.config',
        '--hidden-import=backend.services',
        '--hidden-import=backend.services.analyzer_service',
        '--hidden-import=backend.models',
        '--hidden-import=backend.models.schemas',
        
        # Clean build
        '--clean',
        
        # Output directory
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.',
    ]
    
    print("=" * 60)
    print("Building MotionCraft Competition Analyzer")
    print("=" * 60)
    print(f"Project root: {project_root}")
    print(f"Python version: {sys.version}")
    print("=" * 60)
    
    # Run PyInstaller
    try:
        PyInstaller.__main__.run(args)
        print("\n" + "=" * 60)
        print("✅ Build completed successfully!")
        print("=" * 60)
        print(f"Executable location: {project_root / 'dist' / 'CompetitionMonitor.exe'}")
        print("\nTo run:")
        print("  1. Copy .env file to the same directory as CompetitionMonitor.exe")
        print("  2. Run CompetitionMonitor.exe")
        print("=" * 60)
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ Build failed!")
        print("=" * 60)
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_executable()

