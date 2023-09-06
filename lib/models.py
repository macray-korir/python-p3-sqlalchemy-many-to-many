from sqlalchemy import create_engine, ForeignKey, Table, Column, Integer, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    games = relationship('Game', secondary='game_users', back_populates='users')

    def __repr__(self):
        return f'User(id={self.id}, name={self.name})'

# Association table for Game and User many-to-many relationship
game_user = Table(
    'game_users',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
)

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    platform = Column(String)
    price = Column(Integer)

    reviews = relationship('Review', back_populates='game')
    users = relationship('User', secondary=game_user, back_populates='games')

    def __repr__(self):
        return f'Game(id={self.id}, title={self.title}, platform={self.platform})'

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    comment = Column(String)
    
    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship('Game', back_populates='reviews')

    def __repr__(self):
        return f'Review(id={self.id}, score={self.score}, comment={self.comment})'

SQLITE_URL = 'sqlite:///:memory:'

engine = create_engine(SQLITE_URL)  

Base.metadata.create_all(engine)