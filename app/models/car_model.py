from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Cars(Base):
    __tablename__ = "cars"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    car_id = Column(String(255), nullable=False, index=True)
    brand = Column(String(255), nullable=True, index=True) 
    name = Column(String(255), nullable=True, index=True)
    price = Column(Integer, nullable=True)
    location = Column(String(255), nullable=True, index=True)
    status = Column(String(255), nullable=True, index=True)
    year = Column(String(255), nullable=True, index=True)
    description = Column(Text, nullable=True)
    mileage = Column(Integer, nullable=True)
    origin = Column(String(255), nullable=True)
    body_type = Column(String(255), nullable=True)
    transmission = Column(String(255), nullable=True)
    engine = Column(String(255), nullable=True)
    exterior_color = Column(String(255), nullable=True)
    interior_color = Column(String(255), nullable=True)
    capacity = Column(String(255), nullable=True)
    number_of_doors = Column(String(255), nullable=True)
    drive_train = Column(String(255), nullable=True)
    seller_name = Column(String(255), nullable=True)
    address_seller = Column(String(255), nullable=True)
    phones = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Car(id={self.id}, car_id='{self.car_id}', name='{self.name}', price='{self.price}', location='{self.location}', status='{self.status}', year='{self.year}')>"
