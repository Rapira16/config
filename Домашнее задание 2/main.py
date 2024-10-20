import os
import zipfile
import xml.etree.ElementTree as ET
import argparse


def extract_dependencies(nupkg_path, dependencies=None, visited=None):
    if dependencies is None:
        dependencies = {}
    if visited is None:
        visited = set()

    with zipfile.ZipFile(nupkg_path, 'r') as z:
        for filename in z.namelist():
            if filename.endswith('.nuspec'):
                with z.open(filename) as file:
                    tree = ET.parse(file)
                    root = tree.getroot()
                    ns = {'n': root.tag.split('}')[0].strip('{')}
                    package_id = root.find('.//n:metadata/n:id', ns).text
                    package_version = root.find('.//n:metadata/n:version', ns).text

                    if package_id not in visited:
                        visited.add(package_id)

                        for dep_group in root.findall('.//n:dependencies', ns):
                            for dep in dep_group.findall('.//n:dependency', ns):
                                dep_package = dep.attrib['id']
                                dep_version = dep.attrib['version']

                                if dep_package not in visited:
                                    dependencies[dep_package] = dep_version

                                    # Рекурсивно извлекаем зависимости для этого пакета
                                    try:
                                        dep_nupkg_path = f"{os.path.dirname(nupkg_path)}/{dep_package}.{dep_version}.nupkg"
                                        if os.path.exists(dep_nupkg_path):
                                            extract_dependencies(dep_nupkg_path, dependencies, visited)
                                    except Exception as e:
                                        print(f"Ошибка при извлечении зависимостей для {dep_package}: {str(e)}")

    return dependencies


def generate_plantuml(dependencies, main_package):
    plantuml_code = "@startuml\n"
    added_edges = set()  # Множество для отслеживания добавленных связей

    # Создаем связи между основным пакетом и его зависимостями
    for dep, version in dependencies.items():
        # Добавляем связь от основного пакета к зависимому пакету
        plantuml_code += f"[{main_package}] --> [{dep} {version}]\n"
        added_edges.add((main_package, dep))

        # Рекурсивно добавляем зависимости для каждого зависимого пакета
        for inner_dep, inner_version in dependencies.items():
            if inner_dep != dep:
                edge = (dep, inner_dep)
                reverse_edge = (inner_dep, dep)
                # Проверяем, была ли уже добавлена эта связь или обратная связь
                if edge not in added_edges and reverse_edge not in added_edges:
                    plantuml_code += f"[{dep} {version}] --> [{inner_dep} {inner_version}]\n"
                    added_edges.add(edge)

    plantuml_code += "@enduml"
    return plantuml_code


def main():
    parser = argparse.ArgumentParser(description="Dependency Graph Visualizer for .NET packages")
    parser.add_argument("nupkg_path", help="Path to the .NET package file")
    parser.add_argument("output_path", help="Path to output the result code")
    args = parser.parse_args()

    dependencies = extract_dependencies(args.nupkg_path)

    # Извлекаем имя основного пакета
    main_package = os.path.basename(args.nupkg_path).split('.')[0]

    plantuml_code = generate_plantuml(dependencies, main_package)

    with open(args.output_path, 'w') as f:
        f.write(plantuml_code)

    print(f"PlantUML code has been written to {args.output_path}")


if __name__ == "__main__":
    main()
