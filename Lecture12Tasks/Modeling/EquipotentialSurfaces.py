import numpy as np
import matplotlib.pyplot as plt


# Функция для вычисления электрического поля от точечного заряда
def electric_field(q, r0, x, y):
    """
    Вычисляет компоненты электрического поля (Ex, Ey) в точке (x, y)
    от точечного заряда q, расположенного в r0 (x0, y0).

    Параметры:
    - q: величина заряда
    - r0: координаты заряда (x0, y0)
    - x, y: координаты расчетной точки

    Возвращает:
    - Ex, Ey: компоненты электрического поля
    """
    rx = x - r0[0]
    ry = y - r0[1]
    r = np.sqrt(rx ** 2 + ry ** 2)
    r3 = r ** 3 + 1e-12  # добавляем малую величину, чтобы избежать деления на 0
    Ex = q * rx / r3
    Ey = q * ry / r3
    return Ex, Ey


# Функция для вычисления потенциала от точечного заряда
def electric_potential(q, r0, x, y):
    """
    Вычисляет электрический потенциал в точке (x, y)
    от точечного заряда q, расположенного в r0 (x0, y0).

    Параметры:
    - q: величина заряда
    - r0: координаты заряда (x0, y0)
    - x, y: координаты расчетной точки

    Возвращает:
    - V: значение потенциала
    """
    rx = x - r0[0]
    ry = y - r0[1]
    r = np.sqrt(rx ** 2 + ry ** 2)
    r = np.maximum(r, 1e-12)  # избегаем деления на 0
    V = q / r
    return V


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

    return charges


# Основная программа
def main():
    print("Программа визуализации электростатического поля точечных зарядов.")
    charges = get_user_input()

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

    # Визуализация
    plt.figure(figsize=(12, 8))  # Увеличен размер графика для удобства

    # Визуализация эквипотенциальных поверхностей
    levels = np.linspace(V.min(), V.max(), 50)  # Уровни потенциала
    plt.contour(X, Y, V, levels=levels, cmap='coolwarm', alpha=0.75)

    # Визуализация линий напряженности
    plt.streamplot(X, Y, Ex, Ey, color='black', linewidth=1)

    # Добавляем заряды на график
    for q, pos in charges:
        color = 'red' if q > 0 else 'blue'
        label = f'Заряд: {q} Кл, Координаты: ({pos[0]}, {pos[1]})'
        plt.scatter(*pos, color=color, s=50, label=label)

    # Убираем дублирование легенды
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), title="Параметры зарядов", loc='center left',
               bbox_to_anchor=(1, 0.5))

    plt.title('Электрическое поле и эквипотенциальные поверхности')
    plt.xlabel('Ось X')
    plt.ylabel('Ось Y')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.tight_layout()  # Чтобы элементы не перекрывались
    plt.show()


if __name__ == "__main__":
    main()
