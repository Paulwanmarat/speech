import speech_recognition as sr
import pyttsx3
import time
import numpy as np

class HighAccuracyVoiceVerifier:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.5
        self.microphone = sr.Microphone()
        
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 200)
        
        self.valid_names = ["sophie", "julia", "emma", "sara", "laura",
                          "hayley", "susan", "fleur", "gabrielle", "robin",
                          "john", "liam", "lucas", "william", "kevin",
                          "jesse", "noah", "harrie", "peter", "robin"]
        
        self.sample_rate = 48000
        self.chunk_size = 2048
        
        self.confirmed_name = None
        self.current_processing_name = None
        self.audio_buffer = None

    def calibrate_microphone(self):
        """Precise microphone calibration"""
        with self.microphone as source:
            print("Calibrating microphone...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            self.recognizer.energy_threshold = min(
                self.recognizer.energy_threshold + 500, 
                4000
            )

    def speak(self, text):
        """Clear speech output"""
        print(f"ASSISTANT: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def active_listen(self, timeout=1.5):
        """High-accuracy listening with real-time processing"""
        with self.microphone as source:
            print("\n[Listening actively...]")
            start_time = time.time()
            audio_data = []
            
            while time.time() - start_time < timeout:
                try:
                    chunk = source.stream.read(self.chunk_size)
                    audio_data.append(chunk)
                    audio_frame = np.frombuffer(chunk, dtype=np.int16)
                    current_volume = np.abs(audio_frame).mean()
                    if current_volume > 1000:
                        print("* Voice detected *")
                        start_time = time.time()
                        
                except Exception as e:
                    print(f"Audio processing error: {e}")
                    continue
            
            if audio_data:
                audio_buffer = b''.join(audio_data)
                try:
                    audio = sr.AudioData(audio_buffer, 
                                       sample_rate=self.sample_rate,
                                       sample_width=2)
                    text = self.recognizer.recognize_google(audio)
                    print(f"USER: {text.lower()}")
                    return text.lower()
                except sr.UnknownValueError:
                    print("Speech not understood")
                except sr.RequestError:
                    print("API unavailable")
        
        return None

    def verify_identity(self):
        """Precise verification process"""
        self.speak("Hello can I ask you some questions?")
        time.sleep(0.5)
        
        remaining_names = self.valid_names.copy()
        
        while len(remaining_names) > 0:
            if len(remaining_names) == 1:
                name = remaining_names[0]
                print(f"\n=== AUTOMATICALLY VERIFIED ===\n{name.upper()}\n=============================")
                self.confirmed_name = name
                self.current_processing_name = name 
                self.speak(f"Hi {name}.")
                
                print(f"Currently processing name: {self.current_processing_name}")
                start_time = time.time()
                while time.time() - start_time < 12:
                    time.sleep(0.1)
                
                self.speak("Thank you for cooperation!")
                self.current_processing_name = None 
                return True
                
            name = remaining_names[0]
            self.speak(f"Are you {name}?")
            
            response = self.active_listen()
            
            if response and "yes" in response:
                print(f"\n=== VERIFIED ===\n{name.upper()}\n================")
                self.confirmed_name = name
                self.current_processing_name = name 
                self.speak(f"Hi {name}.")
                
                
                print(f"Currently processing name: {self.current_processing_name}")
                start_time = time.time()
                while time.time() - start_time < 12:

                    time.sleep(0.1)
                
                self.speak("Thank you for cooperation!")
                self.current_processing_name = None 
                return True
            elif response and "no" in response:
                print(f"Not {name}, removing from possibilities...")
                remaining_names.remove(name)
                continue
                
        self.speak("No matches found")
        return False

    def run(self):
        """Run verification system"""
        print("\n=== Testing ===")
        self.calibrate_microphone()
        
        if self.verify_identity():
            print(f"\nFinal stored name: {self.confirmed_name}")
        else:
            print("\nVerification incomplete")

if __name__ == "__main__":
    verifier = HighAccuracyVoiceVerifier()
    verifier.run()