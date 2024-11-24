import sys
import struct


def assemble(input_file, output_file, log_file):
    commands = {
        'LOAD': 0x0F,
        'LESS_THAN': 0x3C,
        'READ': 0x99,  # Новая команда для чтения из памяти
        'WRITE': 0x8D,  # Новая команда для записи в память
    }

    log = []
    binary_code = bytearray()

    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            cmd = parts[0]

            if cmd == 'LOAD':
                if len(parts) != 4:
                    print(f"Ошибка: Неверное количество аргументов для команды LOAD: {line.strip()}")
                    continue

                A_index = int(parts[1])  # Индекс вектора A
                A_value = int(parts[2])  # Значение для загрузки в A
                B_value = int(parts[3])  # Значение для загрузки в B

                # Запись команды LOAD в бинарный код
                binary_code.extend(struct.pack('>B B', commands[cmd], A_index))
                log.append(f"{line.strip()}=0x{binary_code[-2:].hex()}")

                # Запись значений в векторы A и B
                binary_code.append(A_value)  # Значение A
                binary_code.append(B_value)  # Значение B

            elif cmd == 'LESS_THAN':
                if len(parts) != 4:
                    print(f"Ошибка: Неверное количество аргументов для команды LESS_THAN: {line.strip()}")
                    continue

                A = int(parts[1])  # Индекс вектора A
                B = int(parts[2])  # Индекс вектора B
                C = int(parts[3])  # Адрес для результата
                binary_code.extend(struct.pack('>B B B', commands[cmd], A, B))
                binary_code.append(C)  # C будет 1 байт (адрес для результата)
                log.append(f"{line.strip()}=0x{binary_code[-5:].hex()}")

            elif cmd == 'READ':
                if len(parts) != 4:
                    print(f"Ошибка: Неверное количество аргументов для команды READ: {line.strip()}")
                    continue

                A = int(parts[1])  # Адрес для чтения
                B = int(parts[2])  # Адрес для хранения результата
                C = int(parts[3])  # Смещение
                binary_code.extend(struct.pack('>B B B', commands[cmd], A, B))
                binary_code.append(C)  # C будет 1 байт (смещение)
                log.append(f"{line.strip()}=0x{binary_code[-5:].hex()}")

            elif cmd == 'WRITE':
                if len(parts) != 4:
                    print(f"Ошибка: Неверное количество аргументов для команды WRITE: {line.strip()}")
                    continue

                A = int(parts[1])  # Значение для записи
                B = int(parts[2])  # Адрес, откуда брать значение
                C = int(parts[3])  # Адрес для записи
                binary_code.extend(struct.pack('>B B I', commands[cmd], A, C))
                log.append(f"{line.strip()}=0x{binary_code[-6:].hex()}")

    with open(output_file, 'wb') as f:
        f.write(binary_code)

    with open(log_file, 'w') as f:
        for entry in log:
            f.write(entry + '\n')


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, output_file, log_file)
