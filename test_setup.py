"""
Test script to verify all modules are working correctly
Run this after installation to check if everything is set up properly
"""

import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("="*60)
    print("TESTING MODULE IMPORTS")
    print("="*60)
    
    modules = {
        "cv2": "OpenCV",
        "mediapipe": "MediaPipe",
        "numpy": "NumPy",
        "pyautogui": "PyAutoGUI",
        "speech_recognition": "SpeechRecognition",
        "pyaudio": "PyAudio"
    }
    
    failed = []
    
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"✓ {name:20s} - OK")
        except ImportError as e:
            print(f"✗ {name:20s} - FAILED: {e}")
            failed.append(name)
    
    print()
    
    if failed:
        print(f"⚠ {len(failed)} module(s) failed to import:")
        for name in failed:
            print(f"  - {name}")
        return False
    else:
        print("✓ All modules imported successfully!")
        return True


def test_custom_modules():
    """Test if custom modules are working"""
    print("\n" + "="*60)
    print("TESTING CUSTOM MODULES")
    print("="*60)
    
    tests = []
    
    # Test config
    try:
        from config import config_manager, OperationMode
        print(f"✓ config.py           - OK")
        tests.append(True)
    except Exception as e:
        print(f"✗ config.py           - FAILED: {e}")
        tests.append(False)
    
    # Test gesture detector
    try:
        from gesture_detector import GestureDetector
        print(f"✓ gesture_detector.py - OK")
        tests.append(True)
    except Exception as e:
        print(f"✗ gesture_detector.py - FAILED: {e}")
        tests.append(False)
    
    # Test voice recognizer
    try:
        from voice_recognizer import VoiceRecognizer
        print(f"✓ voice_recognizer.py - OK")
        tests.append(True)
    except Exception as e:
        print(f"✗ voice_recognizer.py - FAILED: {e}")
        tests.append(False)
    
    # Test controller
    try:
        from controller import PresentationController
        print(f"✓ controller.py       - OK")
        tests.append(True)
    except Exception as e:
        print(f"✗ controller.py       - FAILED: {e}")
        tests.append(False)
    
    print()
    
    if all(tests):
        print("✓ All custom modules working!")
        return True
    else:
        print(f"⚠ {tests.count(False)} module(s) failed")
        return False


def test_camera():
    """Test camera access"""
    print("\n" + "="*60)
    print("TESTING CAMERA")
    print("="*60)
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                print(f"✓ Camera working!")
                print(f"  Resolution: {w}x{h}")
                print(f"  FPS: {cap.get(cv2.CAP_PROP_FPS):.1f}")
                cap.release()
                return True
            else:
                print("✗ Camera opened but cannot read frame")
                cap.release()
                return False
        else:
            print("✗ Cannot open camera")
            print("  Check if camera is being used by another application")
            return False
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False


def test_microphone():
    """Test microphone access"""
    print("\n" + "="*60)
    print("TESTING MICROPHONE")
    print("="*60)
    
    try:
        import speech_recognition as sr
        
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("  Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            print(f"✓ Microphone working!")
            print(f"  Energy threshold: {r.energy_threshold}")
            return True
    except Exception as e:
        print(f"✗ Microphone test failed: {e}")
        print("  Check if microphone is connected and permissions are granted")
        return False


def test_keyboard():
    """Test keyboard control"""
    print("\n" + "="*60)
    print("TESTING KEYBOARD CONTROL")
    print("="*60)
    
    try:
        import pyautogui
        
        screen_size = pyautogui.size()
        print(f"✓ PyAutoGUI working!")
        print(f"  Screen size: {screen_size.width}x{screen_size.height}")
        print(f"  Failsafe: {pyautogui.FAILSAFE}")
        return True
    except Exception as e:
        print(f"✗ Keyboard control test failed: {e}")
        return False


def test_vosk():
    """Test Vosk offline model (optional)"""
    print("\n" + "="*60)
    print("TESTING VOSK (OPTIONAL)")
    print("="*60)
    
    try:
        import os
        from vosk import Model
        
        model_path = "./models/vosk-model-small-id-0.22"
        
        if os.path.exists(model_path):
            model = Model(model_path)
            print(f"✓ Vosk model found and loaded!")
            print(f"  Path: {model_path}")
            return True
        else:
            print("⚠ Vosk model not found (optional)")
            print(f"  Expected path: {model_path}")
            print("  Download from: https://alphacephei.com/vosk/models")
            return None  # Not a failure, just optional
    except ImportError:
        print("⚠ Vosk not installed (optional)")
        print("  Install with: pip install vosk")
        return None
    except Exception as e:
        print(f"⚠ Vosk test warning: {e}")
        return None


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("PRESENTATION CONTROL TOOL - SYSTEM CHECK")
    print("="*60)
    print()
    
    results = {}
    
    # Run tests
    results['imports'] = test_imports()
    results['custom_modules'] = test_custom_modules()
    results['camera'] = test_camera()
    results['microphone'] = test_microphone()
    results['keyboard'] = test_keyboard()
    results['vosk'] = test_vosk()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    optional = sum(1 for v in results.values() if v is None)
    
    print(f"Passed:   {passed}")
    print(f"Failed:   {failed}")
    print(f"Optional: {optional}")
    print()
    
    if failed == 0:
        print("✓ All critical tests passed!")
        print("  You're ready to use the Presentation Control Tool!")
        print()
        print("Next steps:")
        print("  1. Run calibration: python main.py --calibrate")
        print("  2. Start application: python main.py")
        return 0
    else:
        print("✗ Some tests failed")
        print("  Please check the errors above and fix them before running the application")
        print()
        print("Common fixes:")
        print("  - Camera: Close other apps using camera")
        print("  - Microphone: Check Windows privacy settings")
        print("  - PyAudio: Reinstall using pipwin or pre-built wheels")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
