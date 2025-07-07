import streamlit as st
import speech_recognition as sr
import io
import tempfile
import os
from gtts import gTTS
import base64
import logging

class AudioHandler:
    def __init__(self):
        """Initialize audio handler with speech recognition"""
        self.recognizer = sr.Recognizer()
        
        # Adjust for ambient noise
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
        except:
            # Handle case where microphone is not available
            pass

    def speech_to_text(self, audio_data):
        """Convert speech audio to text"""
        try:
            # Save audio data to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                temp_audio.write(audio_data.getvalue())
                temp_audio_path = temp_audio.name
            
            try:
                # Load audio file
                with sr.AudioFile(temp_audio_path) as source:
                    audio = self.recognizer.record(source)
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
                return text
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_audio_path):
                    os.unlink(temp_audio_path)
                    
        except sr.UnknownValueError:
            logging.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logging.error(f"Speech recognition request failed: {e}")
            return None
        except Exception as e:
            logging.error(f"Error in speech to text conversion: {e}")
            return None

    def text_to_speech(self, text, language='en', slow=False):
        """Convert text to speech audio"""
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            return audio_buffer.getvalue()
            
        except Exception as e:
            logging.error(f"Error in text to speech conversion: {e}")
            return None

    def process_audio_input(self, audio_bytes):
        """Process uploaded audio file"""
        try:
            # Convert bytes to text
            text = self.speech_to_text(audio_bytes)
            return text
        except Exception as e:
            logging.error(f"Error processing audio input: {e}")
            return None

    def create_audio_response(self, response_text):
        """Create audio response from text"""
        try:
            # Generate speech from text
            audio_data = self.text_to_speech(response_text)
            
            if audio_data:
                # Encode audio data for web playback
                audio_base64 = base64.b64encode(audio_data).decode()
                return audio_base64
            
            return None
            
        except Exception as e:
            logging.error(f"Error creating audio response: {e}")
            return None

    def validate_audio_input(self, audio_data):
        """Validate that audio input is processable"""
        try:
            if not audio_data:
                return False, "No audio data provided"
            
            # Check if audio data has content
            if len(audio_data.getvalue()) < 1000:  # Minimum size check
                return False, "Audio file too short"
            
            return True, "Audio is valid"
            
        except Exception as e:
            return False, f"Audio validation error: {str(e)}"

    def get_audio_duration(self, audio_data):
        """Get duration of audio file (approximate)"""
        try:
            # This is a rough estimation based on file size
            # For more accurate duration, you'd need additional libraries
            file_size = len(audio_data.getvalue())
            # Rough estimation: 16kHz, 16-bit mono = ~32KB per second
            estimated_duration = file_size / 32000
            return max(1, int(estimated_duration))  # At least 1 second
            
        except Exception as e:
            logging.error(f"Error estimating audio duration: {e}")
            return 0
