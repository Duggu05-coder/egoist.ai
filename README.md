# AI Therapy Assistant

A comprehensive multi-modal therapy chatbot built with Streamlit and Google Gemini AI that provides emotional support through text, voice, and image interactions.

## Features

### 🎯 Core Functionality
- **Text-based therapy conversations** with empathetic AI responses
- **Voice input/output** - Record your voice and get audio responses
- **Image analysis** - Upload images for therapeutic interpretation
- **Emotional context analysis** - AI detects and responds to your emotional state
- **Persistent conversation history** - All conversations saved to PostgreSQL database

### 🎵 Emotional Support System
- **Personalized song recommendations** based on your emotions
- **Instant remedies** - Breathing exercises, grounding techniques, mindfulness practices
- **Audio guidance** - Voice instructions for remedies and song introductions
- **Uplifting jokes** - Mood-boosting humor tailored to your emotional state
- **Motivational quotes** - Inspiring messages matched to your feelings

### 🛡️ Safety Features
- **Therapy-focused responses only** - Blocks mathematical/academic questions
- **Professional boundaries** - Clear AI assistant limitations
- **Crisis support guidance** - Encourages professional help when needed
- **Emotional content filtering** - Ensures all responses are therapeutic

## Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database (optional - can run without database)
- Google Gemini API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-therapy-assistant.git
   cd ai-therapy-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r setup_requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   DATABASE_URL=postgresql://username:password@localhost/therapy_db
   ```

4. **Get your Google Gemini API key**
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Create a new project
   - Generate an API key
   - Add it to your `.env` file

5. **Run the application**
   ```bash
   streamlit run app.py --server.port 8501
   ```

## Usage

### Basic Conversation
1. Open the app in your browser
2. Type your feelings or concerns in the chat
3. Get empathetic responses with personalized support

### Voice Features
1. Click "🎤 Record Voice" to speak your message
2. The AI will transcribe and respond to your voice
3. Enable "Audio Output" to hear responses read aloud

### Image Analysis
1. Upload an image using the file uploader
2. The AI will analyze the image for emotional context
3. Get therapeutic insights about visual content

### Emotional Support
- **Songs**: Get music recommendations based on your mood
- **Remedies**: Receive instant coping strategies (breathing, grounding, etc.)
- **Audio Guidance**: Click audio buttons for voice-guided remedies
- **Jokes**: Enjoy mood-lifting humor
- **Quotes**: Find inspiration with motivational quotes

## Project Structure

```
ai-therapy-assistant/
├── app.py                 # Main Streamlit application
├── therapy_bot.py         # Core AI therapy logic
├── audio_handler.py       # Voice processing
├── image_handler.py       # Image analysis
├── audio_generator.py     # Audio generation for songs/remedies
├── database.py           # Database management
├── setup_requirements.txt # Python dependencies
├── replit.md             # Project documentation
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

## Configuration

### Streamlit Configuration
The app is configured to run on `0.0.0.0:8501` for deployment compatibility.

### Database Configuration
- Uses PostgreSQL for persistent storage
- Stores conversation history, user sessions, and emotional context
- Can run without database (conversations stored in session only)

## API Dependencies

- **Google Gemini API**: Primary AI engine for text and vision processing
- **Google Speech Recognition**: Speech-to-text conversion
- **Google Text-to-Speech**: Audio response generation

## Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
- **Replit**: Direct deployment with environment variables
- **Streamlit Cloud**: Native Streamlit deployment
- **Docker**: Containerized deployment for cloud platforms
- **Heroku**: Web application deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation in `replit.md`
- Review the code comments for implementation details

## Disclaimer

This AI therapy assistant is designed for emotional support and should not replace professional mental health care. If you're experiencing a mental health crisis, please contact a qualified mental health professional or emergency services.

## Recent Updates

- **July 7, 2025**: Added remedies system with audio guidance
- **July 7, 2025**: Enhanced emotional support with songs and jokes
- **July 7, 2025**: Added strict mathematical content filtering
- **July 1, 2025**: Implemented PostgreSQL database integration
- **June 30, 2025**: Initial release with multi-modal support

---

Made with ❤️ for mental health support and emotional wellbeing.