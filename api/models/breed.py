from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from api.models.base import Base

class CatBreed(Base):
    __tablename__ = "cat_breeds"

    id = Column(String, primary_key=True)  # ex: "abys"
    name = Column(String, nullable=False)
    origin = Column(String)
    temperament = Column(Text)
    description = Column(Text)

    images = relationship("CatImage", back_populates="breed")
