from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    planet_id = Column(Integer, ForeignKey('planet.id'))
    # Relationship to Planet
    home_planet = relationship("Planet", back_populates="residents")
    # Relationship to Ship
    ships = relationship("Ship", secondary="person_ship")

class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    climate = Column(String(250))
    population = Column(String(250))
    # Relationship to Person
    residents = relationship("Person", back_populates="home_planet")

class Ship(Base):
    __tablename__ = 'ship'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    model = Column(String(250), nullable=False)
    manufacturer = Column(String(250))
    # Many-to-many relationship with Person
    pilots = relationship("Person", secondary="person_ship")

# Association Table for the many-to-many relationship between Person and Ship
class PersonShip(Base):
    __tablename__ = 'person_ship'
    person_id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    ship_id = Column(Integer, ForeignKey('ship.id'), primary_key=True)

# Generate the diagram
engine = create_engine('sqlite:///starwars.db')
Base.metadata.create_all(engine)

try:
    render_er(Base, 'starwars_diagram.png')
    print("Success! Check the starwars_diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
