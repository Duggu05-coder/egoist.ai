import os
import logging
from gtts import gTTS
import io

class AudioGenerator:
    def __init__(self):
        """Initialize audio generator"""
        self.temp_dir = "temp_audio"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
    
    def create_song_audio(self, song_name, emotion_type):
        """Create audio file for recommended song"""
        try:
            # Create a simple audio message about the song
            text = f"Here's a recommended song for {emotion_type}: {song_name}. This music can help soothe your emotions and provide comfort."
            
            # Generate audio
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to bytes
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            
            return audio_bytes.getvalue()
            
        except Exception as e:
            logging.error(f"Error creating song audio: {e}")
            return None
    
    def create_remedy_audio(self, remedy_text):
        """Create audio guidance for a remedy"""
        try:
            # Create guided audio for the remedy
            guidance_text = f"Here's a helpful remedy: {remedy_text}. Take your time and be gentle with yourself."
            
            # Generate audio
            tts = gTTS(text=guidance_text, lang='en', slow=True)
            
            # Save to bytes
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            
            return audio_bytes.getvalue()
            
        except Exception as e:
            logging.error(f"Error creating remedy audio: {e}")
            return None
    
    def cleanup_temp_files(self):
        """Clean up temporary audio files"""
        try:
            for file in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            logging.error(f"Error cleaning up temp files: {e}")