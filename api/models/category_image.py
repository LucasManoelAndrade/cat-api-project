from sqlalchemy import Column, Integer, String
from api.models.base import Base

class CategoryImage(Base):
    __tablename__ = "category_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    category = Column(String, nullable=False)  # Ex: "hat", "sunglasses"
