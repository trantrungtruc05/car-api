import numpy as np

from app.crud.cars_repo import cars_crud
from app.core.database import get_db

db = next(get_db())

# call get_car_by_branch_and_name_like method and add price in object to array
cars = cars_crud.get_car_by_branch_and_name_like_and_year_and_location_and_status_order_by_price_asc(db=db, brand="Toyota", name="Toyota Veloz Cross 1.5 CVT", year="2025", location="TP HCM", status="Xe mới")
ls_car = []
for car in cars:
    ls_car.append(car.price)


data = np.array(ls_car)

Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)

print(f"Q1: {Q1}")
print(f"Q3: {Q3}")

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = data[(data < lower) | (data > upper)]


print("List car:", ls_car)
print("Outliers:", outliers)


