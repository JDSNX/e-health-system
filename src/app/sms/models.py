import json
from sqlalchemy import String, Integer, Column, Text
from sqlalchemy.types import TypeDecorator
from app.database.core import Base

class TextPickleType(TypeDecorator):

    impl = Text(256)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    ref_id = Column(Integer, unique=True)
    full_name =  Column(String)
    emergency_contact_person = Column(String)
    emergency_contact_number = Column(String)
    results = Column(TextPickleType())
    timestamp = Column(Integer)
    password = Column(String)
    

