import sys
import struct


def assemble(input_file, output_file, log_file):
    commands = {
        'LOAD': 0x0F,
        'LESS_THAN': 0x3C,
    }

    log = []
    binary_code = bytearray()

    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            cmd = parts[0]

            if cmd == 'LOAD':
                A = int(parts[1])  # Индекс вектора
                value = int(parts[2])  # Значение для загрузки
                C = int(parts[3])  # Адрес для записи
                binary_code.extend(struct.pack('>B B I', commands[cmd], A, C))
                log.append(f"{line.strip()}=0x{binary_code[-6:].hex()}")

            elif cmd == 'LESS_THAN':
                A = int(parts[1])  # Индекс вектора A
                B = int(parts[2])  # Индекс вектора B
                C = int(parts[3])  # Адрес для результата
                binary_code.extend(struct.pack('>B B B', commands[cmd], A, B))
                binary_code.append(C)  # C будет 1 байт (адрес для результата)
                log.append(f"{line.strip()}=0x{binary_code[-5:].hex()}")

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
