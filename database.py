import os
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    total_conversations = Column(Integer, default=0)
    
class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    session_id = Column(String(255), nullable=False)
    user_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    input_type = Column(String(50), nullable=False)  # text, audio, image
    has_audio_response = Column(Boolean, default=False)
    emotional_context = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    response_time = Column(Float, nullable=True)  # Time taken to generate response

class UserFeedback(Base):
    __tablename__ = "user_feedback"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    rating = Column(Integer, nullable=True)  # 1-5 rating
    feedback_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseManager:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
        
    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logging.info("Database tables created successfully")
        except Exception as e:
            logging.error(f"Error creating database tables: {e}")
            raise
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def get_or_create_user(self, session_id):
        """Get existing user or create new one"""
        db = self.get_session()
        try:
            user = db.query(User).filter(User.session_id == session_id).first()
            if not user:
                user = User(session_id=session_id)
                db.add(user)
                db.commit()
                db.refresh(user)
                logging.info(f"Created new user with session_id: {session_id}")
            else:
                # Update last active time
                user.last_active = datetime.utcnow()
                db.commit()
            return user
        except Exception as e:
            db.rollback()
            logging.error(f"Error getting/creating user: {e}")
            raise
        finally:
            db.close()
    
    def save_conversation(self, user_id, session_id, user_input, ai_response, input_type, has_audio_response=False, emotional_context=None, response_time=None):
        """Save conversation to database"""
        db = self.get_session()
        try:
            conversation = Conversation(
                user_id=user_id,
                session_id=session_id,
                user_input=user_input,
                ai_response=ai_response,
                input_type=input_type,
                has_audio_response=has_audio_response,
                emotional_context=emotional_context,
                response_time=response_time
            )
            db.add(conversation)
            
            # Update user's total conversation count
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.total_conversations += 1
                user.last_active = datetime.utcnow()
            
            db.commit()
            db.refresh(conversation)
            logging.info(f"Saved conversation for user {user_id}")
            return conversation
        except Exception as e:
            db.rollback()
            logging.error(f"Error saving conversation: {e}")
            raise
        finally:
            db.close()
    
    def get_user_conversations(self, session_id, limit=50):
        """Get user's conversation history"""
        db = self.get_session()
        try:
            conversations = db.query(Conversation).filter(
                Conversation.session_id == session_id
            ).order_by(Conversation.created_at.desc()).limit(limit).all()
            
            # Convert to list of dictionaries for easier use
            conversation_list = []
            for conv in conversations:
                conversation_list.append({
                    'id': str(conv.id),
                    'user': conv.user_input,
                    'assistant': conv.ai_response,
                    'input_type': conv.input_type,
                    'has_audio_response': conv.has_audio_response,
                    'created_at': conv.created_at,
                    'emotional_context': conv.emotional_context
                })
            
            return list(reversed(conversation_list))  # Return in chronological order
        except Exception as e:
            logging.error(f"Error getting user conversations: {e}")
            return []
        finally:
            db.close()
    
    def save_user_feedback(self, conversation_id, user_id, rating=None, feedback_text=None):
        """Save user feedback for a conversation"""
        db = self.get_session()
        try:
            feedback = UserFeedback(
                conversation_id=conversation_id,
                user_id=user_id,
                rating=rating,
                feedback_text=feedback_text
            )
            db.add(feedback)
            db.commit()
            logging.info(f"Saved feedback for conversation {conversation_id}")
            return feedback
        except Exception as e:
            db.rollback()
            logging.error(f"Error saving feedback: {e}")
            raise
        finally:
            db.close()
    
    def get_user_stats(self, session_id):
        """Get user statistics"""
        db = self.get_session()
        try:
            user = db.query(User).filter(User.session_id == session_id).first()
            if user:
                total_conversations = db.query(Conversation).filter(
                    Conversation.session_id == session_id
                ).count()
                
                return {
                    'total_conversations': total_conversations,
                    'user_since': user.created_at,
                    'last_active': user.last_active
                }
            return None
        except Exception as e:
            logging.error(f"Error getting user stats: {e}")
            return None
        finally:
            db.close()
    
    def clear_user_conversations(self, session_id):
        """Clear all conversations for a user"""
        db = self.get_session()
        try:
            db.query(Conversation).filter(
                Conversation.session_id == session_id
            ).delete()
            
            # Reset user's conversation count
            user = db.query(User).filter(User.session_id == session_id).first()
            if user:
                user.total_conversations = 0
            
            db.commit()
            logging.info(f"Cleared conversations for session {session_id}")
        except Exception as e:
            db.rollback()
            logging.error(f"Error clearing conversations: {e}")
            raise
        finally:
            db.close()

# Initialize database manager
db_manager = DatabaseManager()

def init_database():
    """Initialize database tables"""
    try:
        db_manager.create_tables()
        logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")
        raise