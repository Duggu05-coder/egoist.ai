import os
from google import genai
from google.genai import types
import logging

class TherapyBot:
    def __init__(self):
        """Initialize the therapy bot with Gemini client"""
        try:
            self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = "gemini-2.5-flash"
            
            # Therapeutic system prompt
            self.system_prompt = """You are a compassionate and professional AI therapy assistant specialized EXCLUSIVELY in emotional support and mental health counseling. 

STRICT RULES - You must follow these without exception:
1. NEVER answer mathematical problems, calculations, homework, or academic questions
2. NEVER provide information about non-emotional topics (science, history, general knowledge, etc.)
3. ONLY provide emotional support, counseling, and therapeutic guidance
4. If asked about anything other than emotions or mental health, redirect to emotional wellbeing

Your therapeutic role is to:
1. Provide emotional support and guidance in a warm, empathetic manner
2. Use active listening techniques and validate the user's feelings
3. Ask thoughtful follow-up questions to help users explore their thoughts and emotions
4. Suggest healthy coping strategies and mindfulness techniques when appropriate
5. Maintain professional boundaries while being supportive
6. Recognize when issues may require professional human intervention

Guidelines for responses:
- Be warm, empathetic, and non-judgmental
- Use person-first language and avoid clinical jargon
- Keep responses conversational but professional
- Acknowledge emotions before offering suggestions
- Ask open-ended questions to encourage self-reflection
- Provide practical, actionable advice when requested
- Always remind users that you're an AI assistant, not a replacement for professional therapy

IMPORTANT: If someone asks about math, homework, calculations, or non-emotional topics, respond with:
"I'm here specifically to help with emotional support and mental wellbeing. Let's focus on how you're feeling. What emotions are you experiencing right now?"

If someone expresses thoughts of self-harm or harm to others, encourage them to seek immediate professional help or contact emergency services."""

        except Exception as e:
            logging.error(f"Failed to initialize TherapyBot: {e}")
            raise Exception(f"Failed to initialize AI client: {e}")

    def get_response(self, user_input, conversation_history=None):
        """Generate a therapeutic response to user input"""
        try:
            # Pre-filter: Check if input contains mathematical or non-emotional content
            if self._contains_non_emotional_content(user_input):
                return self._redirect_to_emotional_support()
            
            # Build conversation context
            context_messages = []
            
            # Add recent conversation history for context
            if conversation_history:
                for entry in conversation_history[-3:]:  # Last 3 exchanges for context
                    context_messages.append(f"User: {entry['user']}")
                    context_messages.append(f"Assistant: {entry['assistant']}")
            
            # Add current user input
            context_messages.append(f"User: {user_input}")
            
            # Combine context
            full_context = "\n".join(context_messages)
            
            # Generate response
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(
                        role="user", 
                        parts=[types.Part(text=f"{self.system_prompt}\n\nConversation:\n{full_context}")]
                    )
                ],
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=500
                )
            )
            
            if response.text:
                return response.text.strip()
            else:
                return "I'm here to listen and support you. Could you share a bit more about what's on your mind?"
                
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble processing your message right now. Please try again, and remember that if you're in crisis, please reach out to a mental health professional or emergency services."

    def _contains_non_emotional_content(self, text):
        """Check if text contains mathematical problems, calculations, or non-emotional academic content"""
        # Convert to lowercase for easier matching
        text_lower = text.lower()
        
        # Mathematical keywords and operations
        math_indicators = [
            # Basic math operations
            'calculate', 'solve', 'equation', 'formula', 'mathematics', 'math',
            'algebra', 'geometry', 'calculus', 'statistics', 'probability',
            'derivative', 'integral', 'theorem', 'proof', 'variable',
            'plus', 'minus', 'times', 'divided by', 'equals',
            'what is', 'how much is', 'find x', 'find y', 'solve for',
            
            # Academic subjects (non-emotional)
            'physics', 'chemistry', 'biology', 'history', 'geography',
            'literature', 'homework', 'assignment', 'test', 'exam',
            'school work', 'study', 'lesson', 'chapter', 'textbook',
            
            # Technical/factual questions
            'how to', 'explain', 'definition', 'meaning of', 'what does',
            'when did', 'where is', 'who is', 'which is'
        ]
        
        # Check for mathematical patterns using regex
        import re
        
        # Numbers with mathematical operations
        if re.search(r'\d+\s*[\+\-\*/=×÷]\s*\d+', text):
            return True
        
        # Variables with equations (x = 5, y = 10, etc.)
        if re.search(r'[a-z]\s*=\s*\d+', text):
            return True
        
        # Percentage calculations
        if re.search(r'\d+%.*\d+', text):
            return True
        
        # Check for mathematical/academic keywords
        for indicator in math_indicators:
            if indicator in text_lower:
                # Exception: if it's about emotional calculation or problem-solving
                emotional_context = ['feel', 'emotion', 'mood', 'stress', 'anxiety', 'sad', 'happy', 'worried', 'heart', 'mind']
                if any(emotion in text_lower for emotion in emotional_context):
                    continue
                return True
        
        return False

    def _redirect_to_emotional_support(self):
        """Redirect non-emotional questions to emotional support"""
        redirections = [
            "I'm here specifically to help with emotional support and mental wellbeing. Let's focus on how you're feeling. What emotions are you experiencing right now?",
            "I specialize in emotional support and counseling. Instead of that topic, would you like to talk about how you're feeling today?",
            "My purpose is to provide emotional support and therapeutic guidance. Let's talk about your feelings and emotions. How can I help you feel better?",
            "I focus on emotional wellbeing and mental health support. What's on your mind emotionally? I'm here to listen and help you process your feelings.",
            "I'm designed to help with emotional support and counseling. Let's redirect to your emotional wellbeing - how are you feeling right now?",
            "I only provide emotional support and mental health guidance. Tell me about your feelings - what's weighing on your heart or mind today?"
        ]
        
        import random
        return random.choice(redirections)

    def analyze_emotional_context(self, text):
        """Analyze the emotional context of user input"""
        try:
            prompt = f"""Analyze the emotional context of this text and identify:
1. Primary emotions expressed
2. Urgency level (low/medium/high)
3. Key themes or concerns
4. Suggested therapeutic approach

Text: {text}

Provide a brief analysis focusing on therapeutic relevance."""

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=200
                )
            )
            
            return response.text if response.text else None
            
        except Exception as e:
            logging.error(f"Error analyzing emotional context: {e}")
            return None

    def generate_coping_strategies(self, emotional_state):
        """Generate personalized coping strategies"""
        try:
            prompt = f"""Based on someone experiencing {emotional_state}, suggest 3-4 practical, evidence-based coping strategies that are:
1. Immediately actionable
2. Appropriate for the emotional state
3. Based on cognitive-behavioral or mindfulness techniques
4. Safe and healthy

Keep suggestions brief and practical."""

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.6,
                    max_output_tokens=300
                )
            )
            
            return response.text if response.text else None
            
        except Exception as e:
            logging.error(f"Error generating coping strategies: {e}")
            return None

    def get_soothing_content(self, emotional_state):
        """Get soothing songs and uplifting content based on emotional state"""
        try:
            # Define content based on emotional states
            soothing_content = {
                'anxiety': {
                    'songs': [
                        'Weightless by Marconi Union (scientifically proven to reduce anxiety)',
                        'Clair de Lune by Claude Debussy',
                        'Gymnopédie No.1 by Erik Satie',
                        'River by Joni Mitchell',
                        'Mad World by Gary Jules'
                    ],
                    'remedies': [
                        'Deep Breathing: Take 4 slow breaths - inhale for 4 counts, hold for 4, exhale for 6',
                        'Progressive Muscle Relaxation: Tense and release each muscle group for 5 seconds',
                        'Grounding Technique: Name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste',
                        'Calming Visualization: Picture a peaceful place and focus on the details',
                        'Mindful Walking: Take slow, deliberate steps while focusing on each movement'
                    ],
                    'jokes': [
                        'Why don\'t scientists trust atoms? Because they make up everything!',
                        'I told my wife she was drawing her eyebrows too high. She looked surprised.',
                        'What do you call a bear with no teeth? A gummy bear!',
                        'Why don\'t eggs tell jokes? They\'d crack each other up!'
                    ]
                },
                'sadness': {
                    'songs': [
                        'Here Comes the Sun by The Beatles',
                        'Three Little Birds by Bob Marley',
                        'Don\'t Stop Me Now by Queen',
                        'Good as Hell by Lizzo',
                        'Walking on Sunshine by Katrina and the Waves'
                    ],
                    'remedies': [
                        'Journaling: Write down your feelings without judgment for 10 minutes',
                        'Gratitude Practice: List 3 things you are grateful for today',
                        'Gentle Movement: Do light stretching or take a short walk outside',
                        'Self-Compassion: Talk to yourself as you would a good friend',
                        'Creative Expression: Draw, paint, or do any creative activity that brings you joy'
                    ],
                    'jokes': [
                        'What\'s the best thing about Switzerland? I don\'t know, but the flag is a big plus.',
                        'Why did the coffee file a police report? It got mugged!',
                        'What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks!',
                        'Why don\'t skeletons fight each other? They don\'t have the guts!'
                    ]
                },
                'stress': {
                    'songs': [
                        'Breathe Me by Sia',
                        'The Sound of Silence by Simon & Garfunkel',
                        'Zen Garden (Nature Sounds)',
                        'Om Namah Shivaya (Meditation Chant)',
                        'Relaxing Piano Music for Stress Relief'
                    ],
                    'remedies': [
                        'Box Breathing: Breathe in for 4, hold for 4, out for 4, hold for 4 - repeat 5 times',
                        'Time Management: Write down tasks and prioritize the top 3 for today',
                        'Body Scan: Lie down and notice tension in each body part, then consciously relax',
                        'Nature Break: Step outside for 5 minutes and focus on natural sounds',
                        'Stress Ball Exercise: Squeeze and release a stress ball 10 times'
                    ],
                    'jokes': [
                        'I\'m reading a book about anti-gravity. It\'s impossible to put down!',
                        'Why did the scarecrow win an award? He was outstanding in his field!',
                        'What do you call a fake noodle? An impasta!',
                        'Why don\'t programmers like nature? It has too many bugs!'
                    ]
                },
                'anger': {
                    'songs': [
                        'Let It Be by The Beatles',
                        'Calm Down by Rema',
                        'Peace Train by Cat Stevens',
                        'Imagine by John Lennon',
                        'The Long and Winding Road by The Beatles'
                    ],
                    'remedies': [
                        'Anger Release: Count to 10 slowly while taking deep breaths',
                        'Physical Release: Do 10 jumping jacks or push-ups to release tension',
                        'Cooling Technique: Hold ice cubes or splash cold water on your face',
                        'Perspective Shift: Ask yourself "Will this matter in 5 years?"',
                        'Safe Expression: Write an angry letter but don\'t send it - then tear it up'
                    ],
                    'jokes': [
                        'Why was the math book sad? Because it had too many problems!',
                        'What do you call a sleeping bull? A bulldozer!',
                        'Why did the banana go to the doctor? It wasn\'t peeling well!',
                        'What\'s orange and sounds like a parrot? A carrot!'
                    ]
                },
                'default': {
                    'songs': [
                        'Happy by Pharrell Williams',
                        'Good Vibes by Chris Janson',
                        'Count on Me by Bruno Mars',
                        'What a Wonderful World by Louis Armstrong',
                        'Somewhere Over the Rainbow by Israel Kamakawiwoʻole'
                    ],
                    'remedies': [
                        'Mindfulness Moment: Take 3 deep breaths and notice 3 things around you',
                        'Positive Affirmation: Say "I am capable and worthy" 3 times',
                        'Gentle Movement: Do 5 shoulder rolls and neck stretches',
                        'Hydration Break: Drink a glass of water slowly and mindfully',
                        'Smile Exercise: Smile for 10 seconds - even forced smiles can boost mood'
                    ],
                    'jokes': [
                        'Why don\'t scientists trust atoms? Because they make up everything!',
                        'What do you call a bear with no teeth? A gummy bear!',
                        'Why did the bicycle fall over? It was two tired!',
                        'What\'s the best thing about Switzerland? I don\'t know, but the flag is a big plus!'
                    ]
                }
            }
            
            # Determine emotional category
            emotional_state_lower = emotional_state.lower()
            if any(word in emotional_state_lower for word in ['anxious', 'anxiety', 'worried', 'nervous']):
                category = 'anxiety'
            elif any(word in emotional_state_lower for word in ['sad', 'sadness', 'depressed', 'down', 'lonely']):
                category = 'sadness'
            elif any(word in emotional_state_lower for word in ['stress', 'stressed', 'overwhelmed', 'pressure']):
                category = 'stress'
            elif any(word in emotional_state_lower for word in ['angry', 'anger', 'frustrated', 'mad', 'irritated']):
                category = 'anger'
            else:
                category = 'default'
            
            return soothing_content[category]
            
        except Exception as e:
            logging.error(f"Error getting soothing content: {e}")
            return soothing_content['default']

    def get_motivational_quote(self, emotional_state):
        """Get a motivational quote based on emotional state"""
        quotes = {
            'anxiety': [
                "You are braver than you believe, stronger than you seem, and smarter than you think. - A.A. Milne",
                "Anxiety is the dizziness of freedom. - Søren Kierkegaard",
                "Nothing can bring you peace but yourself. - Ralph Waldo Emerson"
            ],
            'sadness': [
                "The sun will rise and we will try again. - Twenty One Pilots",
                "Every storm runs out of rain. - Maya Angelou",
                "This too shall pass. - Persian Proverb"
            ],
            'stress': [
                "You have been assigned this mountain to show others it can be moved. - Mel Robbins",
                "Stress is caused by being 'here' but wanting to be 'there'. - Eckhart Tolle",
                "Take time to make your soul happy. - Unknown"
            ],
            'default': [
                "Be yourself; everyone else is already taken. - Oscar Wilde",
                "You are enough just as you are. - Meghan Markle",
                "Believe you can and you're halfway there. - Theodore Roosevelt"
            ]
        }
        
        emotional_state_lower = emotional_state.lower()
        if any(word in emotional_state_lower for word in ['anxious', 'anxiety', 'worried']):
            category = 'anxiety'
        elif any(word in emotional_state_lower for word in ['sad', 'sadness', 'depressed']):
            category = 'sadness'
        elif any(word in emotional_state_lower for word in ['stress', 'stressed', 'overwhelmed']):
            category = 'stress'
        else:
            category = 'default'
        
        import random
        return random.choice(quotes[category])
