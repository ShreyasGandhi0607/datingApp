from sqlalchemy import (
    Integer, String, Column, create_engine, Date, Sequence, ForeignKey ,JSON, DateTime
    )
from sqlalchemy.orm import  sessionmaker, declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from user import User,Base
import hashlib

# Initialization
engine = create_engine('sqlite:///database/profile.db')
Session = sessionmaker(bind=engine)
session = Session()

# Defining Profile DB
class Profile(Base):
    __tablename__ = "profiles"

    profile_id = Column(Integer,Sequence('profile_id_seq',start=1000),primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    gender = Column(String,nullable=False)
    date_of_birth = Column(Date,nullable=False)
    bio = Column(String,nullable=True)
    profile_pic_url = Column(String,nullable=True)
    location = Column(String,nullable=False)
    interests = Column(JSON,nullable=True)
    preferred_gender = Column(String,nullable=False)
    age_pref_min = Column(Integer,nullable=False)
    age_pref_max = Column(Integer,nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

# creating table
Base.metadata.create_all(engine)

email  = input('Enter user u want to add profile to ')
existing_user = session.query(User).filter_by(email=email).first()

if existing_user:
    # Existing user: Add profile
    new_profile = Profile(
        user_id=existing_user.user_id,
        first_name="Test",
        last_name="User",
        gender="Male",
        date_of_birth=datetime(2001, 8, 6).date(),
        location="Pune",
        preferred_gender="Female",
        age_pref_min=18,
        age_pref_max=26
    )

    session.add(new_profile)
    session.commit()

    print(f"Profile added successfully for user: {existing_user.username}")
else:
    # New user: Check if email exists already
    username = input('Enter username: ')
    email = input('Enter email: ')
    
    # Check if the email already exists in the database
    existing_user_by_email = session.query(User).filter_by(email=email).first()

    if existing_user_by_email:
        print("Error: This email is already registered.")
    else:
        password = input('Enter password: ')

        # Hash the password before storing
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        new_user = User(username=username, email=email, password_hash=password_hash)
        session.add(new_user)
        session.commit()

        new_profile = Profile(
            user_id=new_user.user_id,
            first_name="Test",
            last_name="User",
            gender="Male",
            date_of_birth=datetime(2001, 8, 6).date(),
            location="Pune",
            preferred_gender="Female",
            age_pref_min=18,
            age_pref_max=26
        )

        session.add(new_profile)
        session.commit()

        print(f"New user and profile added successfully for {new_user.username}.")
