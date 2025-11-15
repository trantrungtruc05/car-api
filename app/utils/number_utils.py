import re
from app.crud.cars_repo import cars_crud
from app.core.database import get_db


db = next(get_db())


def convert_price_to_number(price: str) -> int:
    text = price.lower()
    total = 0
    parts = re.findall(r"([\d\.]+)\s*(tỷ|triệu|nghìn|ngàn)?", text)
    for number, unit in parts:
        number = float(number)
        if unit == "tỷ":
            total += number * 1_000_000_000
        elif unit == "triệu":
            total += number * 1_000_000
        elif unit == "nghìn" or unit == "ngàn":
            total += number * 1_000
        else:
            total += number  # không có đơn vị thì để nguyên

    return total

def update_price_into_db() -> int:
    # get all cars
    cars = cars_crud.get_all_cars(db=db)
    for car in cars:
        # print id processing
        print(f"Update pricing from string to number for car id: {car.id}")
        new_price = convert_price_to_number(car.price)
        cars_crud.update_price_for_car(db=db, car_id=car.car_id, price=new_price)


if __name__ == "__main__":
    update_price_into_db()
    print("done")
