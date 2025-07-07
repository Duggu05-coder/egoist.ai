# Installation Guide - AI Therapy Assistant

## Quick Start (Recommended)

### 1. Download and Extract
```bash
# Download the project files
git clone https://github.com/yourusername/ai-therapy-assistant.git
cd ai-therapy-assistant
```

### 2. Install Python Dependencies
```bash
# Install required packages
pip install -r setup_requirements.txt
```

### 3. Set Up API Key
1. Get your Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)
2. Copy `.env.example` to `.env`
3. Add your API key to the `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### 4. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Detailed Installation

### System Requirements
- Python 3.8 or higher
- 4GB RAM minimum
- Internet connection for AI services
- Microphone (optional, for voice features)

### Step-by-Step Setup

#### 1. Python Environment
```bash
# Check Python version
python --version

# Create virtual environment (recommended)
python -m venv therapy_env
source therapy_env/bin/activate  # On Windows: therapy_env\Scripts\activate
```

#### 2. Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r setup_requirements.txt
```

#### 3. Database Setup (Optional)
If you want persistent conversation storage:

```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb therapy_db

# Add database URL to .env file
DATABASE_URL=postgresql://postgres:password@localhost:5432/therapy_db
```

#### 4. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
nano .env
```

#### 5. Test Installation
```bash
# Run basic test
python -c "from therapy_bot import TherapyBot; print('Installation successful!')"

# Start the app
streamlit run app.py
```

## Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# If you get module import errors
pip install --upgrade streamlit google-genai gtts pillow
```

#### 2. Audio Issues
```bash
# On Ubuntu/Debian for audio support
sudo apt-get install portaudio19-dev python3-pyaudio

# Reinstall PyAudio
pip uninstall pyaudio
pip install pyaudio
```

#### 3. Database Connection
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Reset database connection
export DATABASE_URL=""  # Run without database
```

#### 4. API Key Issues
- Verify your Gemini API key is valid
- Check for extra spaces in the .env file
- Ensure the key has proper permissions

### Platform-Specific Instructions

#### Windows
```cmd
# Install Python from python.org
# Use Command Prompt or PowerShell

pip install -r setup_requirements.txt
streamlit run app.py
```

#### macOS
```bash
# Install using Homebrew
brew install python postgresql

# Then follow standard installation
pip install -r setup_requirements.txt
```

#### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-pip postgresql libpq-dev

# Follow standard installation
pip3 install -r setup_requirements.txt
```

## Docker Installation (Alternative)

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r setup_requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t ai-therapy-assistant .
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key ai-therapy-assistant
```

## Verification

After installation, verify these features work:
1. ✅ Text conversations
2. ✅ Voice recording (if microphone available)
3. ✅ Image upload and analysis
4. ✅ Emotional remedies and songs
5. ✅ Audio playback for remedies

## Getting Help

- Check the [README.md](README.md) for feature documentation
- Review error logs in the terminal
- Ensure all environment variables are set correctly
- Test with a simple conversation first

## Security Notes

- Keep your API keys private
- Don't commit `.env` files to version control
- Use environment variables in production
- Regularly update dependencies for security patches