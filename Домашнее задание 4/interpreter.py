import sys
import struct
import csv

def interpret(binary_file, output_file):
    memory = [0] * 256

    # Ввод значений для вектора A
    print("Введите 6 значений для вектора A:")
    for i in range(6):
        memory[5 + i] = int(input(f"A[{i}]: "))

    # Ввод значений для вектора B
    print("Введите 6 значений для вектора B:")
    for i in range(6):
        memory[11 + i] = int(input(f"B[{i}]: "))

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
