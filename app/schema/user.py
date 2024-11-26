from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from datetime import datetime


# Initialize
engine = create_engine('sqlite:///database/user.db')  # Correct absolute path format
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
new_user = User(username='user5',email='user5@gmail.com',password_hash='yui4iuio8io9oi')
session.add(new_user)
session.commit()

def last_login(user_id):
    # get user using id
    user = session.query(User).filter_by(user_id=user_id).first()

    if user:
        # update last_login 
        user.last_login = datetime.now()
        session.commit()
        print(f"last login commited for {user.username}")
    else:
        print("user not found")



last_login(1)

session.close()