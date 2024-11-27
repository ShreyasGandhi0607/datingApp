from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from datetime import datetime
import hashlib

# Initialize
engine = create_engine('sqlite:///database/user.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# Defining user Model
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String,nullable=False,unique=True)
    email = Column(String,nullable=False,unique=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    last_login = Column(DateTime, nullable=True)

# create table
Base.metadata.create_all(engine)

# CRUD operations
# new_user = User(username='user5',email='user5@gmail.com',password_hash='yui4iuio8io9oi')
# session.add(new_user)
# session.commit()

def add_new_user(username,email,password):
    password_hash = password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    try:
        new_user = User(username=username, email=email, password_hash=password_hash)
        session.add(new_user)
        session.commit()
        print(f"User '{username}' added successfully!")
    except Exception as e:
        session.rollback()  # Rollback in case of any error
        print(f"Error occurred: {e}")






def last_login(user_id):
    try:
        user = session.query(User).filter_by(user_id=user_id).first()

        if user:
            # Update last_login 
            user.last_login = datetime.now()
            session.commit()
            print(f"Last login updated for {user.username}")
        else:
            print("User not found.")
    except Exception as e:
        print(f"Error occurred: {e}")



# last_login(1)

# session.close()