import os
import zipfile
import xml.etree.ElementTree as ET
import argparse


def extract_dependencies(nupkg_path, dependencies=None, visited=None):
    # Инициализация словаря зависимостей и множества посещенных пакетов
    if dependencies is None:
        dependencies = {}
    if visited is None:
        visited = set()

    # Открываем .nupkg файл как zip-архив
    with zipfile.ZipFile(nupkg_path, 'r') as z:
        # Перебираем все файлы в архиве
        for filename in z.namelist():
            # Ищем файл .nuspec, содержащий метаданные пакета
            if filename.endswith('.nuspec'):
                with z.open(filename) as file:
                    # Парсим .nuspec файл
                    tree = ET.parse(file)
                    root = tree.getroot()
                    ns = {'n': root.tag.split('}')[0].strip('{')}  # Определяем пространство имен
                    package_id = root.find('.//n:metadata/n:id', ns).text  # Получаем ID пакета
                    package_version = root.find('.//n:metadata/n:version', ns).text  # Получаем версию пакета

                    # Проверяем, был ли уже обработан этот пакет
                    if package_id not in visited:
                        visited.add(package_id)  # Добавляем пакет в посещенные

                        # Ищем группы зависимостей
                        for dep_group in root.findall('.//n:dependencies', ns):
                            for dep in dep_group.findall('.//n:dependency', ns):
                                dep_package = dep.attrib['id']  # ID зависимого пакета
                                dep_version = dep.attrib['version']  # Версия зависимого пакета

                                # Если зависимый пакет еще не был посещен
                                if dep_package not in visited:
                                    dependencies[dep_package] = dep_version  # Добавляем зависимость

                                    # Рекурсивно извлекаем зависимости для этого пакета
                                    try:
                                        dep_nupkg_path = f"{os.path.dirname(nupkg_path)}/{dep_package}.{dep_version}.nupkg"
                                        if os.path.exists(dep_nupkg_path):  # Проверяем, существует ли пакет
                                            extract_dependencies(dep_nupkg_path, dependencies, visited)
                                    except Exception as e:
                                        print(f"Ошибка при извлечении зависимостей для {dep_package}: {str(e)}")

    return dependencies  # Возвращаем все найденные зависимости


def generate_plantuml(dependencies, main_package):
    plantuml_code = "@startuml\n"  # Начало PlantUML кода
    added_edges = set()  # Множество для отслеживания добавленных связей

    # Создаем связи между основным пакетом и его зависимостями
    for dep, version in dependencies.items():
        # Добавляем связь от основного пакета к зависимому пакету
        plantuml_code += f"[{main_package}] --> [{dep} {version}]\n"
        added_edges.add((main_package, dep))  # Запоминаем добавленную связь

        # Рекурсивно добавляем зависимости для каждого зависимого пакета
        for inner_dep, inner_version in dependencies.items():
            if inner_dep != dep:  # Проверяем, чтобы не добавлять связь с самим собой
                edge = (dep, inner_dep)
                reverse_edge = (inner_dep, dep)
                # Проверяем, была ли уже добавлена эта связь или обратная связь
                if edge not in added_edges and reverse_edge not in added_edges:
                    plantuml_code += f"[{dep} {version}] --> [{inner_dep} {inner_version}]\n"
                    added_edges.add(edge)  # Запоминаем добавленную связь

    plantuml_code += "@enduml"  # Конец PlantUML кода
    return plantuml_code  # Возвращаем сгенерированный код


def main():
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description="Dependency Graph Visualizer for .NET packages")
    parser.add_argument("nupkg_path", help="Path to the .NET package file")  # Путь к .nupkg файлу
    parser.add_argument("output_path", help="Path to output the result code")  # Путь для сохранения результата
    args = parser.parse_args()  # Получаем аргументы

    # Извлекаем зависимости из указанного пакета
    dependencies = extract_dependencies(args.nupkg_path)

    # Извлекаем имя основного пакета
    main_package = os
