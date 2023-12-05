from sqlalchemy import Column, Integer, String, Float

from db import Base

class Music(Base):
    __tablename__ = "music"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    blues = Column(Float, nullable=False)
    classical = Column(Float, nullable=False)
    country = Column(Float, nullable=False)
    disco = Column(Float, nullable=False)
    hiphop = Column(Float, nullable=False)
    jazz = Column(Float, nullable=False)
    metal = Column(Float, nullable=False)
    pop = Column(Float, nullable=False)
    reggae = Column(Float, nullable=False)
    rock = Column(Float, nullable=False)

    def get_vectors(self):
        return [
            self.blues,
            self.classical,
            self.country,
            self.disco,
            self.hiphop,
            self.jazz,
            self.metal,
            self.pop,
            self.reggae,
            self.rock
        ]