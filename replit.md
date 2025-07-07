# AI Therapy Assistant

## Overview

This is a multi-modal AI therapy assistant built with Streamlit that provides therapeutic conversations through text, voice, and image interactions. The application uses Google's Gemini AI models to deliver compassionate, professional therapeutic responses while maintaining appropriate boundaries for an AI assistant.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Frontend**: Streamlit web application providing an intuitive chat interface
- **AI Engine**: Google Gemini AI models for text generation and image analysis
- **Audio Processing**: Speech recognition and text-to-speech capabilities
- **Image Analysis**: Vision-based therapeutic image interpretation
- **Database Layer**: PostgreSQL database for persistent conversation storage
- **Session Management**: Streamlit session state with database persistence

## Key Components

### Core Modules

1. **app.py** - Main Streamlit application entry point
   - Handles UI rendering and user interactions
   - Manages session state and conversation flow
   - Integrates all handler modules

2. **therapy_bot.py** - Core AI therapeutic assistant
   - Uses Gemini 2.5 Flash model for conversational responses
   - Implements professional therapeutic guidelines and safety measures
   - Maintains conversation context and history

3. **audio_handler.py** - Speech processing capabilities
   - Speech-to-text using Google Speech Recognition
   - Text-to-speech using Google Text-to-Speech (gTTS)
   - Handles audio file management and cleanup

4. **image_handler.py** - Vision-based analysis
   - Uses Gemini 2.5 Pro model for enhanced image understanding
   - Provides therapeutic context for image analysis
   - Generates empathetic insights about visual content

5. **database.py** - Database management and persistence
   - PostgreSQL integration with SQLAlchemy ORM
   - User session management and conversation history storage
   - Emotional context analysis tracking and user statistics

### Technology Stack

- **Framework**: Streamlit for web application
- **AI Models**: Google Gemini (Flash for text, Pro for vision)
- **Speech Processing**: SpeechRecognition library + Google Speech API
- **Text-to-Speech**: Google Text-to-Speech (gTTS)
- **Image Processing**: PIL (Python Imaging Library)
- **Audio Handling**: Built-in Python audio libraries

## Data Flow

1. **User Input**: Text, audio, or image input through Streamlit interface
2. **Processing**: Appropriate handler processes the input type
3. **AI Analysis**: Gemini models generate therapeutic responses
4. **Response Generation**: Text responses with optional audio output
5. **Session Update**: Conversation history maintained in session state
6. **UI Update**: Streamlit displays responses and updates interface

## External Dependencies

### Required APIs
- **Google Gemini API**: Primary AI engine for text and vision processing
- **Google Speech Recognition API**: Speech-to-text conversion
- **Google Text-to-Speech API**: Audio response generation

### Environment Variables
- `GEMINI_API_KEY`: Required for Google Gemini AI services

### Python Libraries
- `streamlit`: Web application framework
- `google-genai`: Google Generative AI client
- `speech_recognition`: Speech processing
- `gtts`: Google Text-to-Speech
- `pillow`: Image processing
- `psycopg2-binary`: PostgreSQL database adapter
- `sqlalchemy`: SQL toolkit and ORM
- `logging`: Error handling and debugging

## Deployment Strategy

The application is designed for deployment on platforms supporting Python web applications:

- **Replit**: Direct deployment with environment variable configuration
- **Streamlit Cloud**: Native Streamlit deployment platform
- **Docker**: Containerized deployment for cloud platforms
- **Local Development**: Direct Python execution with requirements.txt

### Configuration Requirements
1. Set up Google Cloud API credentials
2. Configure GEMINI_API_KEY environment variable
3. Install required Python dependencies
4. Ensure microphone access for audio features (if deployed locally)

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

- **July 7, 2025**: Enhanced emotional support features and content filtering
  - Added soothing songs recommendations based on detected emotions (anxiety, sadness, stress, anger)
  - Implemented funny jokes system to help lift users' moods
  - Created motivational quotes matched to emotional states
  - Added strict mathematical content filtering to ensure therapy-only responses
  - Enhanced conversation display with expandable sections for coping strategies, songs, and jokes
  - Fixed Streamlit widget errors for smoother user experience

- **July 1, 2025**: Added PostgreSQL database integration
  - Implemented user session management and persistent conversation storage
  - Added conversation history tracking with emotional context analysis
  - Created database schema for users, conversations, and feedback
  - Enhanced conversation flow with database persistence and user statistics

## Changelog

Changelog:
- June 30, 2025. Initial setup
- July 1, 2025. Added database functionality