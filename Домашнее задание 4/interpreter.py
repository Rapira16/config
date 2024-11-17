import sys
import struct
import csv


def interpret(binary_file, output_file):
    memory = [0] * 256

    # Инициализация векторов A и B
    memory[5] = 5  # A[0]
    memory[6] = 3  # A[1]
    memory[7] = 8  # A[2]
    memory[8] = 6  # A[3]
    memory[9] = 2  # A[4]
    memory[10] = 4  # A[5]

    memory[11] = 7  # B[0]
    memory[12] = 2  # B[1]
    memory[13] = 9  # B[2]
    memory[14] = 5  # B[3]
    memory[15] = 3  # B[4]
    memory[16] = 6  # B[5]

    # Инициализация вектора C
    for i in range(6):
        memory[17 + i] = 0

    # Вывод значений векторов A и B для проверки
    print("Values in A:")
    for i in range(6):
        print(f"A[{i}] = {memory[5 + i]}")

    print("Values in B:")
    for i in range(6):
        print(f"B[{i}] = {memory[11 + i]}")

    with open(binary_file, 'rb') as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            opcode = struct.unpack('>B', byte)[0]

            if opcode == 0x0F:  # LOAD
                A, C = struct.unpack('>B I', f.read(5))
                memory[C] = memory[A]
            elif opcode == 0x3C:  # LESS_THAN
                A, B = struct.unpack('>B B', f.read(2))
                C = 17 + A  # Используем индекс A для записи результата в C

                # Получаем значения для сравнения
                value_A = memory[5 + A]
                value_B = memory[11 + B]

                # Вывод значений для сравнения
                print(f"Comparing A[{A}] = {value_A} with B[{B}] = {value_B}")

                # Сравниваем значения из памяти
                if value_A < value_B:
                    memory[C] = 1
                    print(f"Result: C[{C}] = 1 (True)")
                else:
                    memory[C] = 0
                    print(f"Result: C[{C}] = 0 (False)")

    # Запись результатов в CSV файл
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(6):
            writer.writerow([f'C[{i}]', memory[17 + i]])


if __name__ == "__main__":
    binary_file = sys.argv[1]
    output_file = sys.argv[2]
    interpret(binary_file, output_file)
