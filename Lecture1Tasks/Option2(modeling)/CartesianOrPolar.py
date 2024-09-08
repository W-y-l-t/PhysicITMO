import math
import keyboard

def cartesian_to_polar(x, y, precision):
    r = round(math.sqrt(x ** 2 + y ** 2), precision)
    theta = round(math.atan2(y, x), precision)  # используем atan2 для правильного вычисления угла

    return r, theta

def polar_to_cartesian(r, theta, precision):
    x = round(r * math.cos(theta), precision)
    y = round(r * math.sin(theta), precision)

    return x, y

def main():
    system = input("Введите тип системы координат для преобразования (cartesian/polar): ").strip().lower()

    if system == "cartesian":
        x = float(input("Введите координату X: "))
        y = float(input("Введите координату Y: "))
        precision = int(input("Введите точность (количество знаков после запятой): "))

        r, theta = cartesian_to_polar(x, y, precision)

        print(f"Полярные координаты: r = {r}, theta = {theta} (в радианах)")

    elif system == "polar":
        r = float(input("Введите радиус r: "))
        theta = float(input("Введите угол theta (в радианах): "))
        precision = int(input("Введите точность (количество знаков после запятой): "))

        x, y = polar_to_cartesian(r, theta, precision)

        print(f"Декартовы координаты: x = {x}, y = {y}")

    else:
        print("Неверный ввод системы координат.")

    print("Для выхода из программы нажмите enter")
    while True:
        if keyboard.is_pressed("enter"):
            break

if __name__ == "__main__":
    main()
