import numpy as np
import matplotlib.pyplot as plt

# Функция для вычисления электрического поля от точечного заряда
def electric_field(q, r0, x, y):
    rx = x - r0[0]
    ry = y - r0[1]
    r = np.sqrt(rx ** 2 + ry ** 2)
    r3 = r ** 3 + 1e-12  # добавляем малую величину, чтобы избежать деления на 0
    Ex = q * rx / r3
    Ey = q * ry / r3
    return Ex, Ey

# Функция для вычисления потенциала от точечного заряда
def electric_potential(q, r0, x, y):
    rx = x - r0[0]
    ry = y - r0[1]
    r = np.sqrt(rx ** 2 + ry ** 2)
    r = np.maximum(r, 1e-12)  # избегаем деления на 0
    V = q / r
    return V

# Функция для расчета силы и момента силы, действующих на диполь
def dipole_force_and_torque(p, theta, x_dipole, y_dipole, Ex, Ey):
    E_dipole_x = np.interp(x_dipole, Ex[0, :], Ex[:, 0])
    E_dipole_y = np.interp(y_dipole, Ey[:, 0], Ey[0, :])

    force_x = p * np.cos(theta) * E_dipole_x
    force_y = p * np.sin(theta) * E_dipole_y
    force_magnitude = np.sqrt(force_x**2 + force_y**2)

    torque = p * (E_dipole_y * np.cos(theta) - E_dipole_x * np.sin(theta))

    return force_x, force_y, force_magnitude, torque

# Функция для получения и валидации пользовательского ввода
def get_user_input():
    charges = []
    try:
        n = int(input("Введите количество зарядов: "))
        if n <= 0:
            raise ValueError("Количество зарядов должно быть больше нуля.")

        for i in range(n):
            print(f"Заряд {i + 1}:")
            q = float(input("  Величина заряда (в Кл): "))
            x = float(input("  Координата X: "))
            y = float(input("  Координата Y: "))
            charges.append((q, (x, y)))
    except ValueError as e:
        print(f"Ошибка ввода: {e}. Попробуйте снова.")
        return get_user_input()

    # Ввод диполя
    print("Введите параметры диполя:")
    try:
        p = float(input("  Модуль дипольного момента p (Кл*м): "))
        theta = float(input("  Угол theta (в градусах): "))
        theta = np.radians(theta)  # Преобразование угла в радианы
        x_dipole = float(input("  Координата X диполя: "))
        y_dipole = float(input("  Координата Y диполя: "))
    except ValueError as e:
        print(f"Ошибка ввода: {e}. Попробуйте снова.")
        return get_user_input()

    return charges, (p, theta, (x_dipole, y_dipole))

# Основная программа
def main():
    print("Программа визуализации электростатического поля точечных зарядов и диполя.")
    charges, dipole = get_user_input()

    # Определяем границы области на основе зарядов
    x_coords = [pos[0] for _, pos in charges]
    y_coords = [pos[1] for _, pos in charges]

    x_min, x_max = min(x_coords) - 5, max(x_coords) + 5  # Добавляем отступы по X
    y_min, y_max = min(y_coords) - 5, max(y_coords) + 5  # Добавляем отступы по Y

    # Генерация сетки для расчетов
    x = np.linspace(x_min, x_max, 200)
    y = np.linspace(y_min, y_max, 200)
    X, Y = np.meshgrid(x, y)

    # Инициализация полей
    Ex, Ey = np.zeros(X.shape), np.zeros(Y.shape)
    V = np.zeros(X.shape)

    # Суммируем вклад каждого заряда
    for q, pos in charges:
        ex, ey = electric_field(q, pos, X, Y)
        Ex += ex
        Ey += ey
        V += electric_potential(q, pos, X, Y)

    # Расчет сил и момента для диполя
    p, theta, (x_dipole, y_dipole) = dipole
    force_x, force_y, force_magnitude, torque = dipole_force_and_torque(p, theta, x_dipole, y_dipole, Ex, Ey)

    print(f"Сила, действующая на диполь: Fx = {force_x:.2e} Н, Fy = {force_y:.2e} Н")
    print(f"Модуль силы: {force_magnitude:.2e} Н")
    print(f"Момент силы, действующий на диполь: {torque:.2e} Н·м")

    # Визуализация
    plt.figure(figsize=(12, 8))

    # Визуализация эквипотенциальных поверхностей
    levels = np.linspace(V.min(), V.max(), 50)
    plt.contour(X, Y, V, levels=levels, cmap='coolwarm', alpha=0.75)

    # Визуализация линий напряженности
    plt.streamplot(X, Y, Ex, Ey, color='black', linewidth=1)

    # Добавляем заряды на график
    for q, pos in charges:
        color = 'red' if q > 0 else 'blue'
        label = f'Заряд: {q} Кл, Координаты: ({pos[0]}, {pos[1]})'
        plt.scatter(*pos, color=color, s=50, label=label)

    # Добавляем диполь на график с уменьшенной стрелкой
    arrow_scale = 0.5  # Масштабируем длину стрелки
    plt.quiver(x_dipole, y_dipole, arrow_scale * np.cos(theta), arrow_scale * np.sin(theta),
               angles='xy', scale_units='xy', scale=1, color='green', label='Диполь')

    # Убираем дублирование легенды
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), title="Параметры зарядов и диполя", loc='center left',
               bbox_to_anchor=(1, 0.5))

    plt.title('Электрическое поле, эквипотенциальные поверхности и диполь')
    plt.xlabel('Ось X')
    plt.ylabel('Ось Y')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.tight_layout()  # Чтобы элементы не перекрывались
    plt.show()

if __name__ == "__main__":
    main()
