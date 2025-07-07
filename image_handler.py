import os
from google import genai
from google.genai import types
from PIL import Image
import io
import base64
import logging

class ImageHandler:
    def __init__(self):
        """Initialize image handler with Gemini client for vision capabilities"""
        try:
            self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = "gemini-2.5-pro"  # Use pro model for better image analysis
        except Exception as e:
            logging.error(f"Failed to initialize ImageHandler: {e}")
            raise Exception(f"Failed to initialize image analysis client: {e}")

    def analyze_image_with_context(self, uploaded_file, user_context):
        """Analyze image with therapeutic context"""
        try:
            # Read image data
            image_data = uploaded_file.read()
            
            # Create therapeutic analysis prompt
            therapeutic_prompt = f"""As a therapeutic AI assistant, analyze this image in the context of the user's question: "{user_context}"

Please provide:
1. A compassionate description of what you observe in the image
2. How this image might relate to the user's emotional state or concerns
3. Therapeutic insights or gentle observations that might be helpful
4. Questions that could help the user explore their feelings about this image

Remember to be empathetic, non-judgmental, and supportive in your analysis. Focus on emotional and psychological aspects that might be relevant for therapeutic discussion."""

            # Analyze image with Gemini Vision
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Part.from_bytes(
                        data=image_data,
                        mime_type=f"image/{uploaded_file.type.split('/')[-1]}",
                    ),
                    therapeutic_prompt
                ],
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=400
                )
            )
            
            return response.text if response.text else "I can see your image, but I'm having trouble analyzing it right now. Could you tell me more about what this image means to you?"
            
        except Exception as e:
            logging.error(f"Error analyzing image: {e}")
            return f"I'm having difficulty analyzing the image right now. However, I'd love to hear about what this image represents to you and how it relates to your feelings or experiences."

    def analyze_image_emotions(self, uploaded_file):
        """Analyze potential emotions or mood conveyed by an image"""
        try:
            image_data = uploaded_file.read()
            
            emotion_prompt = """Analyze this image for emotional content and mood. Consider:
1. Colors and their psychological impact
2. Composition and visual elements that might reflect emotions
3. Symbolic elements that could relate to feelings or mental states
4. Overall mood or atmosphere of the image

Provide insights that could be relevant for therapeutic discussion, focusing on emotional and psychological aspects."""

            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Part.from_bytes(
                        data=image_data,
                        mime_type=f"image/{uploaded_file.type.split('/')[-1]}",
                    ),
                    emotion_prompt
                ],
                config=types.GenerateContentConfig(
                    temperature=0.6,
                    max_output_tokens=300
                )
            )
            
            return response.text if response.text else None
            
        except Exception as e:
            logging.error(f"Error analyzing image emotions: {e}")
            return None

    def validate_image(self, uploaded_file):
        """Validate uploaded image file"""
        try:
            if not uploaded_file:
                return False, "No image file provided"
            
            # Check file size (limit to 10MB)
            if uploaded_file.size > 10 * 1024 * 1024:
                return False, "Image file too large (max 10MB)"
            
            # Check file type
            allowed_types = ['image/png', 'image/jpeg', 'image/jpg']
            if uploaded_file.type not in allowed_types:
                return False, "Unsupported image format (use PNG or JPEG)"
            
            # Try to open with PIL to validate
            try:
                image = Image.open(uploaded_file)
                image.verify()
                uploaded_file.seek(0)  # Reset file pointer
                return True, "Image is valid"
            except Exception:
                return False, "Invalid or corrupted image file"
                
        except Exception as e:
            return False, f"Image validation error: {str(e)}"

    def get_image_info(self, uploaded_file):
        """Get basic information about the uploaded image"""
        try:
            image = Image.open(uploaded_file)
            info = {
                'format': image.format,
                'mode': image.mode,
                'size': image.size,
                'width': image.width,
                'height': image.height
            }
            uploaded_file.seek(0)  # Reset file pointer
            return info
        except Exception as e:
            logging.error(f"Error getting image info: {e}")
            return None

    def resize_image_if_needed(self, uploaded_file, max_size=(1024, 1024)):
        """Resize image if it's too large for processing"""
        try:
            image = Image.open(uploaded_file)
            
            # Check if resize is needed
            if image.width > max_size[0] or image.height > max_size[1]:
                # Resize while maintaining aspect ratio
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save resized image to bytes
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format=image.format or 'JPEG')
                img_byte_arr.seek(0)
                
                return img_byte_arr
            else:
                uploaded_file.seek(0)
                return uploaded_file
                
        except Exception as e:
            logging.error(f"Error resizing image: {e}")
            uploaded_file.seek(0)
            return uploaded_file

    def generate_therapeutic_questions(self, image_analysis):
        """Generate therapeutic questions based on image analysis"""
        try:
            prompt = f"""Based on this image analysis: "{image_analysis}"

Generate 3-4 thoughtful, open-ended questions that a therapist might ask to help someone explore their feelings and thoughts about this image. The questions should:
1. Encourage self-reflection
2. Be emotionally supportive
3. Help the person connect the image to their inner experience
4. Be appropriate for therapeutic dialogue

Format as a simple list."""

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=200
                )
            )
            
            return response.text if response.text else None
            
        except Exception as e:
            logging.error(f"Error generating therapeutic questions: {e}")
            return None
