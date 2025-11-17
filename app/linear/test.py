import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Dữ liệu
X = np.array([[10], [20], [30], [40], [50]])
y = np.array([800, 750, 700, 630, 590])

model = LinearRegression()
model.fit(X, y)

print("Hệ số (slope):", model.coef_)
print("Intercept:", model.intercept_)
print("Dự đoán phút = 50 → tiền:", model.predict([[50]]))

plt.scatter(X, y, label="Data points") 
plt.scatter(X, y, label="Real data")       # điểm dữ liệu
plt.plot(X, model.predict(X), label="Regression line") # đường tuyến tính
plt.xlabel("X")
plt.ylabel("y")
plt.legend()
plt.show()
