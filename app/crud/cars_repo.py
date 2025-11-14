from sqlalchemy.orm import Session
from app.models.car_model import Cars
from app.schemas.car_schema import CarsCreate

class CarsCRUD:
    def create_car(self, db: Session, car: CarsCreate) -> Cars:
        """Tạo xe mới"""
        db_car = Cars(
            car_id=car.car_id,
            name=car.name,
            price=car.price,
            location=car.location,
            status=car.status,
            year=car.year,
            mileage=car.mileage,
            origin=car.origin,
            body_type=car.body_type,
            transmission=car.transmission,
            engine=car.engine,
            exterior_color=car.exterior_color,
            interior_color=car.interior_color,
            capacity=car.capacity,
            number_of_doors=car.number_of_doors,
            drive_train=car.drive_train,
            seller_name=car.seller_name,
            address_seller=car.address_seller,
            phones=car.phones,
        )
        db.add(db_car)
        db.commit()
        db.refresh(db_car)

cars_crud = CarsCRUD()