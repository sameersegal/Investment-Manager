# Models for Postgres Database using SQLAlchemy

from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship, backref

engine = create_engine('postgresql://localhost:5432/foodie')
Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    messages = relationship('Message', backref=backref('conversation', order_by=id))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self):
        return "<Conversation(id='%s', title='%s')>" % (self.id, self.title)
    
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    type = Column(Enum('user', 'bot','thought','error'))
    text = Column(String)
    feedback = Column(Enum('none', 'positive', 'negative'), default='none')
    created_at = Column(DateTime)

    def __repr__(self):
        return "<Message(id='%s', conversation_id='%s', type='%s', text='%s')>" % (self.id, self.conversation_id, self.type, self.text)
    

