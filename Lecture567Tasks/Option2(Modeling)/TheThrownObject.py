import numpy as np
import matplotlib.pyplot as plt

# Функции для ввода и проверки значений
def get_positive_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Значение должно быть неотрицательным.")
            else:
                return value
        except ValueError:
            print("Пожалуйста, введите числовое значение.")

def get_angle_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0 or value > 90:
                print("Угол должен быть между 0 и 90 градусами.")
            else:
                return value
        except ValueError:
            print("Пожалуйста, введите числовое значение.")

# Ввод данных от пользователя
v0 = get_positive_input("Введите начальную скорость (м/с, неотрицательное число): ")
theta = np.radians(get_angle_input("Введите угол броска (градусы, от 0 до 90): "))
h0 = get_positive_input("Введите начальную высоту (м, неотрицательное число): ")
k = get_positive_input("Введите коэффициент сопротивления воздуха (неотрицательное число): ")

# Константы
g = 9.81
t_start = 0  # Начальное время
dt = 0.01    # Шаг времени

# Начальные условия
x0 = 0
vx0 = v0 * np.cos(theta)
vy0 = v0 * np.sin(theta)

# Функция для решения системы уравнений
def equations(t, y):
    x, y_pos, vx, vy = y
    dxdt = vx
    dydt = vy
    dvxdt = -k * vx
    dvydt = -g - k * vy
    return [dxdt, dydt, dvxdt, dvydt]

# Численное решение методом Рунге-Кутты
def runge_kutta_4th(equations, y0, t):
    n = len(t)
    y = np.zeros((n, len(y0)))
    y[0] = y0
    for i in range(1, n):
        dt = t[i] - t[i-1]
        k1 = np.array(equations(t[i-1], y[i-1]))
        k2 = np.array(equations(t[i-1] + dt/2, y[i-1] + dt/2 * k1))
        k3 = np.array(equations(t[i-1] + dt/2, y[i-1] + dt/2 * k2))
        k4 = np.array(equations(t[i-1] + dt, y[i-1] + dt * k3))
        y[i] = y[i-1] + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

        # Остановить расчет, если тело касается земли
        if y[i][1] < 0:
            return y[:i+1]  # Вернуть только до момента касания земли
    return y

# Временной интервал
t_eval = np.arange(t_start, 40, dt)  # 40 секунд - достаточно для большинства бросков

# Решение задачи
initial_conditions = [x0, h0, vx0, vy0]
sol = runge_kutta_4th(equations, initial_conditions, t_eval)

# Извлечение данных
x = sol[:, 0]
y = sol[:, 1]
vx = sol[:, 2]
vy = sol[:, 3]

# Построение графиков на одном листе
fig, axs = plt.subplots(3, 1, figsize=(10, 15))

# 1. Траектория движения тела
axs[0].plot(x, y, label='Траектория движения', color='b')
axs[0].set_title('Траектория движения тела')
axs[0].set_xlabel('Координата x (м)')
axs[0].set_ylabel('Координата y (м)')
axs[0].grid(True)
axs[0].legend()

# 2. Зависимость скорости от времени
axs[1].plot(np.arange(len(vx)) * dt, vx, label='Скорость по оси x', color='r')
axs[1].plot(np.arange(len(vy)) * dt, vy, label='Скорость по оси y', color='g')
axs[1].set_title('Скорость от времени')
axs[1].set_xlabel('Время (с)')
axs[1].set_ylabel('Скорость (м/с)')
axs[1].grid(True)
axs[1].legend()

# 3. Зависимость координат от времени
axs[2].plot(np.arange(len(x)) * dt, x, label='Координата x', color='r')
axs[2].plot(np.arange(len(y)) * dt, y, label='Координата y', color='g')
axs[2].set_title('Координаты от времени')
axs[2].set_xlabel('Время (с)')
axs[2].set_ylabel('Координаты (м)')
axs[2].grid(True)
axs[2].legend()

plt.tight_layout()
plt.show()
