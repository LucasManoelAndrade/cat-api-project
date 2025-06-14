from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.models.base import Base

class CatImage(Base):
    __tablename__ = "cat_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    breed_id = Column(String, ForeignKey("cat_breeds.id"))

    breed = relationship("CatBreed", back_populates="images")
