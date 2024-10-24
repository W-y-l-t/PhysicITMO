import numpy as np
import matplotlib.pyplot as plt


# Функция для ввода и проверки значений
def get_positive_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Значение должно быть положительным.")
            else:
                return value
        except ValueError:
            print("Пожалуйста, введите числовое значение.")


def get_non_negative_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Значение не может быть отрицательным.")
            else:
                return value
        except ValueError:
            print("Пожалуйста, введите числовое значение.")


# Ввод данных от пользователя с проверкой
m = get_positive_input("Введите массу груза (кг, положительное число): ")
k = get_positive_input("Введите коэффициент жесткости пружины (Н/м, положительное число): ")
b = get_non_negative_input("Введите коэффициент сопротивления среды (Н·с/м, неотрицательное число): ")
x0 = get_non_negative_input("Введите начальную координату (м, неотрицательное число): ")
v0 = get_non_negative_input("Введите начальную скорость (м/с, неотрицательное число): ")

# Определение параметров численного решения
t_start = 0
t_end = get_positive_input("Введите время колебаний (с, положительное число): ")
dt = 0.01
num_steps = int((t_end - t_start) / dt)

# Инициализация массивов для времени, координаты и скорости
t = np.linspace(t_start, t_end, num_steps)
x = np.zeros(num_steps)
v = np.zeros(num_steps)

# Начальные условия
x[0] = x0
v[0] = v0

# Численное решение методом Эйлера
for i in range(1, num_steps):
    dxdt = v[i - 1]
    dvdt = -(k / m) * x[i - 1] - (b / m) * v[i - 1]

    x[i] = x[i - 1] + dxdt * dt
    v[i] = v[i - 1] + dvdt * dt

# Вычисление энергий
kinetic_energy = 0.5 * m * v ** 2
potential_energy = 0.5 * k * x ** 2
total_energy = kinetic_energy + potential_energy

# Построение графиков
plt.figure(figsize=(10, 6))
plt.plot(t, kinetic_energy, label='Кинетическая энергия', color='b')
plt.plot(t, potential_energy, label='Потенциальная энергия', color='g')
plt.plot(t, total_energy, label='Полная механическая энергия', color='r', linestyle='--')
plt.title('Энергии в зависимости от времени')
plt.xlabel('Время (с)')
plt.ylabel('Энергия (Дж)')
plt.legend()
plt.grid(True)
plt.show()
