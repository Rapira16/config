import argparse
import os


def parse_toml(input_file):
    toml_data = {}
    current_section = None

    try:
        with open(input_file, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue  # Пропустить пустые строки и комментарии

                # Проверка на секцию
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1].strip()
                    if current_section in toml_data:
                        raise SyntaxError(f"Ошибка: секция '{current_section}' уже определена на строке {line_number}.")
                    toml_data[current_section] = {}
                else:
                    # Разделение ключа и значения
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")  # Удаление кавычек

                        # Обработка массивов
                        if value.startswith('[') and value.endswith(']'):
                            value = value[1:-1].split(',')
                            value = [v.strip() for v in value]  # Удаление пробелов
                        else:
                            value = value  # Оставляем как строку

                        if not key:
                            raise SyntaxError(f"Ошибка: пустой ключ на строке {line_number}.")
                        if current_section:
                            toml_data[current_section][key] = value
                        else:
                            toml_data[key] = value
                    else:
                        raise SyntaxError(
                            f"Ошибка: неверный формат строки на строке {line_number}. Ожидалось 'ключ = значение'.")

    except SyntaxError as e:
        print(f"Синтаксическая ошибка в файле '{input_file}': {e}")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла '{input_file}': {e}")
        return None

    return toml_data


def generate_custom_config(toml_data):
    lines = []

    def process_value(value):
        if isinstance(value, str):
            return f'[[{value}]]'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            # Обработка списка, чтобы каждый элемент был в отдельных двойных квадратных скобках
            return ', '.join([f'[[{item}]]' for item in value])
        else:
            return str(value)

    for key, value in toml_data.items():
        if isinstance(value, dict):
            lines.append(f"{key} = {{")
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, list):
                    # Если sub_value - это список, то обрабатываем его отдельно
                    formatted_value = ', '.join([f'[[{item}]]' for item in sub_value])
                    lines.append(f"    {sub_key} = [{formatted_value}];")
                else:
                    lines.append(f"    {sub_key} = {process_value(sub_value)};")
            lines.append("}")
        else:
            lines.append(f"var {key} = {process_value(value)};")

    return "\n".join(lines).replace('"', '')


def main():
    parser = argparse.ArgumentParser(description='Преобразование TOML в учебный конфигурационный язык.')
    parser.add_argument('input_file', help='Путь к входному файлу TOML')
    parser.add_argument('output_file', help='Путь к выходному файлу конфигурации')

    args = parser.parse_args()

    toml_data = parse_toml(args.input_file)
    if toml_data is None:
        return  # Если есть синтаксическая ошибка, выходим

    custom_config = generate_custom_config(toml_data)
    try:
        with open(args.output_file, 'w') as f:
            f.write(custom_config)
    except Exception as e:
        print(f"Ошибка при записи в файл '{args.output_file}': {e}")


if __name__ == "__main__":
    main()
