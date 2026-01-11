"""
Voice command mode
Handles voice input and wake word detection
"""

import time
from typing import Optional


class VoiceMode:
    """Voice command mode handler"""
    
    def __init__(self, jarvis_instance):
        """
        Initialize voice mode
        
        Args:
            jarvis_instance: Jarvis instance to process commands
        """
        self.jarvis = jarvis_instance
        self.running = False
    
    def listen_for_voice(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """Listen for voice input and return transcribed text"""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with microphone as source:
                print("🎤 Adjusting for ambient noise... Please wait.")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("✅ Ready! Listening...")
            
            # Listen for audio
            with microphone as source:
                try:
                    audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                    print("🎤 Processing voice input...")
                    
                    # Use Google Speech Recognition
                    text = recognizer.recognize_google(audio)
                    return text.lower()
                except sr.WaitTimeoutError:
                    print("⏱️  No voice input detected within timeout period.")
                    return None
                except sr.UnknownValueError:
                    print("❌ Could not understand audio. Please try again.")
                    return None
                except sr.RequestError as e:
                    print(f"❌ Error with speech recognition service: {e}")
                    print("💡 Make sure you have an internet connection for Google Speech Recognition.")
                    return None
                    
        except ImportError:
            print("❌ speech_recognition module not found.")
            print("💡 Please install it: pip3 install SpeechRecognition pyaudio")
            return None
        except Exception as e:
            print(f"❌ Error listening for voice: {e}")
            return None
    
    def listen_for_wake_word(self) -> Optional[str]:
        """Listen continuously for 'jarvis' wake word, then capture command"""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            print("🎤 Voice command mode activated!")
            print("💡 Say 'jarvis' followed by your command")
            print("💡 Example: 'jarvis list files in this directory'")
            print("=" * 60)
            
            # Adjust for ambient noise
            with microphone as source:
                print("🎤 Adjusting for ambient noise... Please wait.")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("✅ Ready! Listening for 'jarvis'...")
            
            while self.running:
                try:
                    with microphone as source:
                        # Listen for audio (no timeout, continuous listening)
                        print("\n🎤 Listening... (say 'jarvis' followed by your command)")
                        audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
                        
                        print("🎤 Processing voice input...")
                        
                        # Recognize speech
                        try:
                            text = recognizer.recognize_google(audio).lower()
                            print(f"📝 Heard: {text}")
                            
                            # Check if "jarvis" is in the text
                            if "jarvis" in text:
                                # Extract command after "jarvis"
                                parts = text.split("jarvis", 1)
                                if len(parts) > 1:
                                    command = parts[1].strip()
                                    if command:
                                        print(f"✅ Command detected: {command}")
                                        return command
                                    else:
                                        print("⚠️  Heard 'jarvis' but no command followed. Please try again.")
                                else:
                                    print("⚠️  Heard 'jarvis' but no command followed. Please try again.")
                            else:
                                print(f"⚠️  Did not hear 'jarvis'. Heard: '{text}'")
                                print("💡 Please say 'jarvis' followed by your command.")
                                
                        except sr.UnknownValueError:
                            print("❌ Could not understand audio. Please try again.")
                        except sr.RequestError as e:
                            print(f"❌ Error with speech recognition service: {e}")
                            print("💡 Make sure you have an internet connection.")
                            
                except KeyboardInterrupt:
                    print("\n👋 Exiting voice command mode...")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
                    time.sleep(1)
                    
        except ImportError:
            print("❌ speech_recognition module not found.")
            print("💡 Please install it: pip3 install SpeechRecognition pyaudio")
            return None
        except Exception as e:
            print(f"❌ Error in voice command mode: {e}")
            return None
    
    def run(self) -> None:
        """Run Jarvis in voice command mode with full agentic support"""
        self.jarvis.clear_screen()
        self.jarvis.print_header()
        print("🎤 VOICE COMMAND MODE - AGENTIC AI")
        print("=" * 60)
        print("💡 Say 'jarvis' followed by your command")
        print("💡 Example: 'jarvis list files in this directory'")
        print("💡 Example: 'jarvis check if my CPU usage is normal'")
        print("💡 Jarvis will automatically iterate through commands until complete")
        print("💡 Say 'quit' or press Ctrl+C to exit")
        print("=" * 60)
        print()
        
        self.running = True
        
        while self.running:
            try:
                # Listen for wake word and command
                command = self.listen_for_wake_word()
                
                if not command:
                    continue
                
                if command.lower() in ['quit', 'q', 'exit', 'stop']:
                    print("👋 Goodbye!")
                    break
                
                # Process the command with full agentic support
                print(f"\n🤖 Processing voice command: {command}")
                print("🔄 Agentic mode: Jarvis will iterate through commands as needed...")
                print("=" * 60)
                self.jarvis.process_query(command)
                print("\n" + "=" * 60)
                print("✅ Agentic flow complete. Listening for next command...")
                print("=" * 60)
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print()
        
        self.running = False
        print()
    
    def stop(self) -> None:
        """Stop voice mode"""
        self.running = False

