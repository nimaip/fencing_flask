#!/usr/bin/env python3
"""
Fencing Pose Analysis - Startup Script
Run this script to start the Flask application
"""

import sys
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = ['flask', 'cv2', 'mediapipe', 'numpy', 'PIL']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'PIL':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing dependencies:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def main():
    """Main function to start the application"""
    print("🏃 Starting Fencing Pose Analysis...")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Import and run the Flask app
    try:
        from app import app
        print("🌐 Starting Flask server...")
        print("📱 Open your browser and go to: http://localhost:5000")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Error importing app: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 