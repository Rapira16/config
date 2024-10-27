import toml
import argparse
import os


def parse_toml(input_file):
    try:
        with open(input_file, 'r') as f:
            return toml.load(f)
    except toml.TomlDecodeError as e:
        print(f"Ошибка при разборе TOML: {e}")
        return None


def generate_custom_config(toml_data):
    lines = []

    def process_value(value):
        if isinstance(value, str):
            return f'[[{value}]]'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            return f'list({", ".join(map(str, value))})'
        else:
            return str(value)

    for key, value in toml_data.items():
        if isinstance(value, dict):
            lines.append(f"{key} = {{")
            for sub_key, sub_value in value.items():
                lines.append(f"    {sub_key} = {process_value(sub_value)};")
            lines.append("}")
        else:
            lines.append(f"var {key} = {process_value(value)};")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Преобразование TOML в учебный конфигурационный язык.')
    parser.add_argument('input_file', help='Путь к входному файлу TOML')
    parser.add_argument('output_file', help='Путь к выходному файлу конфигурации')

    args = parser.parse_args()

    toml_data = parse_toml(args.input_file)
    if toml_data is not None:
        custom_config = generate_custom_config(toml_data)
        with open(args.output_file, 'w') as f:
            f.write(custom_config)


if __name__ == "__main__":
    main()
