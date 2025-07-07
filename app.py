import streamlit as st
import os
import time
import uuid
from therapy_bot import TherapyBot
from audio_handler import AudioHandler
from image_handler import ImageHandler
from database import db_manager, init_database
from audio_generator import AudioGenerator
import base64
from io import BytesIO
import logging

# Set page config
st.set_page_config(
    page_title="AI Therapy Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def initialize_database():
    """Initialize database connection and tables"""
    try:
        init_database()
        return True
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        return False

# Initialize session state
if 'therapy_bot' not in st.session_state:
    st.session_state.therapy_bot = TherapyBot()
if 'audio_handler' not in st.session_state:
    st.session_state.audio_handler = AudioHandler()
if 'image_handler' not in st.session_state:
    st.session_state.image_handler = ImageHandler()
if 'user_session_id' not in st.session_state:
    st.session_state.user_session_id = str(uuid.uuid4())
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_audio_response' not in st.session_state:
    st.session_state.current_audio_response = None
if 'db_initialized' not in st.session_state:
    st.session_state.db_initialized = initialize_database()
if 'current_user' not in st.session_state:
    if st.session_state.db_initialized:
        try:
            st.session_state.current_user = db_manager.get_or_create_user(st.session_state.user_session_id)
            # Load conversation history from database
            st.session_state.conversation_history = db_manager.get_user_conversations(st.session_state.user_session_id)
        except Exception as e:
            logging.error(f"Error loading user data: {e}")
            st.session_state.current_user = None

def main():
    st.title("🧠 AI Therapy Assistant")
    st.markdown("*A supportive space for therapeutic conversations with multi-modal interaction*")
    
    # Sidebar for settings and history
    with st.sidebar:
        st.header("Session Options")
        
        # User stats
        if st.session_state.db_initialized and st.session_state.current_user:
            user_stats = db_manager.get_user_stats(st.session_state.user_session_id)
            if user_stats:
                st.info(f"💬 Total conversations: {user_stats['total_conversations']}")
        
        # Clear conversation button
        if st.button("Clear Conversation", type="secondary"):
            if st.session_state.db_initialized:
                try:
                    db_manager.clear_user_conversations(st.session_state.user_session_id)
                    st.success("Conversation history cleared from database")
                except Exception as e:
                    st.error(f"Error clearing database: {e}")
            st.session_state.conversation_history = []
            st.session_state.current_audio_response = None
            st.rerun()
        
        # Audio settings
        st.subheader("Audio Settings")
        enable_audio_output = st.checkbox("Enable Audio Responses", value=True)
        
        # Export conversation history
        if st.session_state.conversation_history:
            st.subheader("Export Options")
            if st.button("📥 Download Chat History", type="secondary"):
                # Create text export of conversation history
                export_text = f"AI Therapy Assistant - Conversation History\n"
                export_text += f"Session ID: {st.session_state.user_session_id}\n"
                export_text += f"Export Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                export_text += "=" * 50 + "\n\n"
                
                for i, entry in enumerate(st.session_state.conversation_history, 1):
                    export_text += f"Conversation {i}\n"
                    export_text += f"Time: {entry.get('created_at', 'Unknown')}\n"
                    export_text += f"Input Type: {entry['input_type'].title()}\n"
                    export_text += f"You: {entry['user']}\n"
                    export_text += f"Assistant: {entry['assistant']}\n"
                    if entry.get('emotional_context'):
                        export_text += f"Emotional Context: {entry['emotional_context']}\n"
                    export_text += "-" * 30 + "\n\n"
                
                st.download_button(
                    label="💾 Save as Text File",
                    data=export_text,
                    file_name=f"therapy_chat_history_{time.strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        # Database status
        st.subheader("Database Status")
        if st.session_state.db_initialized:
            st.success("✅ Database connected")
        else:
            st.error("❌ Database not available")
        
        # Conversation history
        st.subheader("Recent Conversations")
        if st.session_state.conversation_history:
            for i, entry in enumerate(st.session_state.conversation_history[-5:]):  # Show last 5
                with st.expander(f"Exchange {len(st.session_state.conversation_history) - 4 + i}"):
                    st.write(f"**You:** {entry['user'][:100]}...")
                    st.write(f"**Assistant:** {entry['assistant'][:100]}...")
                    if 'created_at' in entry:
                        st.caption(f"Time: {entry['created_at']}")
        else:
            st.write("No conversation history yet.")
    
    # Main chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat Interface")
        
        # Display conversation history
        if st.session_state.conversation_history:
            st.markdown("---")
            st.subheader("💬 Conversation History")
            
            for i, entry in enumerate(st.session_state.conversation_history):
                # Create container for each conversation
                with st.container():
                    # User message with timestamp
                    st.markdown(f"**🙋 You** ({entry.get('created_at', 'Unknown time')}):")
                    st.markdown(f"*{entry['input_type'].title()} input*")
                    st.write(entry['user'])
                    
                    # Assistant response
                    st.markdown(f"**🤖 Assistant:**")
                    st.write(entry['assistant'])
                    
                    # Show emotional context if available
                    if entry.get('emotional_context'):
                        st.caption(f"💭 Emotional context: {entry['emotional_context']}")
                    
                    # Show coping strategies
                    if entry.get('coping_strategies'):
                        with st.expander("🧘 Coping Strategies"):
                            st.write(entry['coping_strategies'])
                    
                    # Show soothing content (songs, remedies, and jokes)
                    if entry.get('soothing_content'):
                        content = entry['soothing_content']
                        
                        # Create three columns for better layout
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if content.get('songs'):
                                with st.expander("🎵 Soothing Songs"):
                                    for song in content['songs'][:3]:  # Show top 3 songs
                                        st.write(f"• {song}")
                                        # Add audio button for each song
                                        if st.button(f"🔊 Play {song.split(' by')[0]}", key=f"play_{entry.get('id', 'unknown')}_{song[:20]}"):
                                            try:
                                                from audio_generator import AudioGenerator
                                                audio_gen = AudioGenerator()
                                                audio_data = audio_gen.create_song_audio(song, entry.get('emotional_context', 'general'))
                                                if audio_data:
                                                    st.audio(audio_data, format='audio/mp3')
                                            except Exception as e:
                                                st.warning("Audio generation temporarily unavailable")
                        
                        with col2:
                            if content.get('remedies'):
                                with st.expander("💊 Instant Remedies"):
                                    for remedy in content['remedies'][:3]:  # Show top 3 remedies
                                        st.write(f"• {remedy}")
                                        # Add audio guidance for remedy
                                        if st.button(f"🎧 Guide me", key=f"remedy_{entry.get('id', 'unknown')}_{remedy[:20]}"):
                                            try:
                                                from audio_generator import AudioGenerator
                                                audio_gen = AudioGenerator()
                                                audio_data = audio_gen.create_remedy_audio(remedy)
                                                if audio_data:
                                                    st.audio(audio_data, format='audio/mp3')
                                            except Exception as e:
                                                st.warning("Audio guidance temporarily unavailable")
                        
                        with col3:
                            if content.get('jokes'):
                                with st.expander("😄 Uplifting Jokes"):
                                    for joke in content['jokes'][:2]:  # Show 2 jokes
                                        st.write(f"• {joke}")
                    
                    # Show motivational quote
                    if entry.get('motivational_quote'):
                        st.info(f"✨ {entry['motivational_quote']}")
                    
                    # Audio playback if available
                    if entry.get('audio_data') and enable_audio_output:
                        st.audio(entry['audio_data'], format='audio/mp3')
                    
                    # Show if this had audio response
                    if entry.get('has_audio_response'):
                        st.caption("🔊 Audio response generated")
                
                st.divider()
        else:
            st.info("💬 Start a conversation by typing a message below!")
        
        # Text input
        user_input = st.text_area(
            "Share your thoughts or feelings:",
            placeholder="Type your message here...",
            height=100,
            key="text_input"
        )
        
        # Submit text button
        if st.button("Send Message", type="primary", disabled=not user_input.strip()):
            if user_input.strip():
                process_user_input(user_input, "text", enable_audio_output)
    
    with col2:
        st.subheader("🎤 Audio Input")
        
        # Audio recording section
        st.write("Record your voice:")
        audio_bytes = st.audio_input("Record audio")
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            if st.button("Process Audio", type="secondary"):
                with st.spinner("Processing audio..."):
                    try:
                        # Convert audio to text
                        audio_text = st.session_state.audio_handler.speech_to_text(audio_bytes)
                        if audio_text:
                            st.success(f"Transcribed: {audio_text}")
                            process_user_input(audio_text, "audio", enable_audio_output)
                        else:
                            st.error("Could not transcribe audio. Please try again.")
                    except Exception as e:
                        st.error(f"Audio processing error: {str(e)}")
        
        st.divider()
        
        st.subheader("🖼️ Image Input")
        
        # Image upload section
        uploaded_image = st.file_uploader(
            "Upload an image to discuss:",
            type=['png', 'jpg', 'jpeg'],
            help="Share an image that relates to your feelings or situation"
        )
        
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            
            # Image description input
            image_context = st.text_input(
                "Describe what you'd like to discuss about this image:",
                placeholder="What does this image mean to you?"
            )
            
            if st.button("Analyze Image", type="secondary", disabled=not image_context.strip()):
                if image_context.strip():
                    with st.spinner("Analyzing image..."):
                        try:
                            # Process image with context
                            image_analysis = st.session_state.image_handler.analyze_image_with_context(
                                uploaded_image, image_context
                            )
                            if image_analysis:
                                combined_input = f"[Image Context: {image_context}]\n[Image Analysis: {image_analysis}]"
                                process_user_input(combined_input, "image", enable_audio_output)
                            else:
                                st.error("Could not analyze image. Please try again.")
                        except Exception as e:
                            st.error(f"Image processing error: {str(e)}")

def process_user_input(user_input, input_type, enable_audio_output):
    """Process user input and generate response"""
    try:
        start_time = time.time()
        
        with st.spinner("Generating response..."):
            # Get AI response
            response = st.session_state.therapy_bot.get_response(
                user_input, 
                st.session_state.conversation_history
            )
            
            response_time = time.time() - start_time
            
            # Generate audio if enabled
            audio_data = None
            has_audio_response = False
            if enable_audio_output:
                try:
                    audio_data = st.session_state.audio_handler.text_to_speech(response)
                    has_audio_response = audio_data is not None
                except Exception as e:
                    st.warning(f"Audio generation failed: {str(e)}")
            
            # Analyze emotional context and generate supportive content
            emotional_context = None
            coping_strategies = None
            soothing_content = None
            motivational_quote = None
            try:
                emotional_context = st.session_state.therapy_bot.analyze_emotional_context(user_input)
                if emotional_context:
                    # Extract key emotional state for personalized content
                    emotional_state = emotional_context.split('\n')[0] if emotional_context else user_input
                    coping_strategies = st.session_state.therapy_bot.generate_coping_strategies(emotional_state)
                    soothing_content = st.session_state.therapy_bot.get_soothing_content(emotional_state)
                    motivational_quote = st.session_state.therapy_bot.get_motivational_quote(emotional_state)
            except Exception as e:
                logging.warning(f"Emotional analysis failed: {e}")
            
            # Save to database if available
            conversation_id = None
            if st.session_state.db_initialized and st.session_state.current_user:
                try:
                    conversation_record = db_manager.save_conversation(
                        user_id=st.session_state.current_user.id,
                        session_id=st.session_state.user_session_id,
                        user_input=user_input,
                        ai_response=response,
                        input_type=input_type,
                        has_audio_response=has_audio_response,
                        emotional_context=emotional_context,
                        response_time=response_time
                    )
                    conversation_id = conversation_record.id
                except Exception as e:
                    logging.error(f"Failed to save conversation to database: {e}")
                    st.warning("Conversation not saved to database")
            
            # Add to session conversation history
            conversation_entry = {
                'id': str(conversation_id) if conversation_id else None,
                'user': user_input,
                'assistant': response,
                'input_type': input_type,
                'audio_data': audio_data,
                'has_audio_response': has_audio_response,
                'emotional_context': emotional_context,
                'coping_strategies': coping_strategies,
                'soothing_content': soothing_content,
                'motivational_quote': motivational_quote,
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            st.session_state.conversation_history.append(conversation_entry)
            
            # Refresh the page to show new conversation
            st.rerun()
            
    except Exception as e:
        st.error(f"Error processing input: {str(e)}")
        logging.error(f"Error in process_user_input: {e}")

if __name__ == "__main__":
    # Check for required API key
    if not os.getenv("GEMINI_API_KEY"):
        st.error("⚠️ GEMINI_API_KEY environment variable is required. Please set it to use this application.")
        st.stop()
    
    main()
