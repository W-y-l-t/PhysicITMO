import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Функция для проверки корректного ввода числа
def get_float_input(prompt, condition=lambda x: True, error_message="Некорректный ввод, попробуйте снова."):
    while True:
        try:
            value = float(input(prompt))
            if condition(value):
                return value
            else:
                print(error_message)
        except ValueError:
            print(error_message)


# Проверка начальных позиций на пересечение и выход за границы
def validate_positions(pos1, pos2, s1, s2, W, H):
    # Проверка на выход за границы
    def check_within_bounds(pos, s, W, H):
        return (s / 2 <= pos[0] <= W - s / 2) and (s / 2 <= pos[1] <= H - s / 2)

    # Проверка на пересечение: расстояние между центрами должно быть не меньше суммы половин сторон квадратов
    def check_no_overlap(pos1, pos2, s1, s2):
        distance = np.linalg.norm(pos1 - pos2)  # Расстояние между центрами квадратов
        min_distance = (s1 / 2) + (s2 / 2)  # Сумма половин сторон квадратов
        return distance >= min_distance  # Возвращает True, если квадраты не пересекаются

    # Проверяем границы
    if not check_within_bounds(pos1, s1, W, H):
        print(f"Позиция первого квадрата выходит за границы оболочки! {pos1}")
        return False
    if not check_within_bounds(pos2, s2, W, H):
        print(f"Позиция второго квадрата выходит за границы оболочки! {pos2}")
        return False

    # Проверяем пересечение
    if not check_no_overlap(pos1, pos2, s1, s2):
        print("Квадраты пересекаются!")
        return False

    return True


# Ввод пользовательских данных с проверками
print("Введите параметры симуляции:")
m1 = get_float_input("Масса первого тела (положительное число): ", condition=lambda x: x > 0)
m2 = get_float_input("Масса второго тела (положительное число): ", condition=lambda x: x > 0)
v1_x = get_float_input("Скорость по оси X первого тела: ")
v1_y = get_float_input("Скорость по оси Y первого тела: ")
v2_x = get_float_input("Скорость по оси X второго тела: ")
v2_y = get_float_input("Скорость по оси Y второго тела: ")
s1 = get_float_input("Размер стороны квадрата первого тела (положительное число): ", condition=lambda x: x > 0)
s2 = get_float_input("Размер стороны квадрата второго тела (положительное число): ", condition=lambda x: x > 0)
W = get_float_input("Ширина оболочки (положительное число): ", condition=lambda x: x > 0)
H = get_float_input("Высота оболочки (положительное число): ", condition=lambda x: x > 0)

# Ввод начальных положений с проверками
while True:
    pos1 = np.array([get_float_input(f"Начальная позиция по оси X для первого тела (0 < X < {W}): "),
                     get_float_input(f"Начальная позиция по оси Y для первого тела (0 < Y < {H}): ")])

    pos2 = np.array([get_float_input(f"Начальная позиция по оси X для второго тела (0 < X < {W}): "),
                     get_float_input(f"Начальная позиция по оси Y для второго тела (0 < Y < {H}): ")])

    if validate_positions(pos1, pos2, s1, s2, W, H):
        break
    else:
        print("Введите корректные начальные позиции тел.")

# Начальные скорости
v1 = np.array([v1_x, v1_y])  # начальная скорость тела 1
v2 = np.array([v2_x, v2_y])  # начальная скорость тела 2

# Время
dt = 0.01


# Функция для проверки столкновения с границами оболочки
def check_collision_with_walls(pos, vel, s):
    if pos[0] - s / 2 < 0 or pos[0] + s / 2 > W:
        vel[0] = -vel[0]  # изменение направления по оси x
    if pos[1] - s / 2 < 0 or pos[1] + s / 2 > H:
        vel[1] = -vel[1]  # изменение направления по оси y
    return vel


# Функция для проверки столкновения между квадратами
def check_collision_between_squares(pos1, pos2, vel1, vel2, s1, s2):
    # Проверка пересечения границ квадратов
    if (abs(pos1[0] - pos2[0]) < (s1 + s2) / 2) and (abs(pos1[1] - pos2[1]) < (s1 + s2) / 2):
        # Расчет новых скоростей на основе закона сохранения импульса
        v1_new = vel1 * (m1 - m2) / (m1 + m2) + vel2 * (2 * m2) / (m1 + m2)
        v2_new = vel2 * (m2 - m1) / (m1 + m2) + vel1 * (2 * m1) / (m1 + m2)
        return v1_new, v2_new
    return vel1, vel2


# Инициализация графики
fig, ax = plt.subplots()
ax.set_xlim(0, W)
ax.set_ylim(0, H)
rect1 = plt.Rectangle(pos1 - np.array([s1 / 2, s1 / 2]), s1, s1, color='blue')
rect2 = plt.Rectangle(pos2 - np.array([s2 / 2, s2 / 2]), s2, s2, color='red')
ax.add_patch(rect1)
ax.add_patch(rect2)


def update(frame):
    global pos1, pos2, v1, v2

    # Проверка столкновения с оболочкой
    v1 = check_collision_with_walls(pos1, v1, s1)
    v2 = check_collision_with_walls(pos2, v2, s2)

    # Проверка столкновения между квадратами
    v1, v2 = check_collision_between_squares(pos1, pos2, v1, v2, s1, s2)

    # Обновление позиций тел
    pos1 += v1 * dt
    pos2 += v2 * dt

    # Обновление графики
    rect1.set_xy(pos1 - np.array([s1 / 2, s1 / 2]))
    rect2.set_xy(pos2 - np.array([s2 / 2, s2 / 2]))
    return rect1, rect2


ani = FuncAnimation(fig, update, frames=200, interval=10, blit=True)
plt.show()
