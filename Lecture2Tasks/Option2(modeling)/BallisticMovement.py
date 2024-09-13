import numpy as np
import matplotlib.pyplot as plt
import keyboard

g = 9.81  # ускорение свободного падения, м/с^2

def calculate_trajectory(h0, v0, angle_deg):
    angle_rad = np.radians(angle_deg) # значение угла в радианах
    vx = v0 * np.cos(angle_rad)  # горизонтальная составляющая скорости
    vy = v0 * np.sin(angle_rad)  # вертикальная составляющая скорости

    t_flight = (vy + np.sqrt(vy ** 2 + 2 * g * h0)) / g  # полное время полета

    t = np.linspace(0, t_flight, num=1000) # значения времени, которые будут использованы для построения графиков

    x = vx * t  # горизонтальная координата
    y = h0 + vy * t - 0.5 * g * t ** 2  # вертикальная координата

    return t, x, y, vx, vy


def plot_results(t, x, y, vx, vy):
    plt.figure(figsize=(12, 8))

    # Траектория движения
    plt.subplot(2, 2, 1)
    plt.plot(x, y)
    plt.title("Траектория движения")
    plt.xlabel("Горизонтальная координата (м)")
    plt.ylabel("Вертикальная координата (м)")
    plt.grid(True)

    # Скорость от времени
    v_total = np.sqrt(vx ** 2 + (vy - g * t) ** 2)
    plt.subplot(2, 2, 2)
    plt.plot(t, v_total)
    plt.title("Скорость от времени")
    plt.xlabel("Время (с)")
    plt.ylabel("Скорость (м/с)")
    plt.grid(True)

    # Горизонтальная координата от времени
    plt.subplot(2, 2, 3)
    plt.plot(t, x)
    plt.title("Горизонтальная координата от времени")
    plt.xlabel("Время (с)")
    plt.ylabel("Горизонтальная координата (м)")
    plt.grid(True)

    # Вертикальная координата от времени
    plt.subplot(2, 2, 4)
    plt.plot(t, y)
    plt.title("Вертикальная координата от времени")
    plt.xlabel("Время (с)")
    plt.ylabel("Вертикальная координата (м)")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def main():
    # Входные данные
    h0 = float(input("Введите высоту (м): "))
    v0 = float(input("Введите начальную скорость (м/с): "))
    angle_deg = float(input("Введите угол броска (градусы): "))

    # Рассчитать траекторию
    t, x, y, vx, vy = calculate_trajectory(h0, v0, angle_deg)

    # Визуализация результатов
    plot_results(t, x, y, vx, vy)

    print("Для выхода из программы нажмите enter")
    while True:
        if keyboard.is_pressed("enter"):
            break

if __name__ == "__main__":
    main()
