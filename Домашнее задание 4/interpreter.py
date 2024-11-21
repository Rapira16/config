import sys
import struct
import csv


def interpret(binary_file, output_file):
    memory = [0] * 256

    # Чтение бинарного файла и извлечение значений векторов A и B
    with open(binary_file, 'rb') as f:
        binary_data = f.read()

    # Извлечение значений векторов A и B из бинарного кода
    # Предполагаем, что они хранятся в памяти начиная с индексов 5 и 11
    for i in range(6):
        memory[5 + i] = binary_data[i * 4 + 2]  # Значения A
        memory[11 + i] = binary_data[i * 4 + 5]  # Значения B

    print("Вектор A:", memory[5:11])
    print("Вектор B:", memory[11:17])

    # Инициализация вектора C
    for i in range(6):
        memory[17 + i] = 0

    # Сравнение значений из A и B
    for i in range(6):
        value_A = memory[5 + i]  # Значение из A
        value_B = memory[11 + i]  # Значение из B
        C_index = 17 + i  # Индекс для записи результата в C

        # Сравниваем значения из памяти
        if value_A < value_B:
            memory[C_index] = 1
        else:
            memory[C_index] = 0

    # Запись результатов в CSV файл
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(6):
            writer.writerow([f'C[{i}]', memory[17 + i]])


if __name__ == "__main__":
    binary_file = sys.argv[1]  # Оставляем это для совместимости, но не используем
    output_file = sys.argv[2]  # Выходной файл
    interpret(binary_file, output_file)
