from sqlalchemy.orm import Session
from app.models.car_model import Cars
from app.schemas.car_schema import CarsCreate
from typing import List

class CarsCRUD:
    def create_car(self, db: Session, car: CarsCreate) -> Cars:
        """Tạo xe mới"""
        db_car = Cars(
            car_id=car.car_id,
            brand=car.brand,
            name=car.name,
            price=car.price,
            location=car.location,
            status=car.status,
            year=car.year,
            description=car.description,
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

    def get_car_by_car_id(self, db: Session, car_id: str) -> Cars:
        return db.query(Cars).filter(Cars.car_id == car_id).first()
    
    # get all cars order by id asc
    def get_all_cars_order_by_id_asc(self, db: Session) -> List[Cars]:
        return db.query(Cars).order_by(Cars.id.asc()).all()

    # update price for car
    def update_price_for_car(self, db: Session, car_id: str, price: str) -> Cars:
        car = db.query(Cars).filter(Cars.car_id == car_id).first()
        car.price = price
        db.commit()
        db.refresh(car)
        return car

cars_crud = CarsCRUD()